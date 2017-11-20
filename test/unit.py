#!/usr/bin/env python
# encoding: utf-8

'''
@brief:  unit tests for 
@author: steffen@volkmann.com

Copyright (C) 2017  Steffen Volkmann

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110, USA

'''
import unittest
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.Helper import TileInfo


class TestAtlas(unittest.TestCase):

    def setUp(self):
        self.maps = ExtractMapsFromAtlas("./../sample/atlas/mobac-profile-testprj.xml")
        self.ti = TileInfo(self.maps[0])
        pass

    def tearDown(self):
        pass

    def testTileInfo(self):
        self.assertEqual(self.ti.nr_of_tiles,18)
        self.assertEqual(self.ti.x_cnt,6)
        self.assertEqual(self.ti.y_cnt,3)
        self.assertEqual(self.ti.xtile_se, 35166)
        self.assertEqual(self.ti.xtile_nw, 35161)
        self.assertEqual(self.ti.ytile_nw, 21523)
        self.assertEqual(self.ti.ytile_se, 21525)
        self.assertEqual(self.ti.zoom, 16)
        self.assertEqual(self.ti.name, "Kleiner_Wannsee_16")
   
    def testMaps(self):
        self.assertEqual(self.maps[0].zoom, 16)
        self.assertEqual(self.maps[0].name, "Kleiner_Wannsee_16")
              
    def testTileInfoPosNW(self):
        self.assertAlmostEqual(self.ti.NW_lat , 52.41917 , 4)
        self.assertAlmostEqual(self.ti.NW_lon , 13.14514 , 4)
       
    def testTileInfoPosSE(self):
        self.assertAlmostEqual(self.ti.SE_lat , 52.4091 , 4)
        self.assertAlmostEqual(self.ti.SE_lon , 13.1781 , 4)    
        pass
    

if __name__ == "__main__":
    unittest.main()