﻿Changlog
++++++++

Versions
--------

1.8.2 - ??/??/2015
==================
- Fix systemctl service list on el7
- Fix registry key placement on fresh installs

1.8.1 - 04/09/2015
==================
- Fix aggregation of CPU percent only working on Windows
- Fix system/uptime not working on Windows

1.8.0 - 04/02/2015
==================
- Added graphing frontend, available via /graph-picker.html
- Added PID to process information returned by the API
- Adding aggregate function to aggregate list values for checks
- Adding uptime under /api/system/uptime
- Added delayed starting to windows NCPA services
- Changed web sockets to fail gracefully
- Changed uninstall key location for Windows users to be under HKCU
- Changed unit for the user count to be ‘’ rather than c
- Changed plugin to allow passed query arguments to URL
- Changed plugin to remove perfdata
- Changed windows NCPA services to be more windows-like
- Fixed Mac OS installer group/user issues
- Fixed NRDS file path issue on windows
- Fixing issues with /graph and accessing the same state file
- Fixed issue where page head links showed up on /login page
- Fixed issue where server would reject API POST queries
- Fixed windows installer to now upgrade NCPA when NCPA is installed already
- Fixed windows installer to not overwrite configuration file

1.7.2 - 08/28/2014
==================
- Fixed API giving 500 error on windows when filtering processes
- Fixed services filtering by single service name
- Fixed NCPA Passive init.d script on Debian systems
- Fixed issue where warning/critical values were truncated

1.7.1 - 08/19/2014
==================
- Added backwards compatability with the api/service(s) call to work with old plugins/checks
- Added log rotation to all clients, logs rotate at 20MB and will rotate once before overwriting old logs
- Added safeguards when importing disk nodes that prevented the listener from starting in certain circumstances
- Added link to the /top service in the web UI
- Added "diskperf -Y" command to automatically run during Windows install
- Added favicon to the web UI
- Removed unused files and old static docs
- Updated log format to be more descriptive
- Updated test runner to be Python rather than sh to run tests on Windows
- Updated plugin/file type directives to now retain quotes around $plugin_name when being passed to the command line
- Updated styling of main web UI screen
- Fixed issue with SSL certificates using the same serial number
- Fixed threading error on NCPA listener start/stop
- Fixed 500 access error on access
- Fixed Windows logging issue where logs were not at var/\*.log
- Fixed process count checks returning wrong number of processes

1.7.0 - 07/29/2014
==================
- Added full tests for NRDP
- Added realtime graphs
- Added Windows Event Log monitoring
- Added Windows counters monitoring ability
- Added manually creating SSL certificates, and added ability to specify
  cert and key files by specifying in the certificate field by
  a comma-delimited [path/to/cert],[path/to/key]
- Updated help documentation to include changes in 1.7.0
- Updated to non-blocking system using gevent to accomodate many connections
- Updated from the Flask development server for serving HTTPS requests
- Fixed init script for listener not getting the PID file correctly
- Fixed build issue with cx_Freeze which caused the built agent to not run
- Fixed build issue with docs not building during build process
- Fixed dependency issues with Debian systems
- Fixed doc builds during compilation
