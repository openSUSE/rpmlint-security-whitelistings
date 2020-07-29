Security Whitelisting Information for rpmlint-checks
====================================================

In openSUSE [rpmlint-checks](https://github.com/openSUSE/rpmlint-checks) are
used for performing quality assurance on RPM packages. An important part of
these checks are security related and managed by the [SUSE security
team](https://www.suse.com/support/security/).

This repository here is used to administer whitelisting information consumed
by the rpmlint-mini package to actually implement whitelisting restrictions on
certain packaging features.

The maintainer of this repository is the SUSE [security
team](mailto:security@suse.com).

Whitelisting Format
-------------------

The whitelists use the JSON syntax to support a structured and hierarchical
configuration format. A downside of JSON is that no inline comments are
supported like in most other configuration formats. For this reason an
explicit "comment" field is supported for each audit entry.

Most of the whitelisting files should be self-explanatory by looking at them.
For each package a single entry is present in the whitelist. To be extra
prudent the whitelisting usually also checks file contents by keeping track of
the sha256 digests of the whitelisted files. If the packaged file content
changes then a follow-up review by the security team becomes necessary.
Therefore a list of related audits is maintained for each whitelisting entry
complete with Bugzilla reference, file digests and an optional whitelisting
comment.

Every audit section must list the complete state of a package, not just
incremental changes to a previous audit.

Types of Whitelistings
----------------------

### Digest Based Whitelistings

This type of whitelist cares about the contents of files in certain file
system locations. It whitelists file system entries by name and an optional
content digest.

### Metadata Based Whitelistings

This type of whitelist cares about a file's metadata like file type and UNIX
permissions. It whitelists file system entries by comparing the file type,
mode bits and ownership.

Instances of Whitelistings
--------------------------

### Cron Jobs

The file `cron-whitelist.json` contains whitelisting entries for files
installed in one of the directories in /etc/cron.{d,daily,hourly,montly,weekly}.
Cron jobs often run as the `root` user and default-enabled cron jobs are high
risk candidates for security issues. Therefore the security team puts
restrictions on the introduction of new cron jobs or changes to existing cron
jobs.

### Device Files

The file `device-files-whitelist.json` contains whitelisting entries for
device file packaged in RPMs. Device files in RPMs should be an unusual
event. Since device files with bad permissions may allow unprivileged users to
access sensitive system devices it is important to restrict packaging of this
type of files. A metadata whitelisting is used for whitelist any occurences of
device files in packages.

### World Writable Files

There shouldn't be any files packaged that are world-writable. A few
exceptions are public sticky-bit directories or UNIX domain sockets that are
accessible to everybody. These occurrences are covered by this metadata
whitelisting.

### Note About setuid/setgid Bits

Setuid, setgid or capability bits are currently not kept track of here,
because they are managed by the [permissions
package](https://github.com/openSUSE/permissions).

Whitelisting Examples
---------------------

In the following example, comment lines introduced with '#' are embedded for
being able to more easily document the data structure. The actual JSON format
does *not* support such comments, however.

<pre>
# a digest based whitelist
{
    # the package name
    "atop-daemon": {

        # a dictionary containing all the audits and related
        # whitelistings done so far
        "audits": {

            # the key is the SUSE Bugzilla bug number where the # Audit of the
            # package's security features has been performed.
            # The value is another dictionary.
            "bsc#1150533": {

                # This comment is for documentation purposes and is not
                # further used in whitelisting checks.
                "comment": "Performs maintenance and (re)starting of the atop daemon",

                # This contains another dictionary listing the files for which
                # restrictions apply. The whitelisting restriction is not
                # limited to the file causing the whitelisting check to
                # trigger in the first place (like a cron job) but may also
                # list related files that are involved and may cause security
                # issues.
                "digests": {

                    # the keys are the absolute file paths that are the subject
                    # of the whitelisting
                    #
                    # the values are of the form [alg]:[digest], where [alg]
                    # is a hash algorithm supported by the Python hashlib.
                    "/etc/cron.d/atop": "sha256:d8b23c4f9bda803bc8627c23361635a876bc49fc0ace0d98fcd92c7fb33ac430"

                    # it is also possible to explicitly whitelist a file with
                    # arbitrary content for special cases where the content of
                    # the whitelisted file isn't fixed for some reason
                    "/usr/share/atop/atop.daily": "skip:<none>",
                }
            }
        }
    }
}
</pre>

<pre>
# a metadata based whitelist
{
    "filesystem": {
        "audits": {
            "bsc#123456": {
                "comment": "some typical special files",
                # here we use a meta entry instead of a "digests" entry to
                # whitelist file properties in contrast to file contents.
                "meta": {
                    "/some/dev": {
                        # denotes the whitelisted type of file. supported
                        # characters are currently:
                        # '-': regular file
                        # 'd': directory
                        # 'c': character device
                        # 'b': block device
                        # 's': UNIX domain socket
                        "type": "b",
			# the allowed UNIX octal file mode
                        "mode": "0666",
                        # for device files this denotes the allowed minor and
                        # major device number separated by comma
                        "dev": "1,2",
                        # the allowed user and group ownership for the file
                        "owner": "root:root"
                    }
                }
            }
        }
    }
}
</pre>
