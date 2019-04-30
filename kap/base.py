#!/usr/bin/python3
# encoding: utf-8


class point():

    def __init__(self, Ref):
        '''
        Ref:
          Format: x pix,y pix, lat, long. Lat & long in decimal degrees, to 8 decimals, where N lat and E long are positive.
        '''
        # check data
        temp = Ref[4:]
        temp = temp.split(',')

        self.number = temp[0]

        if(Ref[:3] == "REF"):
            self.pos_x = int(temp[1])
            self.pos_y = int(temp[2])
            self.lat = float(temp[3])
            self.lon = float(temp[4])
        if(Ref[:3] == "PLY"):
            self.pos_x = 0
            self.pos_y = 0
            self.lat = float(temp[1])
            self.lon = float(temp[2])

    def __str__(self):
        ret = "lat={} lon={}".format(self.lat, self.lon)
        return ret


class KapBase():

    def __init__(self):
        self.VER = None
        self.NA = None
        self.NU = None
        self.Pixel_y = None
        self.Pixel_x = None
        self.SC = None
        self.GD = None
        self.PR = None
        self.DU = None
        self.DX = None
        self.DY = None

        self.REF_SW = None
        self.REF_NW = None
        self.REF_NE = None
        self.REF_SE = None

        self.PLY_SW = None
        self.PLY_NW = None
        self.PLY_NE = None
        self.PLY_SE = None

        self.nroftiles_x = None
        self.nroftiles_y = None

    def info(self):
        print("Version        : {}".format(self.VER))
        print("Name           : {}".format(self.NA))
        print("NU             : {}".format(self.NU))
        print("RA Hight       : {} px".format(self.Pixel_y))
        print("RA Width       : {} px".format(self.Pixel_x))
        print("Scale          : {}".format(self.SC))
        print("Geodetic Datum : {}".format(self.GD))
        print("Projection     : {}".format(self.PR))
        print("Draft Units    : {}".format(self.DU))

        print("X resolution   : {}".format(self.DX))
        print("Y resolution   : {}".format(self.DY))
        print("Referenz Pos.  :")
        print("SW {}".format(self.REF_SW))
        print("NW {}".format(self.REF_NW))
        print("NE {}".format(self.REF_NE))
        print("SE {}".format(self.REF_SE))

        # print("distance x = {} m".format( dist_x ))
        # print("distance y = {} m".format( dist_y ))
        # print("distance d = {} m".format( dist_diagonale ))

        print("Tiles x : {}".format(self.nroftiles_x))
        print("Tiles y : {}".format(self.nroftiles_y))
