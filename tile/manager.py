#!/usr/bin/python3
# encoding: utf-8

from Utils.glog import getlog
from Utils.DownloadThread import DownloadThread
from tile.sqllitedb import TileSqlLiteDB
from tile.MergeThread import MergeThread
import threading

MERGEDIR = 'Merge/'


class TileServer():

    def __init__(self, name, url):
        self.name = name
        self.url = url


class TileManager(object):
    '''
    classdocs
    '''

    def __init__(self, WorkingDirectory, DBDIR):
        '''
        Constructor
        '''
        self._WorkingDirectory = WorkingDirectory

        self.DBDIR = DBDIR
        self.logger = getlog()

        self.tile = 0
        self.tiledownloaded = 0
        self.tiledownloadskipped = 0
        self.tileskipped = 0
        self.tilemerged = 0
        self.tilemergedskipped = 0
        self.downloaderror = 0
        self.Error_304 = 0
        self.Error_502 = 0
        self.Error_404 = 0
        self.Error_url = 0

        # just ensure that db UDP_TUNNEL
        db = TileSqlLiteDB(self.DBDIR)
        db.CloseDB()

    def UpdateTiles(self, tileserv, ti, force_download):
        cnt = 0
        self.joblist = list()
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                # stop processing of sea rander tiles with zoomlevel lower then nine
                # if tileserv.name == OpenSeaMap and ti.zoom < 9:
                #     break
                self.joblist.append([cnt, x, y, ti.zoom])
                cnt += 1

        # create download threads
        self.threadlist = list()

        # creating a lock
        lock = threading.Lock()

        for thread in range(10):
            thread = thread
            self.threadlist.append(DownloadThread(self, lock, force_download, self.DBDIR))

        # create download threads
        for threadrunner in self.threadlist:
            threadrunner.SetTileSrv(tileserv)
            threadrunner.start()

        # wait until all threads are ready
        for threadrunner in self.threadlist:
            threadrunner.join()

        for threadrunner in self.threadlist:
            cnt += threadrunner.cnt

        return cnt

    def MergeTiles(self, TsOpenSeaMap, TSOpenStreetMap, ti):
        cnt = 0
        self.joblist = list()
        for y in range(ti.ytile_nw, ti.ytile_se + 1):
            for x in range(ti.xtile_nw, ti.xtile_se + 1):
                z = ti.zoom
                self.joblist.append([cnt, x, y, z])
                cnt += 1

        # create download threads
        self.threadlist = list()

        for thread in range(10):
            thread = thread
            self.threadlist.append(MergeThread(self, self.DBDIR))

        # create download threads
        for threadrunner in self.threadlist:
            threadrunner.SetTileSrv(TsOpenSeaMap, TSOpenStreetMap)
            threadrunner.start()

        # wait until all threads are ready
        for threadrunner in self.threadlist:
            threadrunner.join()

        # cleanup workspace
        for threadrunner in self.threadlist:
            threadrunner.CleanupWorkingDir()

        return cnt
