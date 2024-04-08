#!/usr/bin/python3
# encoding: utf-8

import argparse
import time
import os
import json
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.Helper import ChartInfo
from tile.manager import TileManager, TileServer
from Utils.glog import getlog, initlog


def main():
    
    parser = argparse.ArgumentParser(description='merge tiles')
    WDIR = os.getcwd() + '/work/'
    DBDIR = WDIR + "database/"
    parser.add_argument("-i",
                        help="MOBAC Project File",
                        dest="ProjectFile",
                        default="./sample/atlas/mobac/mobac-profile-testprj.xml")

    parser.add_argument("-d", "--DatabaseDirectory", 
                        help="tile store directory",
                        dest="DBDIR",
                        default=DBDIR)

    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="quiet",
                        default=True,
                        help="set log level to info (instead debug)")

    parser.add_argument("-s", "--skip",
                        action="store_true",
                        dest="skip_os",
                        help="skip odd zoom levels")

    parser.add_argument("-m", "--mapsource",
                        help="map server configuration file",
                        dest="MapSrcFile",
                        default="./sample/mapsource/mp-OpenSeaMap.yaml")

    args = parser.parse_args()

    initlog('merge', args.quiet)
    logger = getlog()

    logger.info('Start merge tiles')

    if(args.skip_os is True):
        zoom_filter = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    else:
        zoom_filter = []

    # get maps from mobac project file
    if args.ProjectFile is not None:
        # get list of chart areas from project file
        atlas, name = ExtractMapsFromAtlas(args.ProjectFile, zoom_filter)
        logger.info('atlas name={} number of maps={}'.format(name, len(atlas)))
    else:
        exit()

    tm = TileManager(WDIR, args.DBDIR)

    with open(args.MapSrcFile) as json_file:
        data = json.load(json_file)

    logger.info('')
    logger.info('server info:')
    logger.info('{} url={}'.format(data['basic_layer']['name'], data['basic_layer']['url']))
    logger.info('{} url={}'.format(data['seamark_layer']['name'], data['seamark_layer']['url']))
    logger.info('')
    logger.info('database info:')
    logger.info('{}'.format(args.DBDIR))
    logger.info('')
    logger.info('project info:')
    logger.info('{}'.format(args.ProjectFile))

    TSOpenStreetMap = TileServer(data['basic_layer']['name'], data['basic_layer']['url'])
    TsOpenSeaMap = TileServer(data['seamark_layer']['name'], data['seamark_layer']['url'])

    logger.info('Merge Open Sea Map tiles from {}'.format(TSOpenStreetMap.name))
    mapcnt = 1
    for singlemap in atlas:
        ti = ChartInfo(singlemap)
        logger.info('\n\nStart Merge Tile {} / {}:'.format(mapcnt, len(atlas)))
        mapcnt += 1
        starttime = time.time()
        logger.info(ti)
        cnt = tm.MergeTiles( TsOpenSeaMap, TSOpenStreetMap, ti)
        stoptime = time.time()
        runtime = (stoptime - starttime)
        if runtime == 0:
            runtime = 1
        logger.info('time: {} s'.format(int(stoptime - starttime)))
        logger.info('tiles merged           {}'.format(tm.tilemerged))
        logger.info('tiles mergedskipped    {}'.format(tm.tilemergedskipped))
        logger.info('processsed tiles/s     {0:.2f}'.format(cnt / runtime))


    logger.info('\n\nready')

    return


if __name__ == "__main__":
    exit(main())
