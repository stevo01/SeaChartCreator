# -*- coding: utf-8 -*-
from tile.Info import TileInfo
from Utils.Helper import ensure_dir
import os
import io
import yaml
from _sha256 import sha256
from _sha1 import sha1
import hashlib

class TileDB(object):
    '''
    classdocs
    '''

    def __init__(self, workspace):
        ensure_dir(workspace)
        self.ws = workspace

    def StoreTile(self, tsname, tile, z , x, y):
        filenametile = "{}{}/{}/{}/{}.png".format(self.ws, tsname, z, x, y)
        ensure_dir(filenametile)
        with open(filenametile, 'wb') as f:
            print("Store Tile {} bytes".format(len(tile.data)))
            f.write(tile.data)

        filenameinfo = filenametile + ".yaml"
        m = hashlib.md5()
        m.update(tile.data)
        data = { "date":tile.date,
                 "etag": tile.etag,
                 "updated": True,
                 "sha256": m.hexdigest()
                 }
        with io.open(filenameinfo, 'w', encoding='utf8') as outfile:
            yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    def GetTile(self, tsname, z , x, y):

        filenametile = "{}{}/{}/{}/{}.png".format(self.ws, tsname, z, x, y)
        filenametileinfo = filenametile + ".yaml"

        # check if file exists
        if os.path.isfile(filenametile) and os.path.isfile(filenametileinfo):
            ret = TileInfo(filenametile, filenametileinfo)
        else:
            ret = None

        return ret