#!/usr/bin/python3
# encoding: utf-8


import unittest
from Utils.glog import initlog, getlog
from tile.MergeThread import _MergePictures


class TestMergePictures(unittest.TestCase):

    def setUp(self):
        initlog('bTestMerge')
        self.logger = getlog()

    def tearDown(self):
        pass

    def test_MergePicture(self):
        _MergePictures("./sample/file_openstreetmap.png", "./sample/file_openseamap.png", "./sample/result.png")


if __name__ == "__main__":
    unittest.main()
