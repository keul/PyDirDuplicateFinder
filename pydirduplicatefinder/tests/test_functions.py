# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import unittest
from testcase import PyDirDuplicateFinderTestCase

class TestPrintOption(PyDirDuplicateFinderTestCase):
    
    def testSimpleFiles(self):
        """Basic test for simple usage"""
        self.assertEquals(['aaa', 55], ['aa', 55])

suites = []

suites.append(unittest.TestLoader().loadTestsFromTestCase(TestPrintOption))

alltests = unittest.TestSuite(suites)