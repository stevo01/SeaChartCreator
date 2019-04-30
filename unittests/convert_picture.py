#!/usr/bin/python3
# encoding: utf-8


import unittest
from Utils.glog import initlog, getlog
from Utils.ProcessCmd import ConvertPicture

class Test_ConvertPictures(unittest.TestCase):

    def setUp(self):
        initlog('bTestConvert')
        self.logger = getlog()

    def tearDown(self):
        pass

    def test_MergePicture(self):
        ret = ConvertPicture("./sample/ArabianSea/L16-28008-43024-64-8/16/L16-28008-43024-64-8_16.png", 
                             "./L16-28008-43024-64-8_16.reduced.png", 
                             options="+dither -colors 127 ")
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
