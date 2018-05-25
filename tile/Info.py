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

import yaml
from Utils.Helper import ensure_dir


class TileInfo(object):
    '''
    classdocs
    '''

    def __init__(self, data=None, etag=None, date=None, lastmodified=None):
        self.data = data
        self.etag = etag
        self.date = date
        self.lastmodified = lastmodified
        self.md5 = None
        self.updated = False

    def SetData(self, filename):
        with open(filename, 'rb') as f:
            self.data = f.read()

    def SetTileInfo(self, filename):

        with open(filename, 'r') as stream:
            try:
                tmp = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            self.etag = tmp['etag']
            self.date = tmp['date']
            self.md5 = tmp['md5']
            self.lastmodified = tmp['lastmodified']
            self.updated = tmp['updated']

    def StoreFile(self, filename):
        ensure_dir(filename)
        with open(filename, 'wb') as f:
            f.write(self.data)
