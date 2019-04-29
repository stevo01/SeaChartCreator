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
import os
import shutil
from Utils.ProcessCmd import ZipFiles, StitchPicture, GenerateKapFile
from Utils.glog import getlog
import datetime
from Utils.Helper import ChartInfo, ensure_dir
from tile.mbtilestore import MBTileStore
from config import OpenStreetMap, OpenSeaMap, OpenSeaMapMerged
from tile.MergeThread import _MergePictures

STICHDIR = "StichDir"


def RemoveDir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


def RemoveFile(filename):
    if os.path.exists(filename):
        os.remove(filename)


class AtlasGenerator(object):
    '''
    classdocs
    '''

    def __init__(self, WorkingDirectory, db):
        '''
        Constructor
        '''
        self._WorkingDirectory = WorkingDirectory
        self.db = db
        self.logger = getlog()

    # @param ci - chart information for single map
    def StichTiles(self, ci, atlasname, tablename):
            # cleanup temp directories
            self.logger.info("Cleanup Stitch Directory")
            PathTempTiles = self._WorkingDirectory + "{}/{}/{}/{}/{}/".format(STICHDIR, tablename, atlasname, ci.name, ci.zoom)
            RemoveDir(PathTempTiles)

            # export tiles
            self.logger.info("Export {} Tiles".format(ci.nr_of_tiles))

            cnt = 1
            for y in range(ci.ytile_nw, ci.ytile_se + 1):
                for x in range(ci.xtile_nw, ci.xtile_se + 1):
                    # get tiles from db
                    tile = self.db.GetTile(tablename, ci.zoom, x, y)

                    # check if tile exists
                    if tile is None:
                        self.logger.error("tile with z={} x={} y={} not available in store\n".format(ci.zoom, x, y))
                        assert(0)

                    # write tile to local file
                    TileMerged = "{0:s}{1:d}-{2:05d}.png".format(PathTempTiles, ci.zoom, cnt)
                    tile.StoreFile(TileMerged)
                    cnt = cnt + 1

            # stich tiles
            self.logger.info("Stich {} tiles for map {}".format(ci.nr_of_tiles, ci.name))
            tempfilename = "{}{}_{}.png".format(PathTempTiles, ci.name, ci.zoom)
            StitchPicture(ci.x_cnt, ci.y_cnt, "{}*.png".format(PathTempTiles), tempfilename)

            return tempfilename

    def GenerateKAP(self, atlas, atlasname, reducecolors):
        self.atlas = atlas

        now = datetime.datetime.now()
        creationtimestamp = now.strftime("%Y%m%d-%H%M")

        self.logger.info("Cleanup Kap Directory")
        kapdirname = "{}kap/OSM-OpenCPN2-KAP-{}-{}/".format(self._WorkingDirectory, atlasname, creationtimestamp)

        RemoveDir(kapdirname)
        cnt = 0
        for singlemap in atlas:
            cnt = cnt + 1
            ci = ChartInfo(singlemap)
            self.logger.info("################################################################################")
            self.logger.info("Process Chart {}, {}/{}".format(ci.name, cnt, len(atlas)))
            kapfilename = "{}/{}_{}.kap".format(kapdirname, ci.name, ci.zoom)

            # Stitch tiles to single map file
            tempfilename_street = self.StichTiles(ci, atlasname, OpenStreetMap)
            tempfilename_sea = self.StichTiles(ci, atlasname, OpenSeaMap)

            PathTempTiles = self._WorkingDirectory + "{}/{}/{}/{}/{}/".format(STICHDIR, OpenSeaMapMerged, atlasname, ci.name, ci.zoom)
            RemoveDir(PathTempTiles)
            ensure_dir(PathTempTiles)
            tempfilename = "{}{}_{}.png".format(PathTempTiles, ci.name, ci.zoom)

            # merge files
            _MergePictures(tempfilename_street, tempfilename_sea, tempfilename)
            # MergePictures(tempfilename_sea, tempfilename_street, tempfilename+".2.png")

            '''
            reduce png file to 8 bit to avoid error in imagekap procedure:

            ERROR - internal GetPalette
            ERROR - imgkap return 2
            '''
            #if reducecolors is True:
            #    tempfilereduced = "{}{}_{}_8.png".format(PathTempTiles, ci.name, ci.zoom)
            #    ConvertPicture(tempfilename, tempfilereduced)
            #else:
            #    tempfilereduced = tempfilename

            tempfilereduced = tempfilename

            # generate kap file
            self.logger.info("generate kap file {}".format(kapfilename))
            GenerateKapFile(tempfilereduced, kapfilename, ci)

        # copy info.txt
        shutil.copyfile("documents/info.txt", kapdirname + "info.txt")

        atlasfilename = "{}history/kap/OSM-OpenCPN2-KAP-{}-{}.7z".format(self._WorkingDirectory,
                                                                         atlasname,
                                                                         creationtimestamp)

        ZipFiles(kapdirname, atlasfilename)

        atlasfilename_latest = "./work/kap/OSM-OpenCPN2-KAP-{}.7z".format(atlasname)
        
        ratlasfilename = "../history/kap/OSM-OpenCPN2-KAP-{}-{}.7z".format(atlasname,
                                                                          creationtimestamp)
        
        os.symlink(ratlasfilename, atlasfilename_latest)

    def generate_mbtile(self, atlas, atlasname):
        '''
        generate atlas in mbtile format
        '''
        self.atlas = atlas

        now = datetime.datetime.now()
        creationtimestamp = now.strftime("%Y%m%d-%H%M")

        atlasdirname = "{}mbtiles/OSM-mbtile-{}-{}/".format(self._WorkingDirectory, atlasname, creationtimestamp)
        mbtilefilename = "{}/{}.mbtiles".format(atlasdirname, atlasname)

        self.logger.info("Cleanup tilestore Directory")
        RemoveDir(atlasdirname)

        tilestore = MBTileStore(mbtilefilename)
        tilestore.SetMetadata("name", atlasname)
        tilestore.SetMetadata("format", "png")

        cnt = 0
        for singlemap in atlas:
            cnt = cnt + 1
            ci = ChartInfo(singlemap)
            self.logger.info("################################################################################")
            self.logger.info("Process Chart {}, {}/{}".format(ci.name, cnt, len(atlas)))

            # export tiles
            self.logger.info("Export {} Tiles".format(ci.nr_of_tiles))
            for y in range(ci.ytile_nw, ci.ytile_se + 1):
                for x in range(ci.xtile_nw, ci.xtile_se + 1):
                    # get tiles from db
                    tile = self.db.GetTile(OpenSeaMapMerged, ci.zoom, x, y)
                    # check if tile exists
                    if tile is None:
                        self.logger.error("tile with z={} x={} y={} not available in store\n")
                        assert(0)
                    tilestore.StoreTile(tile, ci.zoom, x, y)

        tilestore.SetMetadata("bounds",
                              "{},{},{},{}".format(ci.SE_lat,
                                                   ci.SE_lon,
                                                   ci.NW_lat,
                                                   ci.NW_lon))

        # copy info.txt
        shutil.copyfile("documents/info.txt", atlasdirname + "info.txt")

        atlasfilename = "{}history/mbtiles/OSM-mbtile-{}-{}.7z".format(self._WorkingDirectory,
                                                                       atlasname,
                                                                       creationtimestamp)

        tilestore.CloseDB()

        ZipFiles(atlasdirname, atlasfilename)

        atlasfilename_latest = "./work/mbtiles/OSM-mbtile-{}.7z".format(atlasname)

        ratlasfilename = "../history/mbtiles/OSM-mbtile-{}-{}.7z".format(atlasname,
                                                                         creationtimestamp)

        RemoveFile(atlasfilename_latest)

        os.symlink(ratlasfilename, atlasfilename_latest)
