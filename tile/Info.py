#!/usr/bin/python3
# encoding: utf-8


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
        self.updated = False  # True indicates update of tile data
        self.date_updated = False  # True indicates update of download date

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
