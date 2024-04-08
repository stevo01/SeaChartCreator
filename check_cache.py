#!/usr/bin/python3
# encoding: utf-8


from optparse import OptionParser
import time
import os
import json
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.Helper import ChartInfo
from tile.manager import TileManager, TileServer
from Utils.glog import getlog, initlog
from tile.sqllitedb import TileSqlLiteDB
from tile.sqllitedb import OpenStreetMap, OpenSeaMap, OpenSeaMapMerged


def main():
    
    WDIR = os.getcwd() + '/work/'
    DBDIR = WDIR + "database/"
    
    parser = OptionParser()
    parser.add_option("-i", "--InFile", type="string", help="MOBAC Project File", dest="ProjectFile", default="./sample/atlas/mobac/mobac-profile-testprj.xml")
    parser.add_option("-d", "--DatabaseDirectory", type="string", help="tile store directory", dest="DBDIR", default=DBDIR)
    parser.add_option("-q", "--quiet", action="store_false", dest="quiet", default=True, help="set log level to info (instead debug)")
    parser.add_option("-s", "--skip", action="store_true", dest="skip_os", help="skip odd zoom levels")
    
    options, arguments = parser.parse_args()
    arguments = arguments
   

    initlog('fetch', options.quiet)
    logger = getlog()

    logger.info('Start fetch tiles')

    if(options.skip_os is True):
        zoom_filter = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    else:
        zoom_filter = []

    # get maps from mobac project file
    if options.ProjectFile is not None:
        # get list of chart areas from project file
        atlas, name = ExtractMapsFromAtlas(options.ProjectFile, zoom_filter)
        logger.info('atlas name={} number of maps={}'.format(name, len(atlas)))
    else:
        exit()


    db = TileSqlLiteDB(options.DBDIR)
    
    map_cnt=0
    tile_cnt_pass=0
    tile_cnt_fail=0
    
    
    for singlemap in atlas:
        map_cnt = map_cnt + 1
        ci = ChartInfo(singlemap)
        
        # export tiles
        for y in range(ci.ytile_nw, ci.ytile_se + 1):
            for x in range(ci.xtile_nw, ci.xtile_se + 1):
                # get tiles from db
                tile = db.GetTile(OpenSeaMapMerged, ci.zoom, x, y)
        
                # check if tile exists
                if tile is None:
                    logger.error("map {} tile with z={} x={} y={} not available in store\n".format(ci.name, ci.zoom, x, y))
                    tile_cnt_fail = tile_cnt_fail + 1
                else:
                    tile_cnt_pass = tile_cnt_pass + 1

    logger.info("map_cnt       = {}".format(map_cnt))
    logger.info("tile_cnt_pass = {}".format(tile_cnt_pass))
    logger.info("tile_cnt_fail = {}".format(tile_cnt_fail))
    db.CloseDB()

    logger.info('\n\nready')

    return


if __name__ == "__main__":
    exit(main())
