# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import unittest
from testcase import PyDirDuplicateFinderTestCase

from pydirduplicatefinder import interface_texts
from duplicatefinder import main

class TestPathFilters(PyDirDuplicateFinderTestCase):
    
    def testDirectDirectoryName(self):
        """Test passing a single full directory name to --include-dir option"""
        d1 = self.mkDir('Lorem')
        d2 = self.mkDir('Ipsum')
        d3 = self.mkDir('at')
        self.assertEquals(main(['-v','--include-dir', d2, d1, d2, d3, ]),
                          self.wrapInNormalExecution([self.temp_dir], []),
                          )

suites = []

suites.append(unittest.TestLoader().loadTestsFromTestCase(TestPathFilters))

alltests = unittest.TestSuite(suites)