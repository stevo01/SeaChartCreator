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

import argparse
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.Helper import ChartInfo
from tile.manager import TileManager, OpenStreetMap, OpenSeaMap, TileServer
from Utils.glog import getlog, initlog
from tile.sqllitedb import TileSqlLiteDB
from Utils.download import CheckExternelUtils
import time

DBDIR = './work/database/'
WDIR = './work/'


def main():
    parser = argparse.ArgumentParser(description='fetch tiles')

    parser.add_argument("-i",
                        help="MOBAC Project File",
                        dest="ProjectFile",
                        default="./sample/atlas/mobac/mobac-profile-testprj.xml")

    parser.add_argument("-d", "--DatabaseDirectory",
                        help="tile store directory",
                        dest="DBDIR",
                        default=DBDIR)

    parser.add_argument("-u", "--update",
                        action="store_true",
                        dest="update",
                        help="update tile if new version existes")

    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        dest="quiet",
                        default=True,
                        help="set log level to info (instead debug)")

    parser.add_argument("-s", "--skip",
                        action="store_true",
                        dest="skip_os",
                        help="skip odd zoom levels")

    args = parser.parse_args()

    initlog('fetch', args.quiet)
    logger = getlog()

    logger.info('Start fetch tiles')

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

    CheckExternelUtils()

    db = TileSqlLiteDB(args.DBDIR)
    tm = TileManager(WDIR, db)

    #TSOpenStreetMap = TileServer(OpenStreetMap, "http://a.tile.openstreetmap.org")
    TSOpenStreetMap = TileServer(OpenStreetMap, "http://stone:8001/tile")

    TsOpenSeaMap = TileServer(OpenSeaMap, "http://tiles.openseamap.org/seamark")

    logger.info('Fetch Open Sea Map tiles from {}'.format(TSOpenStreetMap.name))
    mapcnt = 1
    for singlemap in atlas:
        ti = ChartInfo(singlemap)
        logger.info('Start UpdateTile for street map {} / {}:'.format(mapcnt, len(atlas)))
        mapcnt += 1
        starttime = time.time()
        logger.info(ti)
        cnt = tm.UpdateTiles(TSOpenStreetMap, ti, args.update)
        stoptime = time.time()
        runtime = (stoptime - starttime)
        logger.info('time: {} s'.format(int(stoptime - starttime)))
        logger.info('tiles skipped          {}'.format(tm.tileskipped))
        logger.info('tiles merged           {}'.format(tm.tilemerged))
        logger.info('tiles downloaded       {}'.format(tm.tiledownloaded))
        logger.info('tiles download skipped {}'.format(tm.tiledownloadskipped))
        logger.info('tiles download error   {}'.format(tm.tiledownloaderror))
        logger.info('processsed tiles/s     {0:.2f}'.format(cnt / runtime))

    logger.info('Fetch Open Sea Map tiles from {}'.format(TsOpenSeaMap.name))
    mapcnt = 1
    for singlemap in atlas:
        ti = ChartInfo(singlemap)
        logger.info('Start UpdateTile for sea map {} / {}:'.format(mapcnt, len(atlas)))
        mapcnt += 1
        starttime = time.time()
        logger.info(ti)
        cnt = tm.UpdateTiles(TsOpenSeaMap, ti, args.update)
        stoptime = time.time()
        runtime = (stoptime - starttime)
        logger.info('time: {} s'.format(int(stoptime - starttime)))
        logger.info('tiles skipped          {}'.format(tm.tileskipped))
        logger.info('tiles merged           {}'.format(tm.tilemerged))
        logger.info('tiles downloaded       {}'.format(tm.tiledownloaded))
        logger.info('tiles download skipped {}'.format(tm.tiledownloadskipped))
        logger.info('tiles download error   {}'.format(tm.tiledownloaderror))
        logger.info('processsed tiles/s     {0:.2f}\n'.format(cnt / runtime))

    logger.info('Merge Tiles')
    for singlemap in atlas:
        mapcnt = 1
        ti = ChartInfo(singlemap)
        logger.info('Start UpdateTile for sea map {} / {}:'.format(mapcnt, len(atlas)))
        mapcnt += 1
        starttime = time.time()
        logger.info(ti)
        cnt = tm.MergeTiles(TsOpenSeaMap, TSOpenStreetMap, ti)
        stoptime = time.time()
        runtime = (stoptime - starttime)
        logger.info('time: {} s'.format(int(stoptime - starttime)))
        logger.info('tiles skipped          {}'.format(tm.tileskipped))
        logger.info('tiles merged           {}'.format(tm.tilemerged))
        logger.info('tiles downloaded       {}'.format(tm.tiledownloaded))
        logger.info('tiles download skipped {}'.format(tm.tiledownloadskipped))
        logger.info('tiles download error   {}'.format(tm.tiledownloaderror))
        logger.info('processsed tiles/s     {0:.2f}'.format(cnt / runtime))

    logger.info('ready')
    db.CloseDB()
    return


if __name__ == "__main__":
    exit(main())
