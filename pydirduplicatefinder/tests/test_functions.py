# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import unittest
from testcase import PyDirDuplicateFinderTestCase

from pydirduplicatefinder import interface_texts
from duplicatefinder import main

class TestPrintOption(PyDirDuplicateFinderTestCase):
    
    def testEmptyDirectory(self):
        """Basic test onto an empty directory"""
        self.assertEquals(self.wrapInNormalExecution([self.temp_dir], ''),
                          main(['-ra', 'print', self.temp_dir, ]))

    def test2EmptyDirectories(self):
        """Basic test onto two empty directories"""
        d1 = self.mkDir('d1')
        d2 = self.mkDir('d2')
        self.assertEquals(self.wrapInNormalExecution([d1, d2], ''),
                          main(['-ra', 'print', d1, d2]))

    def test3EmptyDirectoriesWithDuplicate(self):
        """Basic test onto two empty directories (but one passed twice)"""
        d1 = self.mkDir('d1')
        d2 = self.mkDir('d2')
        self.assertEquals(self.wrapInNormalExecution([d1, d2, d2], ''),
                          main(['-ra', 'print', d1, d2, d2]))

suites = []

suites.append(unittest.TestLoader().loadTestsFromTestCase(TestPrintOption))

alltests = unittest.TestSuite(suites)