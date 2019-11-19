Security Whitelisting Information for rpmlint-checks
====================================================

In openSUSE [rpmlint-checks](https://github.com/openSUSE/rpmlint-checks) are
used for performing quality assurance on RPM packages. An important part of
these checks are security related and managed by the [SUSE security
team](https://www.suse.com/support/security/).

This repository here is used to administer whitelisting information consumed
by the rpmlint-mini package to actually implement whitelisting restriction on
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
For each package and whitelisted file a single entry is present in the
whitelist. To be extra prudent the whitelisting usually also checks file
contents by keeping tracking of the sha256 digests of the whitelisted files.
If the content changes then a follow-up review by the security team becomes
necessary. Therefore a list of related audits is maintained for each
whitelisting entry complete with Bugzilla reference, file digest and an
optional whitelisting comment.

Since in some cases the cron job file is only a small wrapper around the
actual program, the whitelisting format also supports a `related` dictionary
for each audit entry. This can list additional files that are related to the
whitelisting and which should be checked for changes.

Types of Whitelistings
----------------------

### Cron Jobs

The file `cron-whitelist.json` contains whitelisting entries for files
installed in one of the directories in /etc/cron.{d,daily,hourly,montly,weekly}.
Cron jobs often run as the `root` user and efault-enabled cron jobs are high
risk candidates for security issues. Therefore the security team puts
restrictions on the introduction of new cron jobs or changes to existing cron
jobs.
