#!/usr/bin/env python
# encoding: utf-8

'''
wrapper functions for usage of external commands

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

import subprocess
from Utils.Helper import TileInfo
       
def _ProcessCmd(cmd): 
    print("execure command: {}".format(cmd))
    return_code = subprocess.call(cmd, shell=True)       
        
def MergePictures(self, SeaMapFilename, OSMFilename, ResultFilename):       
    cmd = "ExternalUtils\\ImageMagick\\composite {} {} {}".format(SeaMapFilename, OSMFilename, ResultFilename)
    _ProcessCmd(cmd)
     
def JoinPicture(xcnt, ycnt, filenamelist, filename):     
    cmd = "ExternalUtils\\ImageMagick\\montage +frame +shadow +label -tile {}x{} -geometry 256x256+0+0 {} {}".format(xcnt, ycnt, filenamelist, filename)
    _ProcessCmd(cmd)
    
def GenerateKapFile(filenamein, filenameout, ti):
    
    cmd = "ExternalUtils\\imgkap\\imgkap {} {} {} {} {} {}".format(filenamein, ti.NW_lat, ti.NW_lon, ti.SE_lat, ti.SE_lon, filenameout)   
    _ProcessCmd(cmd)
    
    cmd = "ExternalUtils\\imgkap\\imgkap {} {} {} ".format(filenameout, filenameout+".export.txt", filenameout+"export.png")
    _ProcessCmd(cmd)