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

import urllib.request


from tile.Info import TileInfo
from Utils.glog import getlog
from Utils.ProcessCmd import MergePictures
from Utils import __app_identifier__
import time
import locale
from random import *

MERGEDIR = 'Merge/'

OpenSeaMapMerged = 'OpenSeaMapMerged'
OpenStreetMap = 'OpenStreetMap'
OpenSeaMap = 'OpenSeaMap'

TileSourceList = [OpenSeaMap, OpenStreetMap, OpenSeaMapMerged]


class TileServer():

    def __init__(self, name, url):
        self.name = name
        self.url = url


class TileManager(object):
    '''
    classdocs
    '''

    def __init__(self, WorkingDirectory, db):
        '''
        Constructor
        '''
        self._WorkingDirectory = WorkingDirectory
        self._WorkingDirMerge = WorkingDirectory + "{}".format(randint(1, 0xffffffff))

        self.db = db
        self.logger = getlog()

        self.tile = 0
        self.tiledownloaded = 0
        self.tiledownloadskipped = 0
        self.tileskipped = 0
        self.tilemerged = 0
        self.tilemergedskipped = 0
        self.tiledownloaderror = 0

    # load single file with http protocol
    def _HttpLoadFile(self, ts, z, x, y, tile=None):

        ret = None

        url = "{}/{}/{}/{}.png".format(ts.url, z, x, y)

        # set user agent to meet the tile usage policy
        # https://operations.osmfoundation.org/policies/tiles/
        self.logger.debug("HttpLoadFile open {}".format(url))

        req = urllib.request.Request(url, data=None, headers={'User-Agent': __app_identifier__})

        if(tile is not None):
            req.add_header('If-None-Match', tile.etag)

        try:
            f = urllib.request.urlopen(req)
            data = f.read()
            date = f.headers['Date']
            lastmodified = f.headers['Last-Modified']
            etag = f.headers['ETag']
            ret = TileInfo(data, etag, date, lastmodified)
            ret.updated = True
            ret.date_updated = True
            self.tiledownloaded += 1
        except urllib.error.HTTPError as err:
            self.logger.debug("HTTPError: {}".format(err.code))
            try:
                tile.date = err.headers['Date']
                ret = tile
                ret.date_updated = True
                if ret is not None:
                    ret.updated = False
                self.tiledownloadskipped += 1
            except Exception as e:
                self.logger.debug("Exception: {}".format(e))
                self.tiledownloaderror += 1
                ret = tile
                if ret is not None:
                    ret.updated = False

        return ret

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

    '''
     @brief This method returns
            - True if Tile requires update
            - False if Tile requires no update

     @param tile - tile
     @param max_timespan - max time span (in hours)
    '''
    def CheckTimespan(self, tile, max_timespan):
        last_update = tile.date  # sample format Thu, 18 Apr 2019 07:01:25 GMT
        retv = True

        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except Exception as e:
            print('Error:', e)

        # https://www.journaldev.com/23365/python-string-to-datetime-strptime
        # %a Weekday as locale’s abbreviated name.                / Sun, Mon, …, Sat (en_US)
        # %d    Day of the month as a zero-padded decimal number. / 01, 02, …, 31
        # %b    Month as locale’s abbreviated name.               / Jan, Feb, …, Dec (en_US)
        # %H    Hour (24-hour clock) as a zero-padded decimal number.    01, 02, … , 23
        # %M    Minute as a zero-padded decimal number.    01, 02, … , 59
        # %S    Second as a zero-padded decimal number.    01, 02, … , 59
        # %m Month as a zero-padded decimal number.    01, 02 … 12
        # %Z    Time zone name (empty string if the object is naive).    (empty), UTC, IST, CST

        try:
            last_update = time.strptime(last_update, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError as e:
            print('ValueError:', e)
            return True

        diff = (time.time() - time.mktime(last_update)) / 3600

        if diff < max_timespan:
            retv = False
        else:
            retv = True

        return retv

    def UpdateTiles(self, tileserv, ti, force_download):
        cnt = 0
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                z = ti.zoom
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
