#!/usr/bin/python3
# encoding: utf-8


import unittest
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.Helper import ChartInfo
from kap.analyse import kapfile
from kap.gen import KapGen


class TestAtlas(unittest.TestCase):

    def setUp(self):
        self.maps, self.name = ExtractMapsFromAtlas("./../sample/atlas/mobac/mobac-profile-testprj.xml")
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
        self.maps, self.name = ExtractMapsFromAtlas("./../sample/atlas/mobac/mobac-profile-testprj.xml")
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

        self.assertEqual(self.kapfile.Pixel_y, 2048)
        self.assertEqual(self.kapfile.Pixel_x, 1283)
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

        self.assertEqual(self.kapfile.Pixel_y, 768)
        self.assertEqual(self.kapfile.Pixel_x, 1540)
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

        self.assertEqual(self.kapfile.Pixel_y, 2048)
        self.assertEqual(self.kapfile.Pixel_x, 1283)
        self.assertEqual(self.kapfile.VER, "2.0")


if __name__ == "__main__":
    unittest.main()
