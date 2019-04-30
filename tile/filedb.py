#!/usr/bin/python3
# encoding: utf-8

from tile.Info import TileInfo
from Utils.Helper import ensure_dir
import os
import io
import yaml
import hashlib
from Utils.glog import getlog


class TileFileDB(object):

    def __init__(self, workspace):
        ensure_dir(workspace)
        self.ws = workspace
        self.logger = getlog()

    def StoreTile(self, tsname, tile, z, x, y):
        filenametile = "{}{}/{}/{}/{}.png".format(self.ws, tsname, z, x, y)
        ensure_dir(filenametile)
        with open(filenametile, 'wb') as f:
            self.logger.debug("Store Tile {} bytes".format(len(tile.data)))
            f.write(tile.data)

        filenameinfo = filenametile + ".yaml"
        m = hashlib.md5()
        m.update(tile.data)
        data = {"date": tile.date,
                "lastmodified": tile.lastmodified,
                "etag": tile.etag,
                "updated": tile.updated,
                "md5": m.hexdigest()
                }
        with io.open(filenameinfo, 'w', encoding='utf8') as outfile:
            yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    def GetTile(self, tsname, z, x, y):

        filenametile = "{}{}/{}/{}/{}.png".format(self.ws, tsname, z, x, y)
        filenametileinfo = filenametile + ".yaml"

        # check if file exists
        if os.path.isfile(filenametile) and os.path.isfile(filenametileinfo):
            ret = TileInfo(None, None, None, None)
            ret.SetData(filenametile)
            ret.SetTileInfo(filenametileinfo)
        else:
            ret = None

        return ret
