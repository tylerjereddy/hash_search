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

from bs4 import BeautifulSoup
import requests

url = "https://3f23b170c54c2533c070-1c8a9b3114517dc5fe17b7c3f8c63a43.ssl.cf2.rackcdn.com/"
html_page = requests.get(url)
soup = BeautifulSoup(html_page.content, features='html5lib')
for link in soup.findAll('a'):
    filename = link.get('href')
    if ('openblas' in filename and
        '0.3.0' in filename and
        ('Darwin' in filename or
         'osx' in filename)):
         # these files are all of type *.tar.gz
         print(filename)
