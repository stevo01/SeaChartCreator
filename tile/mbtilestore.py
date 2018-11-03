#!/usr/bin/python3
# encoding: utf-8

'''

Copyright (C) 2017  Steffen Volkmann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
from Utils.Helper import ensure_dir
from Utils.glog import getlog
import os
import sqlite3

FILENAMESQLLITEDB = "tilestore.sqllite"


class MBTileStore(object):

    '''
        https://github.com/mapbox/mbtiles-spec
        https://github.com/mapbox/mbtiles-spec/wiki/Implementations
        http://wiki.osgeo.org/wiki/Tile_Map_Service_Specification
    '''

    def __init__(self, FilenameDB):

        ensure_dir(FilenameDB)
        self.logger = getlog()
        self.FilenameDB = FilenameDB

        # check if db excists
        if os.path.isfile(FilenameDB) is False:
            self.InitDB()
        else:
            self.con = sqlite3.connect(self.FilenameDB)
            self.cur = self.con.cursor()

        self.writecnt = 0

    def InitDB(self):
        self.con = sqlite3.connect(self.FilenameDB)
        self.cur = self.con.cursor()

        self.cur.execute("""CREATE TABLE metadata (name text, value text);""")
        self.cur.execute("""CREATE TABLE tiles (zoom_level integer, tile_column integer, tile_row integer, tile_data blob);""")
        self.cur.execute("""CREATE UNIQUE INDEX tile_index on tiles (zoom_level, tile_column, tile_row);""")

    def CloseDB(self):
        self.con.commit()
        self.con.close()

    def SetMetadata(self, name, value):

        sqlcmd = 'INSERT OR REPLACE INTO metadata'
        sqlcmd += '(name, value)'
        sqlcmd += 'values (?,?)'

        try:
            self.cur.execute(sqlcmd, (name, value))
        except Exception as e:
            self.logger.error("Error Execute SQL Statement:{}".format(sqlcmd))
            self.logger.exception(e)

    def StoreTile(self, tile, z, x, y):

        '''
        LONG=13.37771496361961;
        LAT=52.51628011262304;
        ZOOM=17;
        TILE_X=70406;
        TILE_Y=42987;
        TILE_Y_TMS=88084;
        '''

        # convert y to TMS system
        y = ((2.0**z) - 1) - y

        sqlcmd = 'INSERT OR REPLACE INTO tiles'
        sqlcmd += '(zoom_level, tile_column, tile_row, tile_data)'
        sqlcmd += 'values (?,?,?,?)'

        try:
            self.cur.execute(sqlcmd, (z, x, y, sqlite3.Binary(tile.data)))
        except Exception as e:
            self.logger.error("Error Execute SQL Statement:{}".format(sqlcmd))
            self.logger.exception(e)

        self.writecnt += 1
        if self.writecnt >= 100:
            self.con.commit()
            self.writecnt = 0
