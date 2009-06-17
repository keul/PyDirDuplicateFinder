# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import os
import os.path
import sys, optparse
import shutil
import unittest

import tempfile

from pydirduplicatefinder import interface_texts

class PyDirDuplicateFinderTestCase(unittest.TestCase):
    """My own extension of the base TestCase class"""
    
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        self.temp_dir = None
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def wrapInNormalExecution(self, dirs, text):
        dirs_text = ', '.join(dirs)
        return interface_texts.STARTING_CHECKING_MSG % dirs_text + "\n" + \
               text + \
               interface_texts.ENDING_NORMALLY_MSG+"\n"

    def mkDir(self, name=None, prefix='tmp'):
       """Create a test directory inside the temp directory"""
       if name:
           path = os.path.join(self.temp_dir, name)
           os.mkdir(path)
           return path
       return tempfile.mkdtemp(prefix=prefix, dir=self.temp_dir)

