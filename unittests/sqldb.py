#!/usr/bin/python3
# encoding: utf-8


import unittest
from atlas.generator import RemoveDir
from tile.sqllitedb import TileSqlLiteDB, OpenStreetMap
from Utils.glog import initlog, getlog
from tile.Info import TileInfo


class TestSQLliteDB(unittest.TestCase):

    def setUp(self):
        initlog('bTestSQLliteDB')
        self.logger = getlog()
        RemoveDir('./../sample/tilestoresql/')
        self.sqldb = TileSqlLiteDB('./../sample/tilestoresql/')

    def tearDown(self):
        pass

    def test_Tile_001(self):
        '''
        write tile and read it back
        '''

        tile1 = TileInfo(bytes([0x13, 0x00, 0x00, 0x00, 0x08, 0x00]),
                         None,
                         None,
                         None)

        # write tile to sqllite db
        self.sqldb.StoreTile(OpenStreetMap, tile1, 16, 34997, 21449)
        self.sqldb.StoreTile(OpenStreetMap, tile1, 1, 2, 10)
        self.sqldb.StoreTile(OpenStreetMap, tile1, 1, 2, 11)

        # read tile back from sqllite db
        tile2 = self.sqldb.GetTile(OpenStreetMap, 16, 34997, 21449)

        # compare tile
        self.assertEqual(tile1.data, tile2.data)
        self.assertEqual(tile1.date, tile2.date)
        self.assertEqual(tile1.etag, tile2.etag)
        self.assertEqual(tile1.lastmodified, tile2.lastmodified)
        self.assertEqual(tile1.md5, tile2.md5)
        self.assertEqual(tile1.updated, tile2.updated)

    def test_Tile_002(self):
        '''
        update tile
        '''

        tile1 = TileInfo(bytes([0x13, 0x00, 0x00, 0x00, 0x08, 0x00]),
                         None,
                         None,
                         None)

        # write tile to sqllite db
        self.sqldb.StoreTile(OpenStreetMap, tile1, 1, 2, 23)

        # read tile back from sqllite db
        tile2 = self.sqldb.GetTile(OpenStreetMap, 1, 2, 23)

        # compare tile
        self.assertEqual(tile1.data, tile2.data)
        self.assertEqual(tile1.date, tile2.date)
        self.assertEqual(tile1.etag, tile2.etag)
        self.assertEqual(tile1.lastmodified, tile2.lastmodified)
        self.assertEqual(tile1.md5, tile2.md5)
        self.assertEqual(tile1.updated, tile2.updated)

        # write tile to sqllite db
        tile1.etag = '123456789'
        tile1.updated = True
        self.sqldb.StoreTile(OpenStreetMap, tile1, 1, 2, 23)

        # read tile back from sqllite db
        tile2 = self.sqldb.GetTile(OpenStreetMap, 1, 2, 23)

        # compare tile
        self.assertEqual(tile1.data, tile2.data)
        self.assertEqual(tile1.date, tile2.date)
        self.assertEqual("123456789", tile2.etag)
        self.assertEqual(tile1.lastmodified, tile2.lastmodified)
        self.assertEqual(tile1.md5, tile2.md5)
        self.assertEqual(True, tile2.updated)


if __name__ == "__main__":
    unittest.main()
