'''
Created on 07.02.2019

@author: stevo
'''
import unittest
from Utils.ProcessCmd import _ProcessCmd
from Utils.glog import initlog

PYTHON = "C:\\tools\\Python35\\python.exe"


class Test(unittest.TestCase):

    def test_fetch(self):
        ret = _ProcessCmd("{} fetch.py -i ./sample/atlas/osmcb/sea/osmcb-catalog-test.xml".format(PYTHON), "./../")
        self.assertEqual(ret, 0)

    def test_fetch_002(self):
        ret = _ProcessCmd("{} fetch.py -i ./sample/atlas/osmcb/sea/osmcb-catalog-test.xml".format(PYTHON), "./../")
        self.assertEqual(ret, 0)

    def test_fetch_003(self):
        ret = _ProcessCmd("{} fetch.py -i ./sample/atlas/osmcb/sea/osmcb-catalog-test.xml -u".format(PYTHON), "./../")
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    initlog('unittest', False)
    #import sys;sys.argv = ['', 'Test.test_fetch']
    unittest.main()