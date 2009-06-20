# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import unittest
from testcase import PyDirDuplicateFinderTestCase

from pydirduplicatefinder import interface_texts
from duplicatefinder import main

class TestBasicOperations(PyDirDuplicateFinderTestCase):
    
    def testEmptyDirectory(self):
        """Basic test onto an empty directory"""
        self.assertEquals(main(['-ra', 'print', self.temp_dir, ]),
                          self.wrapInNormalExecution([self.temp_dir], []),
                          )

    def test2EmptyDirectories(self):
        """Basic test onto two empty directories"""
        d1 = self.mkDir('d1')
        d2 = self.mkDir('d2')
        self.assertEquals(main(['-ra', 'print', d1, d2]),
                          self.wrapInNormalExecution([d1, d2], []),
                          )

    def test3EmptyDirectoriesWithDuplicateDir(self):
        """Basic test onto two empty directories (but one passed twice)"""
        d1 = self.mkDir('d1')
        d2 = self.mkDir('d2')
        self.assertEquals(main(['-ra', 'print', d1, d2, d2]),
                          self.wrapInNormalExecution([d1, d2], ''),
                          )

    def test3EmptyDirectoriesWithDuplicateDir2(self):
        """Basic test onto two directories, one empty and one with a 50 bytes file; this directory is passed twice"""
        d1 = self.mkDir('d1')
        d2 = self.mkDir('d2')
        self.addFile("a", d2, 200)
        self.assertEquals(main(['-ra', 'print', d1, d2, d2]),
                          self.wrapInNormalExecution([d1, d2], []),
                          )

    def testDirectoryAndSingleFileIn(self):
        """Basic test onto two directories, one empty and one with a 50 bytes file"""
        d1 = self.mkDir('d1')
        d2 = self.mkDir('d2')
        self.addFile("a", d2, 200)
        self.assertEquals(main(['-ra', 'print', d1, d2]),
                          self.wrapInNormalExecution([d1, d2], []),
                          )

    def test2DifferentFilesWithSameSizeInSameDir(self):
        """Basic test onto two different files with the same size in the same dir"""
        self.addFile("a", self.temp_dir, 200)
        self.addFile("b", self.temp_dir, 200)
        self.assertEquals(main(['-ra', 'print', self.temp_dir]),
                          self.wrapInNormalExecution([self.temp_dir,], []),
                          )

    def test2DifferentFilesWithDifferentSizeInSameDir(self):
        """Basic test onto two different files (for content and size) in the same dir"""
        self.addFile("a", self.temp_dir, 200)
        self.addFile("b", self.temp_dir, 200)
        self.assertEquals(main(['-ra', 'print', self.temp_dir]),
                          self.wrapInNormalExecution([self.temp_dir,], []),
                          )

    def testDuplicateInSameDir(self):
        """Basic test onto file A, its duplicate B, in the same directory"""
        a = self.addFile("a", self.temp_dir, 200)
        b = self.addFile("b", self.temp_dir, like='a')
        self.assertEquals(main(['-ra', 'print', self.temp_dir]),
                          self.wrapInNormalExecution([self.temp_dir,],
                                                     [interface_texts.FILE_IS_DUPLICATE % (b, a),]),
                          )

    def testDuplicateInAnotherDir(self):
        """Basic test onto file A, its duplicate B, in different directories"""
        d1 = self.mkDir('d1')
        d2 = self.mkDir('d2')
        a = self.addFile("a", d1, 200)
        b = self.addFile("b", d2, like='a')
        self.assertEquals(main(['-ra', 'print', self.temp_dir]),
                          self.wrapInNormalExecution([self.temp_dir,],
                                                     [interface_texts.FILE_IS_DUPLICATE % (b, a),]),
                          )

    def testThatTooSmallDuplicatesAreIgnored(self):
        """Test on file A and its duplicate B, both too small to be checked"""
        a = self.addFile("a", self.temp_dir, 200)
        b = self.addFile("b", self.temp_dir, like='a')
        self.assertEquals(main(['-ra', 'print', '--min-size=400', self.temp_dir]),
                          self.wrapInNormalExecution([self.temp_dir,], []),
                          )

suites = []

suites.append(unittest.TestLoader().loadTestsFromTestCase(TestBasicOperations))

alltests = unittest.TestSuite(suites)