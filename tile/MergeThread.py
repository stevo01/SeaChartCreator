#!/usr/bin/python3
# encoding: utf-8

import threading
from tile.sqllitedb import TileSqlLiteDB
from random import *
from tile.Info import TileInfo
import hashlib
import shutil
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

OpenSeaMapMerged = 'OpenSeaMapMerged'


def _MergePictures(background_file, overlay_file, result_file):

    background = Image.open(background_file)
    overlay = Image.open(overlay_file)

    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    new_img = Image.alpha_composite(background, overlay)
    new_img.save(result_file, "PNG")


class MergeThread(threading.Thread):

    def __init__(self, tileman, DBDIR):
        threading.Thread.__init__(self)
        self.tileman = tileman
        self.DBDIR = DBDIR
        self.stop = False
        self._WorkingDirMerge = self.tileman._WorkingDirectory + "{}".format(randint(1, 0xffffffff))

    def SetTileSrv(self, TsOpenSeaMap, TSOpenStreetMap):
        self.TSOpenStreetMap = TSOpenStreetMap
        self.TsOpenSeaMap = TsOpenSeaMap

    def CleanupWorkingDir(self):
        if os.path.exists(self._WorkingDirMerge):
            print("rmtree " + self._WorkingDirMerge)
            shutil.rmtree(self._WorkingDirMerge)

    def run(self):
        # log = getlog()
        self.db = TileSqlLiteDB(self.DBDIR)
        cnt = 0

        while(self.stop is False):
            if len(self.tileman.joblist) is 0:
                self.stop = True
                break
            job = self.tileman.joblist[0]
            self.tileman.joblist.pop(0)
            # print("{} is working on job {} {} {} {}".format(self.name, job[0], job[1], job[2], job[3]))

            x = job[1]
            y = job[2]
            z = job[3]

            tile_osm_street = self.db.GetTile(self.TSOpenStreetMap.name, z, x, y)
            tile_osm_sea = self.db.GetTile(self.TsOpenSeaMap.name, z, x, y)
            tile_osm3 = self.db.GetTile(OpenSeaMapMerged, z, x, y)

            # stop processing if tile is not available
            if tile_osm_street is None or tile_osm_sea is None:
                assert(False)
                break

            if (tile_osm_street.updated is not 0) or (tile_osm_sea.updated is not 0) or (tile_osm3 is None):
                tile_merged = self.MergeTile(tile_osm_street, tile_osm_sea)
                self.db.StoreTile(OpenSeaMapMerged, tile_merged, z, x, y)

                tile_osm_street.updated = False
                self.db.StoreTile(self.TSOpenStreetMap.name, tile_osm_street, z, x, y)

                tile_osm_sea.updated = False
                self.db.StoreTile(self.TsOpenSeaMap.name, tile_osm_sea, z, x, y)
                self.tileman.tilemerged += 1
            else:
                self.tileman.tilemergedskipped += 1
            cnt += 1

        self.db.CloseDB()

    def MergeTile(self, tile_osm_street, tile_osm_sea):
        # store tile  in file
        filename_in1 = self._WorkingDirMerge + "/" + 'file_openstreetmap.png'
        filename_in2 = self._WorkingDirMerge + "/" + 'file_openseamap.png'
        filename_result1 = self._WorkingDirMerge + "/" + 'file_merged.png'

        # print(hashlib.md5(tile_osm_sea.data).hexdigest())

        # check if tile is blank (or in other words empty)
        if "df9310416043ee37c3b3d4896549d823" == hashlib.md5(tile_osm_sea.data).hexdigest():
            filename_result1 = filename_in1
            tile_osm_street.StoreFile(filename_result1)
        else:
            tile_osm_street.StoreFile(filename_in1)
            tile_osm_sea.StoreFile(filename_in2)

            _MergePictures(filename_in2,
                           filename_in1,
                           filename_result1)

        ret = TileInfo()
        ret.SetData(filename_result1)
        return ret
