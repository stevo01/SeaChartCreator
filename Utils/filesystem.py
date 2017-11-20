'''
Created on 24.12.2017

@author: stevo
'''
import os
import glob

def GetFileList(path, filter=None):
    filenamelist = os.listdir(path)

    if filter:
        ret = list()
        for filename in filenamelist:
            if filename.find(filter) != -1:
                ret.append(path + filename)
    else:
        ret = filenamelist

    return ret

def _GetFileList(path, filter, recursive_value=True):
    filenamelist=list()
    for filename in  glob.iglob('{}**/*{}'.format(path, filter), recursive=recursive_value):
        filenamelist.append(filename)
    
    return filenamelist
    