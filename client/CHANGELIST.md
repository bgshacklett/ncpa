0.3.5
-----
- Added in the 'queryargs' variable to pass in extra arguments to the URL being called
- Fixed missing query_args error

0.3.4
-----
- Added timeout option (-T)

0.3.3
-----
- Fixed issue where --list with no metric would cause an error

0.3.2
-----
- Fixed issue where --unit would change the base unit, not the unit prefix
- Added --units/-n that will change the base unit

0.3.1
-----
- Added quoting to arguments intended to by passed to Nagios plugins, all HTML element given with --arguments, -a will be escaped
- Added --super-verbose flag to aid in debugging. Adds stack track on Exceptional exit
- Moved to Major.Minor.Maintenance versioning scheme to align with NCPA
- Added sanity check so -a/--arguments cannot be called when not calling a plugin

0.3
---
- Moved into main git repository
- Fixed minor bugs

0.2
---
- Fixed Python2 incompatibility.
