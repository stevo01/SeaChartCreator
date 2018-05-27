#!/usr/bin/python3
# encoding: utf-8
'''

Copyright (C) 2017  Steffen Volkmann

This file is part of SeaMapCreator.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
'''

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
    for filename in  glob.iglob('{}**/*{}'.format(path, filterval), recursive=recursive_value):
        filenamelist.append(filename)
    
    return filenamelist
    
