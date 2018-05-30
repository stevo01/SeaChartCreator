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

import os
import urllib.request
from pip._vendor.distlib.compat import ZipFile
from Utils.ProcessCmd import MergePictures, JoinPicture, GenerateKapFile, \
    _ProcessCmd, GenerateKapFileNew
from Utils.Helper import ensure_dir
from platform import linux_distribution
from sys import platform


class MapDownloadManager(object):
    '''
    classdocs
    '''

    def __init__(self, DownloadPath, WorkingPath, version):
        # set attributes
        self.urlOSM = 'http://a.tile.openstreetmap.org'
        self.urlOSeaMap = 'http://tiles.openseamap.org/seamark'
        self.DownloadPath = DownloadPath
        self.WorkingPath = WorkingPath
        self.version = version

        # call the CheckExternelUtils() to ensure that all external applications are available
        self.CheckExternelUtils()
        return

    # load singlke file with http protocol
    def _HttpLoadFile(self, url, filename):

        # set user agent to meet the tile usage policy
        # https://operations.osmfoundation.org/policies/tiles/

        print("HttpLoadFile open {}".format(url))
        req = urllib.request.Request(url, data=None, headers={'User-Agent': self.version})
        f = urllib.request.urlopen(req)
        data = f.read()
        print("HttpLoadFile transfer finished {}".format(url))

        print("HttpLoadFile open file {}".format(filename))
        with open(filename, 'wb') as f:
            print("HttpLoadFile write {} bytes".format(len(data)))
            f.write(data)

        return filename

    def CheckExternelUtils(self):
        downloadPath = 'ExternalUtils/'
        # FileNameImageMagick = downloadPath + 'ImageMagick-7.0.7-11-portable-Q16-x86.zip'
        # PathNameImageMagick = downloadPath + 'ImageMagick'
        # urlImageMagick = 'http://ftp.icm.edu.pl/packages/ImageMagick/binaries/ImageMagick-7.0.7-11-portable-Q16-x86.zip'

        FileNameImageMagick = downloadPath + 'ImageMagick-7.0.7-36-portable-Q16-x86.zip'
        PathNameImageMagick = downloadPath + 'ImageMagick'
        urlImageMagick = 'https://www.imagemagick.org/download/binaries/ImageMagick-7.0.7-36-portable-Q16-x86.zip'


        if platform == "linux" or platform == "linux2":
            PathName_imgkap = downloadPath + 'imgkap/'
            FileName_imgkap_src = PathName_imgkap + 'imgkap.c'
            FileName_imgkap_exe = PathName_imgkap + 'imgkap'

            url_imgkap = 'http://www.dacust.com/inlandwaters/imgkap/v00.01.11/imgkap.c'

            ensure_dir(PathName_imgkap)

            if(os.path.isfile(FileName_imgkap_src) is False):
                print("start download {}".format(url_imgkap))
                self._HttpLoadFile(url_imgkap, FileName_imgkap_src)

            if(os.path.isfile(FileName_imgkap_exe) is False):
                print("compile {}".format(FileName_imgkap_src))
                _ProcessCmd("cd {}; gcc imgkap.c -O3 -s -lm -lfreeimage -o imgkap".format(PathName_imgkap))

            pass
        elif platform == "win32":
            if(os.path.isfile(FileNameImageMagick) is False):
                print("start download {}".format(urlImageMagick))
                filename = self._HttpLoadFile(urlImageMagick, FileNameImageMagick)

            if(os.path.isdir(PathNameImageMagick) is False):
                with ZipFile(FileNameImageMagick) as myzip:
                    myzip.extractall(path=PathNameImageMagick)

            PathName_imgkap = downloadPath + 'imgkap/'
            FileName_imgkap = PathName_imgkap + 'imgkap.exe'
            url_imgkap = 'http://www.dacust.com/inlandwaters/imgkap/v00.01.11/imgkap.exe'

            ensure_dir(PathName_imgkap)

            if(os.path.isfile(FileName_imgkap) is False):
                print("start download {}".format(url_imgkap))
                self._HttpLoadFile(url_imgkap, FileName_imgkap)

    #  file format for storage: /level/x/y.png
    #  file format for montage: level-x-y.png  SeaMap-$level-$y-$x.png
    def _LoadPicture(self, name, level, x, y):
        PathOSM = self.DownloadPath + "/osm/{}/{}/".format(level, x)
        PathSeaMap = self.DownloadPath + "/seamap/{}/{}/".format(level, x)
        PathSeaMapMerged = self.WorkingPath + "/seamapmerged/{}/{}/".format(name, level)

        FileNameOSM = "{}{}.png".format(PathOSM, y)
        FileNameSeaMap = "{}{}.png".format(PathSeaMap, y)
        FileNameSeaMapMerged = "{}{}-{}-{}.png".format(PathSeaMapMerged, level, y, x)

        urlOSM = "{}/{}/{}/{}.png".format(self.urlOSM, level, x, y)
        urlOSeaMap = "{}/{}/{}/{}.png".format(self.urlOSeaMap, level, x, y)

        if not os.path.exists(PathOSM):
            os.makedirs(PathOSM)

        if not os.path.exists(PathSeaMap):
            os.makedirs(PathSeaMap)

        if not os.path.exists(PathSeaMapMerged):
            os.makedirs(PathSeaMapMerged)

        if(os.path.isfile(FileNameOSM) is False):
            print("loadHttp: {}".format(urlOSM))
            self._HttpLoadFile(urlOSM, FileNameOSM)
        else:
            print("skip: {}".format(urlOSM))

        if(os.path.isfile(FileNameSeaMap) is False):
            print("loadHttp: {}".format(urlOSeaMap))
            self._HttpLoadFile(urlOSeaMap, FileNameSeaMap)
        else:
            print("skip: {}".format(urlOSeaMap))

        if(os.path.isfile(FileNameSeaMapMerged) is False):
            MergePictures(FileNameSeaMap, FileNameOSM, FileNameSeaMapMerged)

        return FileNameSeaMapMerged

    def LoadTiles(self, ti):
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                self._LoadPicture(ti.name, ti.zoom, x, y) + " "

    def GetMapFilename(self, ti):
        return "{}/seamapmerged/{}/{}/{}_{}.png".format(self.WorkingPath, ti.name, ti.zoom, ti.name, ti.zoom)

    def MergeTiles(self, ti):
        tempfilename = self.GetMapFilename(ti)
        if(os.path.isfile(tempfilename) is False):
            JoinPicture(ti.x_cnt, ti.y_cnt, "{}/seamapmerged/{}/{}/*.png".format(self.WorkingPath, ti.name, ti.zoom), tempfilename)

    def GenKapFile(self, ti):
        tempfilename = self.GetMapFilename(ti)
        kapdirname = "{}/kap".format(self.WorkingPath)
        kapfilename = "{}/{}_{}.kap".format(kapdirname, ti.name, ti.zoom)
        kapfilenamenew = "{}/{}_{}new.kap".format(kapdirname, ti.name, ti.zoom)

        if not os.path.exists(kapdirname):
            os.makedirs(kapdirname)

        if(os.path.isfile(kapfilename) is False):
            GenerateKapFile(tempfilename, kapfilename, ti)

        #if(os.path.isfile(kapfilenamenew) is False):
        #    GenerateKapFileNew(tempfilename, kapfilenamenew, ti)

        return

    def PrintInfo(self, ti):
        print(ti)
