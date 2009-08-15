# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

from os.path import basename
import unittest
from testcase import PyDirDuplicateFinderTestCase

from pydirduplicatefinder import interface_texts
from duplicatefinder import main

class TestPathFilters(PyDirDuplicateFinderTestCase):
    
    def testDirectDirectoryNameSkippingFile1(self):
        """Test passing a single directory name to --include-dir option"""
        # File in d1 is ignored
        d1 = self.mkDir('Lorem')
        d2 = self.mkDir('Ipsum')
        d3 = self.mkDir('Dolor')
        self.addFile("a", d1, 200)
        self.addFile("a", d2)
        d2name = basename(d2)
        self.assertEquals(main(['--include-dir=%s' % d2name, d1, d2, d3, ]),
                          self.wrapInNormalExecution([d2,], []),
                          )

    def testDirectDirectoryNameSkippingFile2(self):
        """Test passing a single directory name to --include-dir option, but with a duplicate"""
        d1 = self.mkDir('Lorem')
        d2 = self.mkDir('Ipsum')
        d3 = self.mkDir('Dolor')
        self.addFile("a", d1, 200)
        a = self.addFile("a", d2)
        b = self.addFile("b", d2, like="a")
        d2name = basename(d2)
        self.assertEquals(main(['--include-dir=%s' % d2name, d1, d2, d3, ]),
                          self.wrapInNormalExecution([d2,],
                                                     [interface_texts.FILE_IS_DUPLICATE % (b, a),]),
                          )

    def testDirectDirectoriesName(self):
        """Test passing 2 --include-dir option, with 2 dirs name"""
        d1 = self.mkDir('Lorem')
        d2 = self.mkDir('Ipsum')
        d3 = self.mkDir('Dolor')
        d1name = basename(d1)
        d2name = basename(d2)
        self.assertEquals(main(['--include-dir=%s' % d1name, '--include-dir=%s' % d2name, d1, d2, d3]),
                          self.wrapInNormalExecution([d2, d1], []),
                          )

    def testDirectDirectoriesNameAndDuplicate(self):
        """Test passing 2 --include-dir option, and 4 duplicates (1 ignored)"""
        d1 = self.mkDir('Lorem')
        a = self.addFile("a", d1, size=200)
        d2 = self.mkDir('Ipsum')
        b = self.addFile("b", d2, like='a')
        c = self.addFile("c", d2, like='b')        
        d3 = self.mkDir('Dolor')
        self.addFile("a", d3)
        d1name = basename(d1)
        d2name = basename(d2)
        self.assertEquals(main(['--include-dir=%s' % d1name, '--include-dir=%s' % d2name, d1, d2, d3]),
                          self.wrapInNormalExecution([d2, d1],
                                                     [interface_texts.FILE_IS_DUPLICATE % (c, b),
                                                      interface_texts.FILE_IS_DUPLICATE % (a, b)]),
                          )

    def testDirectDirectoriesNameWithRecursion(self):
        """Test a duplicate in a subdirectory is ignored with --include-dir with recursion"""
        d1 = self.mkDir('d1')
        a = self.addFile("a", d1, size=200)
        d2 = self.mkDir('d2', d1)
        b = self.addFile("a", d2)
        d1name = basename(d1)
        self.assertEquals(main(['-r','--include-dir=%s' % d1name, d1, ]),
                          self.wrapInNormalExecution([d1], []),
                          )

    def testDirectDirectoriesNameWithJollyChar(self):
        """Test a duplicate is ignored when usage of --include-dir exclude it; using jolly chars"""
        dira = self.mkDir('dira')
        a = self.addFile("a", dira, size=200)
        dirb = self.mkDir('dirb')
        b = self.addFile("a", dirb)
        cdir = self.mkDir('cdir')
        c = self.addFile("a", cdir)
        self.assertEquals(main(['--include-dir=di*', dira, dirb, cdir]),
                          self.wrapInNormalExecution([dira, dirb],
                                                     [interface_texts.FILE_IS_DUPLICATE % (b, a)]),
                          )

    def testIncludeEquality(self):
        """Test that --include-dir=Car and --include-dir=Carlos is the same as --include-dir=Car*"""
        carl = self.mkDir('Carl')
        a = self.addFile("a", carl, size=200)
        carlos = self.mkDir('Carlos')
        b = self.addFile("a", carlos)
        self.assertEquals(main(['--include-dir=Carl', '--include-dir=Carlos', carl, carlos]),
                          main(['--include-dir=Carl*', carl, carlos]),
                          )

    def testIncludeExcludeDirectoriesAtSametime(self):
        """Test a filter using both --include-dir and --exclude-dir"""
        carl = self.mkDir('Carl')
        a = self.addFile("a", carl, size=200)
        carlos = self.mkDir('Carlos')
        b = self.addFile("a", carlos)
        carles = self.mkDir('Carles', carl)
        c = self.addFile("a", carles)
        carlis = self.mkDir('Carlis')
        d = self.addFile("a", carlis)        
        self.assertEquals(main(['-r','--include-dir=Carl*', '--exclude-dir=Carles', carl, carlos]),
                          self.wrapInNormalExecution([carl, carlos],
                                                     [interface_texts.FILE_IS_DUPLICATE % (b, a)]),
                          )
        self.assertEquals(main(['-r','--include-dir=Carl*', '--exclude-dir=Carles', carl, carlos, carlis]),
                          self.wrapInNormalExecution([carl, carlis, carlos],
                                                     [interface_texts.FILE_IS_DUPLICATE % (d, a),
                                                      interface_texts.FILE_IS_DUPLICATE % (b, a)]),
                          )

    def testIncludeExcludeFiles(self):
        """Test usage of --include-file and --exclude-file"""
        loris = self.addFile("loris", self.temp_dir, size=200)
        laris = self.addFile("laris", self.temp_dir, like="loris")
        liris = self.addFile("liris", self.temp_dir, like="loris")
        self.assertEquals(main(['--include-file=l?ris', '--exclude-file=li*', self.temp_dir]),
                          self.wrapInNormalExecution([self.temp_dir],
                                                     [interface_texts.FILE_IS_DUPLICATE % (loris, laris)]),
                          )


suites = []

suites.append(unittest.TestLoader().loadTestsFromTestCase(TestPathFilters))

alltests = unittest.TestSuite(suites)