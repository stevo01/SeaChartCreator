'''
Created on 07.02.2019

@author: stevo
'''
import unittest
from Utils.ProcessCmd import _ProcessCmd
from Utils.glog import initlog

PYTHON = "python3"


class Test(unittest.TestCase):

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

    def test_fetch_001(self):
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
    unittest.main()
