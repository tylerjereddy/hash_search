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
import tarfile
import urllib
import tempfile
import urllib.request
import os
from pathlib import Path
import hashlib

# from shasum -a 256 libopenblasp-r0.3.0.dev.dylib
# in the MacOS 64-bit wheel from a recent CRON job:
known_sha256 ='2f7888f884abe46be2151b75b5ce00a9e6b839b35804f6568e7a90bed13074b7'
url = "https://3f23b170c54c2533c070-1c8a9b3114517dc5fe17b7c3f8c63a43.ssl.cf2.rackcdn.com/"
html_page = requests.get(url)
soup = BeautifulSoup(html_page.content, features='html5lib')
num_matching_hashes = 0
for link in soup.findAll('a'):
    filename = link.get('href')
    if ('openblas' in filename and
        '0.3.0' in filename and
        ('Darwin' in filename or
         'osx' in filename)):
         # these files are all of type *.tar.gz
         print(filename)
         # download the tarfile to a temporary location
         with tempfile.TemporaryDirectory() as tempdir:
            download_url = urllib.parse.urljoin(url, filename)
            temp_filename = os.path.join(tempdir, filename)
            urllib.request.urlretrieve(download_url, temp_filename)
            # inspect the downloaded tar file
            with tarfile.open(temp_filename, "r:gz") as tarF:
               for member in tarF:
                   if 'libopenblasp-r0.3.0.dev.dylib' in member.name:
                       # extract the file and check its hash against
                       # reference value
                       tarF.extract(member, path=tempdir)
                       candidate_file = os.path.join(tempdir, member.name)
                       print("candidate_file:", candidate_file)
                       with open(candidate_file, 'rb') as candidate:
                           all_bytes = candidate.read()
                           hashval = hashlib.sha256(all_bytes).hexdigest()
                           print("hashval:", hashval)
                           if hashval == known_sha256:
                              num_matching_hashes += 1
                              print("hashes match!!")

print("Total number of matching hashes:", num_matching_hashes)
