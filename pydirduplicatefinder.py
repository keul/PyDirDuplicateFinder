#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
import sys, optparse

version = "0.1.1"
description="Analyse all files in a directory and manage duplicate files (the same file present with different names)"

BUFFER_SIZE = 500000
ACTION_CHOICES = ('print','rename')

def _same_file(filepath1, filepath2):
    """Check if those 2 file (of the same size) are equals"""
    fh1 = open(filepath1, 'r')
    fh2 = open(filepath2, 'r')
    try:
        while True:
            part1 = str(fh1.read(BUFFER_SIZE))
            part2 = str(fh2.read(BUFFER_SIZE))
            if part1!=part2:
                return False
            if not part1:
                # I'm at the end of the file, without find any difference
                return True
    finally:
        fh1.close()
        fh2.close()

def _manageDuplicate(duplicate, original, action='print'):
    print "The file %s is a duplicate of %s" % (duplicate['name'], original['name'])
    if action=='rename':
        newName = "DUPLICATE%s" % duplicate['name']
        print "  Renaming duplicate %s to %s" % (duplicate['name'], newName)
        #print os.path.join(os.path.dirname(duplicate['path']),newName)
        os.rename(duplicate['path'], os.path.join(os.path.dirname(duplicate['path']),newName))

if __name__ == "__main__":

    usage = "usage: %prog [options] [directory]"
    p = optparse.OptionParser(usage=usage, version="%prog " + version, description=description, prog="PyDirDuplicateFinder")
    p.add_option('--action', '-a', default="print", action="store", choices=ACTION_CHOICES, help='Choose an action to do when a duplicate is found. Valid options are %s; print is the default.' % ','.join(ACTION_CHOICES))
    options, arguments = p.parse_args()
    
    action = options.action or ACTION_CHOICES[0]
    
    dir_path = os.getcwd()
    if arguments:
        dir_path = arguments[0]
    
    if not os.path.isdir(dir_path):
        print "The path %s doesn't match a directory"
    
    entries = os.listdir(dir_path)
    files = []
    for entry in entries:
        entry_path = os.path.join(dir_path, entry)
        if not os.path.isdir(entry_path):
            stats = os.stat(entry_path)
            files.append({'name': entry, 'path' : entry_path, 'size': stats.st_size})
    
    # phase 1 - sorting by file size
    files.sort(lambda x, y: int(x['size']-y['size']))

    # phase 2 - iterate file and seek only file with same size
    last_checked = {'name': '', 'path' : '', 'size': -1}
    for file in files:
        if file['size']==0:
            print "skipping \"%s\" that is an empty file" % file['name']
            continue
        if file['size']==last_checked['size']:
            # warning: two files with the same size
            if _same_file(file['path'], last_checked['path']):
                _manageDuplicate(file, last_checked, action=action)
        else:
            # a new original file has been found
            last_checked = file

