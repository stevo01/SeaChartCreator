#!/usr/bin/python3
# encoding: utf-8


from optparse import OptionParser
from Utils.Mobac import ExtractMapsFromAtlas
from atlas.generator import AtlasGenerator
from Utils.glog import getlog, initlog
from tile.sqllitedb import TileSqlLiteDB

DBDIR = './work/database/'
WDIR = './work/'


def main():
    parser = OptionParser()
    parser.add_option("-i", "--InFile", type="string", help="MOBAC Project File", dest="ProjectFile", default="./sample/atlas/mobac/mobac-profile-testprj.xml")
    parser.add_option("-d", "--DatabaseDirectory", type="string", help="tile store directory", dest="DBDIR", default=DBDIR)
    parser.add_option("-q", "--quiet", action="store_false", dest="quiet", default=True, help="set log level to info (instead debug)")
    parser.add_option("-s", "--skip", action="store_true", dest="skip_os", help="skip odd zoom levels")
    parser.add_option("-t", "--Type", type="string", help="atlas type (kap or mbtile)", dest="AtlasType", default="kap")

    options, arguments = parser.parse_args()
    arguments = arguments

    initlog('build', options.quiet)
    logger = getlog()

    logger.info('Start build map')

    if(options.skip_os is True):
        zoom_filter = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    else:
        zoom_filter = []

    logger.info('')
    logger.info('database info:')
    logger.info('{}'.format(options.DBDIR))
    logger.info('')
    logger.info('project info:')
    logger.info('{}'.format(options.ProjectFile))

    # get maps from mobac project file
    if options.ProjectFile is not None:
        # get list of chart areas from project file
        atlas, name = ExtractMapsFromAtlas(options.ProjectFile, zoom_filter)
    else:
        exit()

    db = TileSqlLiteDB(options.DBDIR)
    gen = AtlasGenerator(WDIR, db)

    if options.AtlasType.find("kap") == 0:
        gen.GenerateKAP(atlas, name)
    elif options.AtlasType.find("mbtile") == 0:
        gen.generate_mbtile(atlas, name)
    else:
        assert(0)

    logger.info('ready')
    db.CloseDB()

    return


if __name__ == "__main__":
    exit(main())
