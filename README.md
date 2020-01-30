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

Types of Whitelistings
----------------------

### Cron Jobs

The file `cron-whitelist.json` contains whitelisting entries for files
installed in one of the directories in /etc/cron.{d,daily,hourly,montly,weekly}.
Cron jobs often run as the `root` user and default-enabled cron jobs are high
risk candidates for security issues. Therefore the security team puts
restrictions on the introduction of new cron jobs or changes to existing cron
jobs.

Whitelisting Examples
---------------------

In the following example, comment lines introduced with '#' are embedded for
being able to more easily document the data structure. The actual JSON format
does *not* support such comments, however.

<pre>
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
