#!/usr/bin/python3
# encoding: utf-8


from kap.base import KapBase, point
import math


SCALING_VALUE = 72  # pixel in inch


class KapGen(KapBase):

    def __init__(self):
        KapBase.__init__(self)

    def GenHeader(self, ti):
        '''
        ti tileino
        '''
        self.SetHeaderFromTileInfo(ti)

        '''
        VER/2.0
        CED/SE=1,RE=1,ED=27/05/2018
        BSB/NA=StorkowerGewaesser_1_16
            NU=UNKNOWN,RA=3850,7169,DU=254
        KNP/SC=14596,GD=WGS 84,PR=MERCATOR,PP=0.00
            PI=UNKNOWN,SP=UNKNOWN,SK=0.0,TA=90
            UN=METERS,SD=UNKNOWN,DX=1.46,DY=1.46
        REF/1,0,0,52.295042,13.996582
        REF/2,3849,0,52.295042,14.078979
        REF/3,3849,7168,52.200874,14.078979
        REF/4,0,7168,52.200874,13.996582
        PLY/1,52.295042,13.996582
        PLY/2,52.295042,14.078979
        PLY/3,52.200874,14.078979
        PLY/4,52.200874,13.996582
        DTM/0.000000,0.000000
        OST/1
        IFM/7
        '''

        ret = "VER/2.0\n".format(self.VER)
        ret += "CED/SE=1,RE=1,ED=01/15/2010\n"
        ret += "BSB/NA={}\n".format(self.NA)
        ret += "    NU={},RA={},{},DU={}\n".format(self.NU, self.Pixel_x, self.Pixel_y, self.DU)
        ret += "KNP/SC={:.0f},GD={:s},PR={:s},PP={:s}\n".format(self.SC, self.GD, self.PR, self.PP)
        ret += "    PI={},SP={},SK={},TA={}\n".format(self.PI, self.SP, self.SK, self.TA)
        ret += "    UN={:s},SD={:s},DX={:.2f},DY={:.2f}\n".format(self.UN, self.SD, self.DX, self.DY)

        '''
        # SW , unten links
        ret += "REF/1,{:d},{:d},{:.6f},{:.6f}\n".format(0, 0, self.PLY_SW.lat, self.PLY_SW.lon)

        # NW, oben Links
        ret += "REF/2,{:d},{:d},{:.6f},{:.6f}\n".format(0, self.Pixel_y, self.PLY_NW.lat, self.PLY_NW.lon)

        # NE, oben rechts
        ret += "REF/3,{:d},{:d},{:.6f},{:.6f}\n".format(self.Pixel_x, self.Pixel_y, self.PLY_NE.lat, self.PLY_NE.lon)

        # SE, unten rechts
        ret += "REF/4,{:d},{:d},{:.6f},{:.6f}\n".format(self.Pixel_x, 0, self.PLY_SE.lat, self.PLY_SE.lon)

        # SW , unten links
        ret += "PLY/1,{:.6f},{:.6f}\n".format(self.PLY_SW.lat, self.PLY_SW.lon)

        # NW, oben Links
        ret += "PLY/2,{:.6f},{:.6f}\n".format(self.PLY_NW.lat, self.PLY_NW.lon)

        # NE, oben rechts
        ret += "PLY/3,{:.6f},{:.6f}\n".format(self.PLY_NE.lat, self.PLY_NE.lon)

        # SE, unten rechts
        ret += "PLY/4,{:.6f},{:.6f}\n".format(self.PLY_SE.lat, self.PLY_SE.lon)
        '''

        # NW, oben Links
        ret += "REF/1,{:d},{:d},{:.6f},{:.6f}\n".format(0, 0, self.PLY_NW.lat, self.PLY_NW.lon)

        # NE, oben rechts
        ret += "REF/2,{:d},{:d},{:.6f},{:.6f}\n".format(self.Pixel_x, 0, self.PLY_NE.lat, self.PLY_NE.lon)

        # SE, unten rechts
        ret += "REF/3,{:d},{:d},{:.6f},{:.6f}\n".format(self.Pixel_x, self.Pixel_y, self.PLY_SE.lat, self.PLY_SE.lon)

        # SW , unten links
        ret += "REF/4,{:d},{:d},{:.6f},{:.6f}\n".format(0, self.Pixel_y, self.PLY_SW.lat, self.PLY_SW.lon)

        # NW, oben Links
        ret += "PLY/1,{:.6f},{:.6f}\n".format(self.PLY_NW.lat, self.PLY_NW.lon)

        # NE, oben rechts
        ret += "PLY/2,{:.6f},{:.6f}\n".format(self.PLY_NE.lat, self.PLY_NE.lon)

        # SE, unten rechts
        ret += "PLY/3,{:.6f},{:.6f}\n".format(self.PLY_SE.lat, self.PLY_SE.lon)

        # SW , unten links
        ret += "PLY/4,{:.6f},{:.6f}\n".format(self.PLY_SW.lat, self.PLY_SW.lon)

        ret += "DTM/0.000000,0.000000\n"
        #  ret += "CPH/0\n"
        ret += "OST/1\n"
        ret += "IFM/7\n"

        return ret

    def SetHeaderFromTileInfo(self, ti):

        self.PP = "0.00"  # Projektions Paramater
        self.PI = "UNKNOWN"  # Projection interval
        self.SP = "UNKNOWN"  #
        self.SK = "0.0"  # Skew angle
        self.TA = "90"  # text angle
        self.UN = "METERS"
        self.SD = "MEAN SEA LEVEL"  # Sounding Datum

        x_pixel = ti.x_cnt * 256
        y_pixel = ti.y_cnt * 256

        self.VER = "0.2"

        # Pane name
        self.NA = ti.name

        # NU - Pane number. If chart is 123 and contains a plan A, the plan should be numbered 123_A
        self.NU = "UNKNOWN"

        # RA - width, height - width and height of raster image data in pixels
        self.Pixel_y = y_pixel
        self.Pixel_x = x_pixel

        # DU - Drawing Units in pixels/inch (same as DPI resolution) e.g. 50, 150, 175, 254, 300
        self.DU = "{}".format(SCALING_VALUE)

        #  a = 2 ** 2

        resolution = 156543.03 * math.cos(math.radians(ti.NW_lat)) / (2 ** ti.zoom)
        scaling = SCALING_VALUE * 39.37 * resolution

        # SC - Scale e.g. 25000 means 1:25000
        self.SC = scaling

        # DX X resolution, distance (meters) covered by one pixel in X direction. OpenCPN ignores this and DY
        self.DX = resolution

        # DY Y resolution, distance covered by one pixel in Y direction
        self.DY = resolution

        # GD - Geodetic Datum e.g. WGS84 for us
        self.GD = "WGS 84"

        # PR - Projection e.g. MERCATOR for us. Other known values are TRANSVERSE MERCATOR or
        # LAMBERT CONFORMAL CONIC or POLYCONIC. This must be one of those listed, as the value
        # determines how PP etc. are interpreted. Only MERCATOR and TRANSVERSE MERCATOR are supported by OpenCPN.
        self.PR = "MERCATOR"

        # SW / south west
        self.PLY_SW = point("PLY,1,{},{}".format(ti.SE_lat, ti.NW_lon))

        # NW / north west
        self.PLY_NW = point("PLY,2,{},{}".format(ti.NW_lat, ti.NW_lon))

        # NE / north east
        self.PLY_NE = point("PLY,3,{},{}".format(ti.NW_lat, ti.SE_lon))

        # SE / south east
        self.PLY_SE = point("PLY,4,{},{}".format(ti.SE_lat, ti.SE_lon))
