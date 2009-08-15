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
        self.files = {}
        self.counter = 0
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.files = {}
        self.counter = 0

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def wrapInNormalExecution(self, dirs, texts):
        dirs_text = ', '.join(dirs)
        if texts:
            texts.append('')
        return interface_texts.STARTING_CHECKING_MSG % dirs_text + "\n" + \
               "\n".join(texts) + \
               interface_texts.ENDING_NORMALLY_MSG+"\n"

    def mkDir(self, name=None, where=None, prefix='tmp'):
       """Create a test directory inside the temp directory"""
       if not where:
           where = self.temp_dir
       if name:
           path = os.path.join(where, name)
           os.mkdir(path)
           return path
       return tempfile.mkdtemp(prefix=prefix, dir=where)

    def addFile(self, name, directory_path, size=None, like=None):
       """Add a new test-temp file to a specific directory.
       The name of the file can be simple and a file with random content is created and stored in the
       PyDirDuplicateFinderTestCase.files attribute, and also created in the given path.
       Other call of addFile with the same name will use the already stored file. In those cases the
       use of the size attribute is forbidden.
       @name: name of the file
       @directory_path: path to a directory where store the file
       @size: the size in byte on the file; required only if is the first time you use this name of file,
              forbidden in every other case.
       @like: create a new file with the same content of an already generated file with given name.
       """
       files = self.files
       if size and files.has_key(name):
           raise KeyError("A file with name %s already exists (size: %s bytes). Use a different name"
                          " or don't use the size attribute to use the same file." % (name, files[name]['size']) )
       if not size and not like and not files.has_key(name):
           raise KeyError("File with name %s not found. You must give a size." % name)
       
       if like:
           # Like another file
           content = files[like]['content']
           size = files[like]['size']
       elif not like and not size:
           # Full copy of another file
           content = files[name]['content']
           size = files[name]['size']           
       else:
           # New file
           content = self.counter
           self.counter+=1
           if not size:
               size = files[name]['size']

       file_data = "%016d" % content
       file_data+="a" * (size-16)
       
       file_path = os.path.join(directory_path, name)
       f = open(file_path, "w")
       f.write(file_data)
       f.close()
       
       self.files[name] = {'size': size, 'content': content}
       return file_path
