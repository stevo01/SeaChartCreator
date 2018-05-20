'''
Created on 20.05.2018

@author: stevo
'''
import urllib.request
from seamapcreator import __app_identifier__
from tile.Info import TileInfo


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
        self.TSOpenStreetMap = TileServer("OpenStreetMap", "http://a.tile.openstreetmap.org")
        self.TsOpenSeaMap = TileServer("OpenSeaMap", "http://tiles.openseamap.org/seamark")

    def UpdateTiles(self, ti):
        for y in range(ti.ytile_nw, ti.ytile_se):
            for x in range(ti.xtile_nw, ti.xtile_se):
                self._UpdateTile(ti.zoom, x, y)

    # load singlke file with http protocol
    def _HttpLoadFile(self, ts, z , x, y):

        FileNameOSM = self._WorkingDirectory + "test.png"
        url = "{}/{}/{}/{}.png".format(ts.url, z, x, y) 

        # set user agent to meet the tile usage policy
        # https://operations.osmfoundation.org/policies/tiles/
        print("HttpLoadFile open {}".format(url))
        req = urllib.request.Request(url, data=None, headers={'User-Agent':  __app_identifier__})
        f = urllib.request.urlopen(req)
        data = f.read()
        date = None
        etag = f.headers['ETag']
        ret = TileInfo(data, etag, date)
        return ret

    def _UpdateTile(self, z, x, y):
        tile_osm1 = self.db.GetTile(self.TSOpenStreetMap.name, z , x, y)
        if(tile_osm1 is None):
            tile = self._HttpLoadFile(self.TSOpenStreetMap, z, x, y)
            self.db.StoreTile(self.TSOpenStreetMap.name, tile, z , x, y)


        tile_osm1 = self.db.GetTile(self.TsOpenSeaMap.name, z , x, y)
        if(tile_osm1 is None):
            tile = self._HttpLoadFile(self.TsOpenSeaMap, z, x, y)
            self.db.StoreTile(self.TsOpenSeaMap.name, tile, z , x, y)
