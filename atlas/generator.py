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
from Utils.Helper import ChartInfo
from Utils.ProcessCmd import JoinPicture, GenerateKapFile, \
    GenerateKapFileNew
from Utils.glog import getlog

STICHDIR = "StichDir"


def RemoveDir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


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

    def GenerateKAP(self, atlas, atlasname):
        self.atlas = atlas

        self.logger.info("Cleanup Kap Directory")
        kapdirname = "{}kap/{}/".format(self._WorkingDirectory, atlasname)
        RemoveDir(kapdirname)

        for singlemap in atlas:
            ci = ChartInfo(singlemap)
            self.logger.info("Process Chart {}".format(ci.name))

            # cleanup temp directories
            self.logger.info("Cleanup Stitch Directory")
            PathTempTiles = self._WorkingDirectory + "{}/{}/{}/{}/".format(STICHDIR, atlasname, ci.name, ci.zoom)
            RemoveDir(PathTempTiles)
            kapfilename = "{}/{}_{}.kap".format(kapdirname, ci.name, ci.zoom)
            kapheaderfilename = "{}/{}_{}.kap.header".format(kapdirname, ci.name, ci.zoom)

            # export tiles
            self.logger.info("Export {} Tiles".format(ci.nr_of_tiles))
            for y in range(ci.ytile_nw, ci.ytile_se + 1):
                for x in range(ci.xtile_nw, ci.xtile_se + 1):
                    # get tiles from db
                    tile = self.db.GetTile("OpenSeaMapMerged", ci.zoom, x, y)

                    # check if tile exists
                    if tile is None:
                        self.logger.error("tile with z={} x={} y={} not available in store\n")
                        assert(0)

                    # write tile to local file
                    TileMerged = "{}{}-{}-{}.png".format(PathTempTiles, ci.zoom, y, x)
                    tile.StoreFile(TileMerged)

            # stich tiles
            self.logger.info("Stich {} tiles for map {}".format(ci.nr_of_tiles, ci.name))
            tempfilename = "{}{}_{}.png".format(PathTempTiles, ci.name, ci.zoom)
            JoinPicture(ci.x_cnt, ci.y_cnt, "{}*.png".format(PathTempTiles), tempfilename)

            # generate kap file
            self.logger.info("generate kap file {}".format(kapfilename))
            #GenerateKapFile(tempfilename, kapfilename, ci)
            GenerateKapFileNew(tempfilename, kapfilename, ci)

