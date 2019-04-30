#!/usr/bin/python33
# encoding: utf-8

'''
import urllib
from Utils import __app_identifier__


# load singlke file with http protocol
def HttpLoadFile(url, filename):

    # set user agent to meet the tile usage policy
    # https://operations.osmfoundation.org/policies/tiles/

    print("HttpLoadFile open {}".format(url))
    req = urllib.request.Request(url, data=None, headers={'User-Agent': __app_identifier__})
    f = urllib.request.urlopen(req)
    data = f.read()
    print("HttpLoadFile transfer finished {}".format(url))

    print("HttpLoadFile open file {}".format(filename))
    with open(filename, 'wb') as f:
        print("HttpLoadFile write {} bytes".format(len(data)))
        f.write(data)

    return filename
'''
