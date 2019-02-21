# -*- coding: utf-8 -*-
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from pySync import *

class UtilFunctionTests(unittest.TestCase):
	def test_md5sum_str(self):
		self.assertEqual(md5sum_str(b'hello'), '5d41402abc4b2a76b9719d911017c592')

if __name__ == '__main__':
	unittest.main()

