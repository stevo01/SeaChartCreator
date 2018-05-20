'''
Created on 20.05.2018

@author: stevo
'''

from optparse import OptionParser
from Utils.Mobac import ExtractMapsFromAtlas
from Utils.Helper import TileInfo
from tile.manager import TileManager
from tile.db import TileDB

DBDIR = './../work/database/'
WDIR  = './../work/'


def main():
    parser = OptionParser()
    parser.add_option("-i", "--InFile", type="string", help="MOBAC Project File", dest="ProjectFile", default="./../sample/atlas/mobac/mobac-profile-testprj.xml")

    options, arguments = parser.parse_args()
    arguments = arguments

    # get maps from mobac project file
    if options.ProjectFile is not None:
        # get list of chart areas from project file
        atlas = ExtractMapsFromAtlas(options.ProjectFile)
    else:
        exit()

    db = TileDB(DBDIR)
    tm = TileManager(WDIR, db)

    for singlemap in atlas:
        ti = TileInfo(singlemap)
        tm.UpdateTiles(ti)
        print(ti)

    return

if __name__ == "__main__":
    exit(main())
