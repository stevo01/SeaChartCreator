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

import re
from kap.base import point, KapBase
from Utils.Helper import area
from Utils.Helper import ChartInfo


class kapfile(KapBase):

    def __init__(self, filename):
        self.filename = filename
        self.header = None
        self.AnalyseHeader()

    def GetKapHeader(self):

        self.header = ''

        # open file in binary mode for reading
        with open(self.filename, 'rb') as f:
            while(1 == 1):
                try:
                    text = f.readline().decode()
                    self.header += text
                except:
                    break

        return self.header

    def ParseElement(self, pattern):
        ret = ''
        res = re.search(pattern, self.header)
        if res:
            ret = res.group()
            if(ret[-1:] == '\r'):
                ret = ret[:-1]
            if(ret[-1:] == '\n'):
                ret = ret[:-1]

        return ret

    def _GetArea(self, Points):

        # search max lon
        lon_max = Points[0].lon
        lat_max = Points[0].lat
        lon_min = Points[0].lon
        lat_min = Points[0].lat

        for point in Points:

            if point.lon > lon_max:
                lon_max = point.lon

            if point.lat > lat_max:
                lat_max = point.lat

            if point.lon < lon_min:
                lon_min = point.lon

            if point.lat < lat_min:
                lat_min = point.lat

        for point in Points:

            # check if point is NW
            if(point.lat == lat_max and point.lon == lon_min):
                NW = point
            # check if point is NE
            elif(point.lat == lat_max and point.lon == lon_max):
                NE = point
            # check if point is NW
            elif(point.lat == lat_min and point.lon == lon_max):
                SE = point
            # check if point is NE
            elif(point.lat == lat_min and point.lon == lon_min):
                SW = point
            else:
                assert(0)

        return SW, NW, NE, SE

    def AnalyseHeader(self):

        kh = self.GetKapHeader()

        VER = self.ParseElement("VER\/.*")
        self.VER = VER[4:]

        # Pane name
        NA = self.ParseElement("NA=[^,\n]*")
        self.NA = NA[3:]

        # NU - Pane number. If chart is 123 and contains a plan A, the plan should be numbered 123_A
        NU = self.ParseElement("NU=[^,\n]*")
        self.NU = NU[3:]

        # RA - width, height - width and height of raster image data in pixels
        RA = self.ParseElement("RA=[\d]*,[\d]*")
        temp = RA[3:]
        temp = temp.split(',')
        self.Pixel_x = int(temp[0])
        self.Pixel_y = int(temp[1])

        # SC - Scale e.g. 25000 means 1:25000
        SC = self.ParseElement("SC=[^,\n]*")
        self.SC = SC[3:]

        # GD - Geodetic Datum e.g. WGS84 for us
        GD = self.ParseElement("GD=[^,\n]*")
        self.GD = self.ParseElement("GD=[^,\n]*")
        self.GD = GD[3:]

        # PR - Projection e.g. MERCATOR for us. Other known values are TRANSVERSE MERCATOR or
        # LAMBERT CONFORMAL CONIC or POLYCONIC. This must be one of those listed, as the value
        # determines how PP etc. are interpreted. Only MERCATOR and TRANSVERSE MERCATOR are supported by OpenCPN.
        PR = self.ParseElement("PR=[^,\n]*")
        self.PR = PR[3:]

        # DU - Drawing Units in pixels/inch (same as DPI resolution) e.g. 50, 150, 175, 254, 300
        DU = self.ParseElement("DU=[^,\n]*")
        self.DU = DU[3:]

        # DX X resolution, distance (meters) covered by one pixel in X direction. OpenCPN ignores this and DY
        DX = self.ParseElement("DX=[^,\n]*")
        self.DX = DX[3:]

        # DY Y resolution, distance covered by one pixel in Y direction
        DY = self.ParseElement("DY=[^,\n]*")
        self.DY = DY[3:]

        '''
        Geo-referencing, standard case - simple 4 corner chart, use the 4 corners, starting
        in the SW corner proceeding clockwise.  Format: x pix,y pix, lat, long. Lat & long in
        decimal degrees, to 8 decimals, where N lat and E long are positive.  One reason to use
        all 4 corners is to catch  skewed and warped charts, and calculate SK (8a), also to
        calculate a rotating angle for charts that are not properly aligned.
        If the chart is distorted or warped, use many REF points to let OpenCPN compute the 3rd
        order coefficients to correct the errors.

             NW   N   NE
                  |
             W--- +---E
                  |
             SW   S   SE

        lat / Breitengrad
        lon / Laengengrad

        example:
        Zugspitze Lat = 47° 25′ N oder Nord, Lon = 010° 59′ E oder Ost.

        '''

        # SW / south west
        REF1 = point(self.ParseElement("REF\/1.*[\d]*"))

        # NW / north west
        REF2 = point(self.ParseElement("REF\/2.*[\d]*"))

        # NE / north east
        REF3 = point(self.ParseElement("REF\/3.*[\d]*"))

        # SE / south east
        REF4 = point(self.ParseElement("REF\/4.*[\d]*"))

        # sort the Reference points here
        self.REF_SW, self.REF_NW, self.REF_NE, self.REF_SE = self._GetArea([REF1, REF2, REF3, REF4])

        # check coordinates
        assert(self.REF_NW.lat == self.REF_NE.lat)
        assert(self.REF_SW.lat == self.REF_SE.lat)
        assert(self.REF_NW.lon == self.REF_SW.lon)
        assert(self.REF_NE.lon == self.REF_SE.lon)

        ###############
        # SW / south west
        PLY1 = point(self.ParseElement("PLY\/1.*[\d]*"))

        # NW / north west
        PLY2 = point(self.ParseElement("PLY\/2.*[\d]*"))

        # NE / north east
        PLY3 = point(self.ParseElement("PLY\/3.*[\d]*"))

        # SE / south east
        PLY4 = point(self.ParseElement("PLY\/4.*[\d]*"))

        # sort the Reference points here
        self.PLY_SW, self.PLY_NW, self.PLY_NE, self.PLY_SE = self._GetArea([PLY1, PLY2, PLY3, PLY4])

        # check coordinates
        assert(self.PLY_NW.lat == self.PLY_NE.lat)
        assert(self.PLY_SW.lat == self.PLY_SE.lat)
        assert(self.PLY_NW.lon == self.PLY_SW.lon)
        assert(self.PLY_NE.lon == self.PLY_SE.lon)

        self.nroftiles_x = int(self.Pixel_x / 256)
        self.nroftiles_y = int(self.Pixel_y / 256)

        self.info()

    def GetTileInfo(self, zoom):
        ti = ChartInfo(area(float(self.REF_NW.lat) - 0.0001,
                            float(self.REF_NW.lon) + 0.0001,
                            float(self.REF_SE.lat) + 0.0001,
                            float(self.REF_SE.lon) - 0.0001,
                            self.NA, zoom))
        return ti

    def __str__(self):
        return self.filename
