#!/usr/bin/python33
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
from Utils.Helper import ChartInfo
from kap.analyse import kapfile
from kap.gen import KapGen


class TestAtlas(unittest.TestCase):

    def setUp(self):
        self.maps, self.name = ExtractMapsFromAtlas("./../sample/atlas/mobac-profile-testprj.xml")
        self.ti = ChartInfo(self.maps[0])
        pass

    def tearDown(self):
        pass

    def testTileInfo(self):
        self.assertEqual(self.ti.nr_of_tiles, 18)
        self.assertEqual(self.ti.x_cnt, 6)
        self.assertEqual(self.ti.y_cnt, 3)
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
        self.assertAlmostEqual(self.ti.NW_lat, 52.41917, 4)
        self.assertAlmostEqual(self.ti.NW_lon, 13.14514, 4)

    def testTileInfoPosSE(self):
        self.assertAlmostEqual(self.ti.SE_lat, 52.4091, 4)
        self.assertAlmostEqual(self.ti.SE_lon, 13.1781, 4)
        pass


class TestKapHederGen(unittest.TestCase):

    def setUp(self):
        self.maps, self.name = ExtractMapsFromAtlas("./../sample/atlas/mobac-profile-testprj.xml")
        self.ti = ChartInfo(self.maps[0])
        pass

    def tearDown(self):
        pass

    def test_GenHeader(self):
        gen = KapGen()
        header = gen.GenHeader(self.ti)
        print(header)
        self.assertEqual(1, 1)


class TestKapInfo(unittest.TestCase):

    def setUp(self):
        self.kapfile = kapfile("./../sample/kap/map/map.kap")

        pass

    def tearDown(self):
        pass

    def testTileInfo(self):
        self.assertEqual(self.kapfile.VER, "2.0")
        self.assertEqual(self.kapfile.NA, "")
        self.assertEqual(self.kapfile.DU, "254")
        self.assertEqual(self.kapfile.DX, "1.45")
        self.assertEqual(self.kapfile.DY, "1.45")
        self.assertEqual(self.kapfile.GD, "WGS 84")
        self.assertEqual(self.kapfile.PR, "MERCATOR")
        self.assertEqual(self.kapfile.SC, "14537")

        self.assertEqual(self.kapfile.REF_NE.lat, 52.445966)
        self.assertEqual(self.kapfile.REF_NE.lon, 13.183594)

        self.assertEqual(self.kapfile.REF_NW.lat, 52.445966)
        self.assertEqual(self.kapfile.REF_NW.lon, 13.156128)

        self.assertEqual(self.kapfile.REF_SE.lat, 52.419173)
        self.assertEqual(self.kapfile.REF_SE.lon, 13.183594)

        self.assertEqual(self.kapfile.REF_SW.lat, 52.419173)
        self.assertEqual(self.kapfile.REF_SW.lon, 13.156128)

        self.assertEqual(self.kapfile.Pixel_x, 2048)
        self.assertEqual(self.kapfile.Pixel_y, 1283)
        self.assertEqual(self.kapfile.VER, "2.0")


class TestKapInfo_KleinerWannsee(unittest.TestCase):

    def setUp(self):
        self.kapfile = kapfile("./../sample/kap/Kleiner_Wannsee_16/map.kap")
        pass

    def tearDown(self):
        pass

    def testTileInfo(self):
        self.assertEqual(self.kapfile.VER, "2.0")
        self.assertEqual(self.kapfile.NA, "Kleiner_Wannsee_16")
        self.assertEqual(self.kapfile.DU, "254")
        self.assertEqual(self.kapfile.DX, "1.45")
        self.assertEqual(self.kapfile.DY, "1.45")
        self.assertEqual(self.kapfile.GD, "WGS 84")
        self.assertEqual(self.kapfile.PR, "MERCATOR")
        self.assertEqual(self.kapfile.SC, "14543")

        self.assertEqual(self.kapfile.REF_NE.lat, 52.419173)  # 52.419173 != 52.445966
        self.assertEqual(self.kapfile.REF_NE.lon, 13.178101)  # 13.178101 != 13.183594

        self.assertEqual(self.kapfile.REF_NW.lat, 52.419173)
        self.assertEqual(self.kapfile.REF_NW.lon, 13.145142)

        self.assertEqual(self.kapfile.REF_SE.lat, 52.409121)
        self.assertEqual(self.kapfile.REF_SE.lon, 13.178101)

        self.assertEqual(self.kapfile.REF_SW.lat, 52.409121)
        self.assertEqual(self.kapfile.REF_SW.lon, 13.145142)

        self.assertEqual(self.kapfile.Pixel_x, 768)
        self.assertEqual(self.kapfile.Pixel_y, 1540)
        self.assertEqual(self.kapfile.VER, "2.0")


class TestKapInfo_GrosserWannsee(unittest.TestCase):

    def setUp(self):
        self.kapfile = kapfile("./../sample/kap/Grosser_Wannsee_16/map.kap")

        pass

    def tearDown(self):
        pass

    def testTileInfo(self):
        self.assertEqual(self.kapfile.VER, "2.0")
        self.assertEqual(self.kapfile.NA, "Grosser_Wannsee_16")
        self.assertEqual(self.kapfile.DU, "254")
        self.assertEqual(self.kapfile.DX, "1.45")
        self.assertEqual(self.kapfile.DY, "1.45")
        self.assertEqual(self.kapfile.GD, "WGS 84")
        self.assertEqual(self.kapfile.PR, "MERCATOR")
        self.assertEqual(self.kapfile.SC, "14537")

        self.assertEqual(self.kapfile.REF_NE.lat, 52.445966)
        self.assertEqual(self.kapfile.REF_NE.lon, 13.183594)

        self.assertEqual(self.kapfile.REF_NW.lat, 52.445966)
        self.assertEqual(self.kapfile.REF_NW.lon, 13.156128)

        self.assertEqual(self.kapfile.REF_SE.lat, 52.419173)
        self.assertEqual(self.kapfile.REF_SE.lon, 13.183594)

        self.assertEqual(self.kapfile.REF_SW.lat, 52.419173)
        self.assertEqual(self.kapfile.REF_SW.lon, 13.156128)

        self.assertEqual(self.kapfile.Pixel_x, 2048)
        self.assertEqual(self.kapfile.Pixel_y, 1283)
        self.assertEqual(self.kapfile.VER, "2.0")


if __name__ == "__main__":
    unittest.main()
