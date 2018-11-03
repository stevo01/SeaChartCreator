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
