# -*- coding: utf-8 -*-

import requests
from urllib import parse, request
from clint.textui import progress
from ftplib import FTP


def download(url, filename):
    o = parse.urlparse(url)
    if o.scheme in ['http', 'https',]:
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
    elif o.scheme in ['ftp', 'ftps',]:
        r = request.urlopen(url)
        with open(filename, 'wb') as f:
            ftp = FTP(o.netloc)
            ftp.login()
            total_length = ftp.size(o.path)
            # TODO: Use ftplib to download it with progress bar
            for chunk in progress.bar(iter(lambda: r.read(1024), ''), expected_size=(total_length / 1024) + 1):
                if not chunk:
                    break
                f.write(chunk)
                f.flush()

