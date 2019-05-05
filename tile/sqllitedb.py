#!/usr/bin/python3
# encoding: utf-8


from Utils.Helper import ensure_dir
from Utils.glog import getlog
from tile.Info import TileInfo
import os
import sqlite3
from _sqlite3 import OperationalError
import time

OpenSeaMapMerged = 'OpenSeaMapMerged'
OpenStreetMap = 'OpenStreetMap'
OpenSeaMap = 'OpenSeaMap'

TileSourceList = [OpenSeaMap, OpenStreetMap, OpenSeaMapMerged]

FILENAMESQLLITEDB = "tilestore.sqllite"


class TileSqlLiteDB(object):

    def __init__(self, workspace):
        ensure_dir(workspace)
        self.ws = workspace
        self.logger = getlog()

        self.FilenameDB = workspace + FILENAMESQLLITEDB

        # check if db excists
        if os.path.isfile(self.FilenameDB) is False:
            self.InitDB()
        else:
            self.con = sqlite3.connect(self.FilenameDB)
            self.cur = self.con.cursor()
            self.cur.execute("""PRAGMA journal_mode = WAL""")
            self.cur.execute("""PRAGMA synchronous = NORMAL""")

        self.writecnt = 0

    def InitDB(self):
        self.con = sqlite3.connect(self.FilenameDB)
        self.cur = self.con.cursor()

        for tablename in TileSourceList:
            self.cur.execute("""
            create table {} (
                z integer,
                x integer,
                y integer,
                data blob,
                date text,
                lastmodified text,
                etag text,
                updated boolean,
                md5 text
                );
                """.format(tablename))

            self.cur.execute("""create unique index {}_index on {}
                           (z, x, y);""".format(tablename, tablename))

    def CloseDB(self):
        self.con.commit()
        self.con.close()

    def StoreTile(self, tablename, tile, z, x, y):

        sqlcmd = 'INSERT OR REPLACE INTO {} '.format(tablename)
        sqlcmd += '(z, x, y, data, date, lastmodified, etag, updated, md5)'
        sqlcmd += 'values (?,?,?,?,?,?,?,?,?)'

        retry_cnt = 0
        while retry_cnt < 100:
            try:
                self.cur.execute(sqlcmd, (z, x, y, sqlite3.Binary(tile.data), tile.date, tile.lastmodified, tile.etag, tile.updated, tile.md5))
                break
            except OperationalError as e:
                print("Error Execute SQL Statement:{}".format(sqlcmd))
                print(e.args[0])
                self.logger.error("Error Execute SQL Statement:{}".format(sqlcmd))
                self.logger.error(e.args[0])
                time.sleep(0.1) 
                retry_cnt += 1
            except Exception as e:
                self.logger.error("Error Execute SQL Statement:{}".format(sqlcmd))
                self.logger.exception(e)
                break
        if retry_cnt >= 99:
            assert(False)

        self.con.commit()

        #if(self.writecnt > 1000):
        #    self.con.commit()
        #    self.writecnt=0
        #else:
        #    self.writecnt += 1


    def GetTile(self, tablename, z, x, y):

        sqlcmd = 'select x, y, z, data, date, lastmodified, etag, updated, md5 from {} where (z=?) and (x=?) and (y=?)'.format(tablename)
        ti = None

        try:
            cur = self.cur.execute(sqlcmd, (z, x, y))

            rows = cur.fetchall()

            for dbrecord in rows:
                ti = TileInfo(None, None, None, None)
                ti.data = dbrecord[3]
                ti.date = dbrecord[4]
                ti.lastmodified = dbrecord[5]
                ti.etag = dbrecord[6]
                ti.updated = dbrecord[7]
                ti.md5 = dbrecord[8]

        except Exception as e:
            self.logger.error("Error Execute SQL Statement:{}".format(sqlcmd))
            self.logger.exception(e)

        return ti
