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
        self.db = db
        self.TSOpenStreetMap = TileServer(OpenStreetMap, "http://a.tile.openstreetmap.org")
        self.TsOpenSeaMap = TileServer(OpenSeaMap, "http://tiles.openseamap.org/seamark")

        self.logger = getlog()

        self.tile = 0
        self.tiledownloaded = 0
        self.tiledownloadskipped = 0
        self.tileskipped = 0
        self.tilemerged = 0
        self.tiledownloaderror = 0

    def UpdateTiles(self, ti, update):
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                self._UpdateTile(ti.zoom, x, y, update)

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
            self.tiledownloaded += 1
        except urllib.error.HTTPError as err:
            self.logger.debug("HTTPError: {}".format(err.code))
            try:
                tile.date = err.headers['Date']
                ret = tile
                if ret is not None:
                    ret.updated = False
                self.tiledownloadskipped += 1
            except:
                self.tiledownloaderror += 1
                ret = tile
                if ret is not None:
                    ret.updated = False

        return ret

    def MergeTile(self, tile1, tile2):
        # store tile  in file
        filename_in1 = self._WorkingDirectory + MERGEDIR + 'file_openstreetmap.png'
        filename_in2 = self._WorkingDirectory + MERGEDIR + 'file_openseamap.png'
        filename_result1 = self._WorkingDirectory + MERGEDIR + 'file_merged.png'

        tile1.StoreFile(filename_in1)
        tile2.StoreFile(filename_in2)

        MergePictures(filename_in2,
                      filename_in1,
                      filename_result1)

        ret = TileInfo()
        ret.SetData(filename_result1)
        return ret

    def _UpdateTile(self, z, x, y, update):
        '''
        update - true  check if update of tile excists
               - false skip update if file exists
        '''
        tile_osm1 = self.db.GetTile(self.TSOpenStreetMap.name, z, x, y)
        if(tile_osm1 is not None) and(update is False):
            self.logger.debug("skip update of tile z={} x={} y={} from {}".format(z, x, y, self.TSOpenStreetMap.name))
            self.tileskipped += 1
        else:
            tile_osm1 = self._HttpLoadFile(self.TSOpenStreetMap, z, x, y, tile_osm1)
            if tile_osm1 is None:
                return
            if tile_osm1.updated is True:
                self.db.StoreTile(self.TSOpenStreetMap.name, tile_osm1, z, x, y)

        tile_osm2 = self.db.GetTile(self.TsOpenSeaMap.name, z, x, y)
        if(tile_osm2 is not None) and (update is False):
            self.logger.debug("skip update of tile z={} x={} y={} from {}".format(z, x, y, self.TsOpenSeaMap.name))
            self.tileskipped += 1
        else:
            tile_osm2 = self._HttpLoadFile(self.TsOpenSeaMap, z, x, y, tile_osm2)
            if tile_osm2 is None:
                return
            if tile_osm2.updated is True:
                self.db.StoreTile(self.TsOpenSeaMap.name, tile_osm2, z, x, y)

        tile_osm3 = self.db.GetTile(OpenSeaMapMerged, z, x, y)
        if (tile_osm1.updated is True) or (tile_osm2.updated is True) or (tile_osm3 is None):
            tile_merged = self.MergeTile(tile_osm1, tile_osm2)
            self.db.StoreTile(OpenSeaMapMerged, tile_merged, z, x, y)

            tile_osm1.updated = False
            self.db.StoreTile(self.TSOpenStreetMap.name, tile_osm1, z, x, y)

            tile_osm2.updated = False
            self.db.StoreTile(self.TsOpenSeaMap.name, tile_osm2, z, x, y)
            self.tilemerged += 1

        self.tile += 2
