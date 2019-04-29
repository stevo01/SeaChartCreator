#!/usr/bin/python3
# encoding: utf-8

'''

Copyright (C) 2017  Steffen Volkmann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

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
