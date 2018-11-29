"""
The purpose of this module is to identify
a specific pre-built openblas library file
(i.e., zip file or similar) on the MacPython
community binaries rackspace URL that matches
the version of openblas linked in on our recent
(i.e., CRON job) numpy-wheel OS X builds.

This information is desirable because I would like
to have our Azure CI Mac OS job use the exact matching
openblas pre-built binary as our wheel builds
"""
