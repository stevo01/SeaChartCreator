#!/usr/bin/python3
# encoding: utf-8

'''

Copyright (C) 2017  Steffen Volkmann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

from Utils.glog import getlog
from tile.DownloadThread import DownloadThread
from tile.sqllitedb import TileSqlLiteDB
from tile.MergeThread import MergeThread

MERGEDIR = 'Merge/'


class TileServer():

    def __init__(self, name, url):
        self.name = name
        self.url = url


class TileManager(object):
    '''
    classdocs
    '''

    def __init__(self, WorkingDirectory, DBDIR, force_download):
        '''
        Constructor
        '''
        self._WorkingDirectory = WorkingDirectory

        self.DBDIR = DBDIR
        self.logger = getlog()

        self.tile = 0
        self.tiledownloaded = 0
        self.tiledownloadskipped = 0
        self.tileskipped = 0
        self.tilemerged = 0
        self.tilemergedskipped = 0
        self.tiledownloaderror = 0

        self.force_download=force_download

        # just ensure that db UDP_TUNNEL
        db = TileSqlLiteDB(self.DBDIR)
        db.CloseDB()


    def UpdateTiles(self, tileserv, ti):
        cnt = 0
        self.joblist = list()
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                # stop processing of sea rander tiles with zoomlevel lower then nine
                # if tileserv.name == OpenSeaMap and ti.zoom < 9:
                #     break
                self.joblist.append([cnt, x, y, ti.zoom])
                cnt += 1

        # create download threads
        self.threadlist = list()

        for thread in range(10):
            self.threadlist.append(DownloadThread(self, self.force_download, self.DBDIR))

        # create download threads
        for threadrunner in self.threadlist:
            threadrunner.SetTileSrv(tileserv)
            threadrunner.start()

        # wait until all threads are ready
        for threadrunner in self.threadlist:
            threadrunner.join()

        return cnt

    def MergeTiles(self, TsOpenSeaMap, TSOpenStreetMap, ti):
        cnt = 0
        self.joblist = list()
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                z = ti.zoom
                self.joblist.append([cnt, x, y, z])
                cnt += 1

        # create download threads
        self.threadlist = list()

        for thread in range(10):
            self.threadlist.append(MergeThread(self, self.DBDIR))

        # create download threads
        for threadrunner in self.threadlist:
            threadrunner.SetTileSrv(TsOpenSeaMap, TSOpenStreetMap)
            threadrunner.start()

        # wait until all threads are ready
        for threadrunner in self.threadlist:
            threadrunner.join()

        # cleanup workspace
        for threadrunner in self.threadlist:
            threadrunner.CleanupWorkingDir()

        return cnt
