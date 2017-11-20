#!/usr/bin/python3
# encoding: utf-8

'''
wrapper functions for usage of external commands

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

import subprocess
from Utils.Helper import TileInfo

from sys import platform
from kap.gen import KapGen

if platform == "linux" or platform == "linux2":
    COMPOSITE_APP = "composite"
    MONTAGE_APP = "montage"
    IMGKAP_APP = "ExternalUtils/imgkap/imgkap"
elif platform == "win32":
    COMPOSITE_APP = "ExternalUtils\\ImageMagick\\composite"
    MONTAGE_APP = "ExternalUtils\\ImageMagick\\montage"
    IMGKAP_APP = "ExternalUtils\\imgkap\\imgkap"
else:
    assert(0)


def _ProcessCmd(cmd):
    print("execure command: {}".format(cmd))
    return_code = subprocess.call(cmd, shell=True)
    return return_code


def MergePictures(self, SeaMapFilename, OSMFilename, ResultFilename):
    cmd = "{} {} {} {}".format(COMPOSITE_APP, SeaMapFilename, OSMFilename, ResultFilename)
    ret = _ProcessCmd(cmd)
    assert(ret == 0)


def JoinPicture(xcnt, ycnt, filenamelist, filename):
    cmd = "{} +frame +shadow +label -tile {}x{} -geometry 256x256+0+0 {} {}".format(MONTAGE_APP, xcnt, ycnt, filenamelist, filename)
    ret = _ProcessCmd(cmd)
    assert(ret == 0)


def GenerateKapFile(filenamein, filenameout, ti):

    cmd = "{} {} {} {} {} {} {} -t {}".format(IMGKAP_APP, filenamein, ti.NW_lat, ti.NW_lon, ti.SE_lat, ti.SE_lon, filenameout, ti.name)
    ret = _ProcessCmd(cmd)
    assert(ret == 0)

    cmd = "{} {} {} {} ".format(IMGKAP_APP, filenameout, filenameout + ".export.txt", filenameout + "export.png")
    ret = _ProcessCmd(cmd)
    assert(ret == 0)


def GenerateKapFileNew(filenamein, filenameout, ti):

    # generate header
    gen = KapGen()
    header = gen.GenHeader(ti)

    with open('temp.kap', "w") as f:
        f.write(header)

    cmd = "{} {} {} {} -t {}".format(IMGKAP_APP, filenamein, "temp.kap", filenameout, ti.name)
    ret = _ProcessCmd(cmd)
    assert(ret == 0)

    cmd = "{} {} {} {} ".format(IMGKAP_APP, filenameout, filenameout + ".export.txt", filenameout + "export.png")
    ret = _ProcessCmd(cmd)
    assert(ret == 0)

