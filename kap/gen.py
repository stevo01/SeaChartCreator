#!/usr/bin/python3
# encoding: utf-8
'''
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
from kap.base import KapBase, point


class TileZoomInfo():

    def __init__(self, level, degree, res, scale):
        self.level = level  # zoom level
        self.degree = degree  #
        self.resolution = res  # resolution meter pro pixel
        self.scale = scale  # scale e.g. 25000 -> 1:25000 (85.2pixel/inch)


# source https://wiki.openstreetmap.org/wiki/Zoom_levels
zoominfo = {0: TileZoomInfo(0, 360, 156412, 500000000),
            1: TileZoomInfo(1, 180, 78206, 250000000),
            2: TileZoomInfo(2, 90, 39103, 150000000),
            3: TileZoomInfo(3, 45, 19551, 70000000),
            4: TileZoomInfo(4, 22.5, 9776, 35000000),
            5: TileZoomInfo(5, 11.25, 4888, 15000000),
            6: TileZoomInfo(6, 5.625, 2444, 10000000),
            7: TileZoomInfo(7, 2.813, 1222, 4000000),
            8: TileZoomInfo(8, 1.406, 610.984, 2000000),
            9: TileZoomInfo(9, 0.703, 305.492, 1000000),
            10: TileZoomInfo(10, 0.352, 152.746, 500000),
            11: TileZoomInfo(11, 0.176, 76.373, 250000),
            12: TileZoomInfo(12, 0.088, 38.187, 150000),
            13: TileZoomInfo(13, 0.044, 19.093, 70000),
            14: TileZoomInfo(14, 0.022, 9.547, 35000),
            15: TileZoomInfo(15, 0.011, 4.773, 15000),
            16: TileZoomInfo(16, 0.005, 2.387, 8000),
            17: TileZoomInfo(17, 0.003, 1.193, 4000),
            18: TileZoomInfo(18, 0.001, 0.596, 2000),
            19: TileZoomInfo(19, 0.0005, 0.298, 1000)}


class KapGen(KapBase):

    def __init__(self):
        KapBase.__init__(self)

    def GenHeader(self, ti):
        '''
        ti tileino
        '''
        self.SetHeaderFromTileInfo(ti)

        ret = "VER/2.0\n".format(self.VER)
        ret += "BSB/NA={},NU={}\n".format(self.NA, self.NU)
        ret += "    RA={},{},DU={}\n".format(self.Pixel_x, self.Pixel_y, self.DU)
        ret += "KNP/SC={},GD={},PR={},PP={}\n".format(self.SC, self.GD, self.PR, self.PP)
        ret += "    PI={},SP={},SK={},TA={}\n".format(self.PI, self.SP, self.SK, self.TA)
        ret += "    UN={},SD={}\n".format(self.UN, self.SD)
        ret += "    DX={},DY={}\n".format(self.DX, self.DY)
        ret += "CED/SE=2010,RE=01,ED=01/15/2010\n"
        ret += "OST/1\n"
        ret += "REF/1,{},{},{},{}\n".format(0, 0, self.PLY_SW.lat, self.PLY_SW.lon)
        ret += "REF/2,{},{},{},{}\n".format(0, self.Pixel_y, self.PLY_NW.lat, self.PLY_NW.lon)
        ret += "REF/3,{},{},{},{}\n".format(self.Pixel_x, self.Pixel_y, self.PLY_NE.lat, self.PLY_NE.lon)
        ret += "REF/4,{},{},{},{}\n".format(self.Pixel_x, 0, self.PLY_SE.lat, self.PLY_SE.lon)
        ret += "PLY/1,{},{}\n".format(self.PLY_SW.lat, self.PLY_SW.lon)
        ret += "PLY/2,{},{}\n".format(self.PLY_NW.lat, self.PLY_NW.lon)
        ret += "PLY/3,{},{}\n".format(self.PLY_NE.lat, self.PLY_NE.lon)
        ret += "PLY/4,{},{}\n".format(self.PLY_SE.lat, self.PLY_SE.lon)
        ret += "DTM/0,0\n"
        ret += "CPH/0\n"
        ret += "IFM/7\n"

        return ret

    def SetHeaderFromTileInfo(self, ti):

        self.PP = "UNKNOWL"  # Projektions Paramater
        self.PI = "0.0"  # Projection interval
        self.SP = "UNKNOWN"  #
        self.SK = "0.0"  # Skew angle
        self.TA = "90.0"  # text angle
        self.UN = "METER"
        self.SD = "MEAN SEA LEVEL"  # Sounding Datum

        x_pixel = (ti.xtile_nw - ti.xtile_se) * 256
        if(x_pixel < 0):
            x_pixel = x_pixel * -1

        y_pixel = (ti.ytile_nw - ti.ytile_se) * 256
        if(y_pixel < 0):
            y_pixel = y_pixel * -1

        self.VER = "0.2"

        # Pane name
        self.NA = ti.name

        # NU - Pane number. If chart is 123 and contains a plan A, the plan should be numbered 123_A
        self.NU = ""

        # RA - width, height - width and height of raster image data in pixels
        self.Pixel_y = "{}".format(y_pixel)
        self.Pixel_x = "{}".format(x_pixel)

        # SC - Scale e.g. 25000 means 1:25000
        self.SC = zoominfo[ti.zoom].scale

        # GD - Geodetic Datum e.g. WGS84 for us
        self.GD = "WGS84"

        # PR - Projection e.g. MERCATOR for us. Other known values are TRANSVERSE MERCATOR or
        # LAMBERT CONFORMAL CONIC or POLYCONIC. This must be one of those listed, as the value
        # determines how PP etc. are interpreted. Only MERCATOR and TRANSVERSE MERCATOR are supported by OpenCPN.
        self.PR = "MERCATOR"

        # DU - Drawing Units in pixels/inch (same as DPI resolution) e.g. 50, 150, 175, 254, 300
        self.DU = "85.2"

        # DX X resolution, distance (meters) covered by one pixel in X direction. OpenCPN ignores this and DY
        self.DX = zoominfo[ti.zoom].resolution

        # DY Y resolution, distance covered by one pixel in Y direction
        self.DY = zoominfo[ti.zoom].resolution

        # SW / south west
        self.PLY_SW = point("PLY,1,{},{}".format(ti.SE_lat, ti.NW_lon))

        # NW / north west
        self.PLY_NW = point("PLY,2,{},{}".format(ti.NW_lat, ti.NW_lon))

        # NE / north east
        self.PLY_NE = point("PLY,3,{},{}".format(ti.NW_lat, ti.SE_lon))

        # SE / south east
        self.PLY_SE = point("PLY,4,{},{}".format(ti.SE_lat, ti.SE_lon))
