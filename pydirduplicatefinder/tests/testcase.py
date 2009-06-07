# -*- coding: utf-8 -*-

__author__ = "Keul - lucafbb AT gmail.com"

import os
import os.path
import sys, optparse
import shutil
import unittest

import tempfile

class PyDirDuplicateFinderTestCase(unittest.TestCase):
    """My own extension of the base TestCase class"""
    
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        self.temp_dir = None
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)