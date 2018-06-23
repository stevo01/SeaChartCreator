#!/usr/bin/python33
# encoding: utf-8

'''
download of external utils

Copyright (C) 2017  Steffen Volkmann

This file is part of SeaMapCreator.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

'''

import urllib
from sys import platform
from Utils.Helper import ensure_dir
from Utils.ProcessCmd import _ProcessCmd
from pip._vendor.distlib.compat import ZipFile
import os
from Utils import __app_identifier__


# load singlke file with http protocol
def HttpLoadFile(url, filename):

    # set user agent to meet the tile usage policy
    # https://operations.osmfoundation.org/policies/tiles/

    print("HttpLoadFile open {}".format(url))
    req = urllib.request.Request(url, data=None, headers={'User-Agent': __app_identifier__})
    f = urllib.request.urlopen(req)
    data = f.read()
    print("HttpLoadFile transfer finished {}".format(url))

    print("HttpLoadFile open file {}".format(filename))
    with open(filename, 'wb') as f:
        print("HttpLoadFile write {} bytes".format(len(data)))
        f.write(data)

    return filename


def CheckExternelUtils():
    '''
    note: libfreeimage is required to compile inux version of imgkap.
          sample installation for debian: sudo apt install libfreeimage3
    '''
    downloadPath = 'ExternalUtils/'

    ImageMagick_Filename = "ImageMagick-7.0.8-1-portable-Q16-x64.zip"
    FileNameImageMagick = downloadPath + ImageMagick_Filename
    PathNameImageMagick = downloadPath + 'ImageMagick'
    urlImageMagick = 'https://www.imagemagick.org/download/binaries/{}'.format(ImageMagick_Filename)

    if platform == "linux" or platform == "linux2":
        PathName_imgkap = downloadPath + 'imgkap/'
        FileName_imgkap_src = PathName_imgkap + 'imgkap.c'
        FileName_imgkap_exe = PathName_imgkap + 'imgkap'

        url_imgkap = 'http://www.dacust.com/inlandwaters/imgkap/v00.01.11/imgkap.c'

        ensure_dir(PathName_imgkap)

        if(os.path.isfile(FileName_imgkap_src) is False):
            print("start download {}".format(url_imgkap))
            HttpLoadFile(url_imgkap, FileName_imgkap_src)

        if(os.path.isfile(FileName_imgkap_exe) is False):
            print("compile {}".format(FileName_imgkap_src))
            _ProcessCmd("cd {}; gcc imgkap.c -O3 -s -lm -lfreeimage -o imgkap".format(PathName_imgkap))

        pass
    elif platform == "win32":
        if(os.path.isfile(FileNameImageMagick) is False):
            print("start download {}".format(urlImageMagick))
            filename = HttpLoadFile(urlImageMagick, FileNameImageMagick)

        if(os.path.isdir(PathNameImageMagick) is False):
            with ZipFile(FileNameImageMagick) as myzip:
                myzip.extractall(path=PathNameImageMagick)

        PathName_imgkap = downloadPath + 'imgkap/'
        FileName_imgkap = PathName_imgkap + 'imgkap.exe'
        url_imgkap = 'http://www.dacust.com/inlandwaters/imgkap/v00.01.11/imgkap.exe'

        ensure_dir(PathName_imgkap)

        if(os.path.isfile(FileName_imgkap) is False):
            print("start download {}".format(url_imgkap))
            HttpLoadFile(url_imgkap, FileName_imgkap)
