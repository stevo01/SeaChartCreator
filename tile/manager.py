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

from tile.Info import TileInfo
from Utils.glog import getlog
from Utils.ProcessCmd import MergePictures
from random import *
from tile.DownloadThread import DownloadThread
from tile.sqllitedb import TileSqlLiteDB

MERGEDIR = 'Merge/'

OpenSeaMapMerged = 'OpenSeaMapMerged'
OpenStreetMap = 'OpenStreetMap'
OpenSeaMap = 'OpenSeaMap'


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
        self._WorkingDirMerge = WorkingDirectory + "{}".format(randint(1, 0xffffffff))

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

        # just enshure that db excists
        db = TileSqlLiteDB(self.DBDIR)
        db.CloseDB()

    def MergeTile(self, tile1, tile2):
        # store tile  in file
        filename_in1 = self._WorkingDirMerge + "/" + 'file_openstreetmap.png'
        filename_in2 = self._WorkingDirMerge + "/" + 'file_openseamap.png'
        filename_result1 = self._WorkingDirMerge + "/" + 'file_merged.png'

        tile1.StoreFile(filename_in1)
        tile2.StoreFile(filename_in2)

        MergePictures(filename_in2,
                      filename_in1,
                      filename_result1)

        ret = TileInfo()
        ret.SetData(filename_result1)

        return ret

    def UpdateTiles(self, tileserv, ti):
        cnt = 0
        self.joblist = list()
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                z = ti.zoom
                self.joblist.append([cnt, x, y, z])
                cnt += 1

        # create download threads
        self.threadlist = list()

        for thread in range (10):
            self.threadlist.append(DownloadThread(self, self.force_download, self.DBDIR ))

        # create download threads
        for threadrunner in self.threadlist:
            threadrunner.SetTileSrv(tileserv)
            threadrunner.start()

        # wait until all threads are ready
        for threadrunner in self.threadlist:
            threadrunner.join()

        print("ready")


        '''
                tile_osm2 = self.db.GetTile(tileserv.name, z, x, y)

                # skip download if tile is available
                if(tile_osm2 is not None) and (force_download is False):
                    self.logger.debug("skip update of tile z={} x={} y={} from {}".format(z, x, y, tileserv.name))
                    self.tileskipped += 1
                # skip download if tile is newer the 7 days
                elif(tile_osm2 is not None) and (self.CheckTimespan(tile_osm2, 7 * 24) is False):
                    self.logger.debug("skip update of tile z={} x={} y={} from {}".format(z, x, y, tileserv.name))
                    self.tileskipped += 1
                else:
                    tile_osm2 = self._HttpLoadFile(tileserv, z, x, y, tile_osm2)
                    if tile_osm2 is None:
                        return
                    if (tile_osm2.updated is True) or (tile_osm2.date_updated is True):
                        self.db.StoreTile(tileserv.name, tile_osm2, z, x, y)
                self.tile += 1
                cnt += 1
        '''
        return cnt

    def MergeTiles(self, tileserv1, tileserv2, ti):
        cnt = 0
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                z = ti.zoom
                tile_osm1 = self.db.GetTile(tileserv1.name, z, x, y)
                tile_osm2 = self.db.GetTile(tileserv2.name, z, x, y)
                tile_osm3 = self.db.GetTile(OpenSeaMapMerged, z, x, y)
                if (tile_osm1.updated is not 0) or (tile_osm2.updated is not 0) or (tile_osm3 is None):
                    tile_merged = self.MergeTile(tile_osm1, tile_osm2)
                    self.db.StoreTile(OpenSeaMapMerged, tile_merged, z, x, y)

                    tile_osm1.updated = False
                    self.db.StoreTile(tileserv1.name, tile_osm1, z, x, y)

                    tile_osm2.updated = False
                    self.db.StoreTile(tileserv2.name, tile_osm2, z, x, y)
                    self.tilemerged += 1
                else:
                    self.tilemergedskipped += 1
                cnt += 1
        return cnt
