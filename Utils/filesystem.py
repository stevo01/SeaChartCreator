#!/usr/bin/python3
# encoding: utf-8


import os
import glob


def GetFileList(path, filterval=None):
    filenamelist = os.listdir(path)

    if filterval:
        ret = list()
        for filename in filenamelist:
            if filename.find(filterval) != -1:
                ret.append(path + filename)
    else:
        ret = filenamelist

    return ret


def _GetFileList(path, filterval, recursive_value=True):
    filenamelist = list()
    for filename in glob.iglob('{}**/*{}'.format(path, filterval), recursive=recursive_value):
        filenamelist.append(filename)

    return filenamelist
