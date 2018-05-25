'''
Created on 23.05.2018

@author: stevo
'''
import os
import glob
import shutil
import logging
from Utils.Helper import ChartInfo
from Utils.ProcessCmd import JoinPicture, GenerateKapFile

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
        self.logger = logging.getLogger("main")

    def GenerateKAP(self, atlas, atlasname):
        self.atlas = atlas

        for singlemap in atlas:
            ti = ChartInfo(singlemap)
            self.logger.info("Process Chart {}".format(ti.name))

            # cleanup temp directories
            PathTempTiles = self._WorkingDirectory + "{}/{}/{}/{}/".format(STICHDIR, atlasname, ti.name, ti.zoom)
            RemoveDir(PathTempTiles)
            kapdirname = "{}kap".format(self._WorkingDirectory)
            kapfilename = "{}/{}/{}_{}.kap".format(kapdirname, atlasname, ti.name, ti.zoom)
            RemoveDir(kapdirname)

            # export tiles
            for y in range(ti.ytile_nw, ti.ytile_se + 1):
                for x in range(ti.xtile_nw, ti.xtile_se + 1):
                    # get tiles from db
                    tile = self.db.GetTile("OpenSeaMapMerged", ti.zoom, x, y)

                    # check if tile exists
                    if tile is None:
                        self.logger.Error("tile with z={} x={} y={} not available in store\n")
                        assert(0)

                    # write tile to local file
                    TileMerged = "{}{}-{}-{}.png".format(PathTempTiles, ti.zoom, y, x)
                    tile.StoreFile(TileMerged)

            # stich tiles
            tempfilename = "{}{}_{}.png".format(PathTempTiles, ti.name, ti.zoom)
            JoinPicture(ti.x_cnt, ti.y_cnt, "{}*.png".format(PathTempTiles), tempfilename)

            # generate kap file
            GenerateKapFile(tempfilename, kapfilename, ti)

        return
