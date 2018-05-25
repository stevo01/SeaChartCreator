#!/usr/bin/python3
# encoding: utf-8
'''
several helper functions

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
from ExternalUtils.Conversions import deg2num, num2deg
import os


# storage for coordinates for a single point
class coordinate(object):

    def __init__(self, lat, lon):
        self.lon = lon
        self.lat = lat

    def __str__(self):
        out = "lon={}, lat={}".format(self.lon, self.lat)
        return out


# storage for coordinates for a given area
class area(object):

    # lat0 lon0 is a left,top     (NW) point
    # lat1 lon1 is a right,bottom (SE) point
    def __init__(self, NW_lat, NW_lon, SE_lat, SE_lon, name, zoom):
        self.NW = coordinate(NW_lat, NW_lon)
        self.SW = coordinate(SE_lat, NW_lon)
        self.NE = coordinate(NW_lat, SE_lon)
        self.SE = coordinate(SE_lat, SE_lon)
        self.zoom = zoom
        self.name = name

    def __str__(self):
        out = "{}\n".format(self.name)
        out += "NW lat={}, lon={}\n".format(self.NW.lat, self.NW.lon)
        out += "SW lat={}, lon={}\n".format(self.SW.lat, self.SW.lon)
        out += "NE lat={}, lon={}\n".format(self.NE.lat, self.NE.lon)
        out += "SE lat={}, lon={}  ".format(self.SE.lat, self.SE.lon)
        return out


# storege for tile informations for a given area
class ChartInfo(object):

    def __init__(self, area_info):
        self.xtile_nw, self.ytile_nw = deg2num(area_info.NW.lat, area_info.NW.lon, area_info.zoom)
        self.xtile_se, self.ytile_se = deg2num(area_info.SE.lat, area_info.SE.lon, area_info.zoom)
        self.x_cnt = self.xtile_se - self.xtile_nw + 1
        self.y_cnt = self.ytile_se - self.ytile_nw + 1
        self.nr_of_tiles = self.x_cnt * self.y_cnt
        self.NW_lat, self.NW_lon = num2deg(self.xtile_nw, self.ytile_nw, area_info.zoom)
        self.SE_lat, self.SE_lon = num2deg(self.xtile_se + 1, self.ytile_se + 1, area_info.zoom)
        self.name = area_info.name
        self.zoom = area_info.zoom

    def __str__(self):
        ret = "name  {}\n".format(self.name)
        ret += "zoom level {}\n".format(self.zoom)
        ret += "NW lat : {} lon: {}\n".format(self.NW_lat, self.NW_lon)
        ret += "SE lat : {} lon: {}\n".format(self.SE_lat, self.SE_lon)
        ret += "number of tiles in x direction: {}\n".format(self.x_cnt)
        ret += "number of tiles in y direction: {}\n".format(self.y_cnt)
        ret += "number of tiles = {}\n".format(self.nr_of_tiles)
        ret += "Sum {} x {} = {} MB\n".format(self.x_cnt * 256, self.y_cnt * 256, self.x_cnt * 256 * self.y_cnt * 256 * 8 / (1024 * 1024))

        return ret


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
