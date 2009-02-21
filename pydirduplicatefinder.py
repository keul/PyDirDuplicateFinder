#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
import sys, optparse
import shutil

version = "0.2.0"
description="Analyse all files in a directory and manage duplicate files (the same file present with different names)"

BUFFER_SIZE = 500000
ACTION_CHOICES = ('print','rename','move')

duplicates = []

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
                # I'm at the end of the file, without finding any difference
                return True
    finally:
        fh1.close()
        fh2.close()

def _manageDuplicate(duplicate, original, action):
    if action=='rename':
        prefix = options.prefix
        newName = str(prefix) + str( duplicate['name'])
        print "  Renaming duplicate %s to %s" % (duplicate['path'], newName)
        os.rename(duplicate['path'], os.path.join(os.path.dirname(duplicate['path']),newName))
    elif action=='move':
        if not options.move_to:
            print "\nYou must specify the --move-path option with the 'move' action"
            sys.exit(1)
        # I only memoize duplicates for now, so I can move them later and I'm not forced to manage strange loop
        # (if I choose a target directory inside the checked directories)
        duplicates.append(duplicate)
    else:
        print "The file %s is a duplicate of %s" % (duplicate['path'], original['path'])


def recurse_dir(dir):
    """List files all files inside dir, recursively"""
    dirs = os.walk(dir)
    all_files = []
    for dirpath, dirnames, filenames in dirs:
        files_in = []
        for f in filenames:
            joined = os.path.join (dirpath, f)
            all_files.append(joined)
#        # Now recurse into other subdirs
#        for d in dirnames:
#            all_files.extend(recurse_dir(os.path.join (dirpath, d)))
    return all_files

if __name__ == "__main__":

    usage = "usage: %prog [options] [directory]"
    p = optparse.OptionParser(usage=usage, version="%prog " + version, description=description, prog="pydirduplicatefinder.py")
    p.add_option('--action', '-a', default="print", action="store", choices=ACTION_CHOICES, help='Choose an action to do when a duplicate is found. Valid options are %s; print is the default.' % ','.join(ACTION_CHOICES))
    p.add_option('--recursive', '-r', action="store_true", default=False, help='Also check files in subdirectories recursively.')
    p.add_option('--prefix', '-p', default="DUPLICATED", help="Prefix used for renaming duplicated files when the 'rename' action is chosen.")
    p.add_option('--move-path', '-m', dest="move_to", default=None, metavar="PATH", help="The directory where duplicate will be moved when the 'move' action is chosen.")
    p.add_option('--min-size', '-s', dest="min_size", default=10, help='Indicate the min size in byte of a file to be checked. Default is 10. Empty file are always ignored.')
    options, arguments = p.parse_args()
    
    action = options.action or ACTION_CHOICES[0]
    dir_path = os.getcwd()
    if arguments:
        dir_path = arguments[0]

    try:
        min_size = int(options.min_size)
    except ValueError:
        print "The --min-size options must be an integer"
        sys.exit(1)
    if min_size<=0:
        print "The --min-size options must a positive value"
        sys.exit(1)

    print "Starting checking directory %s" % dir_path

    if not os.path.isdir(dir_path):
        print "The path %s doesn't match a directory"

    files = []
    if options.recursive:
       entries =  recurse_dir(dir_path)
       for entry_path in entries:
           stats = os.stat(entry_path)
           entry = os.path.basename(entry_path)
           files.append({'name': entry, 'path' : entry_path, 'size': stats.st_size}) 
    else:
        entries = os.listdir(dir_path)
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
            print "skipping \"%s\" that is an empty file" % file['path']
            continue
        if file['size']<min_size:
            print "skipping \"%s\" that is too small (%s bytes)." % (file['path'], file['size'])
            continue            
        if file['size']==last_checked['size']:
            # warning: two files with the same size
            if _same_file(file['path'], last_checked['path']):
                _manageDuplicate(file, last_checked, action=action)
        else:
            # a new original file has been found
            last_checked = file

    # Now, if I choosed the move action, I need to really move files.
    if duplicates and options.action=='move':
        dest = options.move_to
        for duplicate in duplicates:
            print "  moving duplicate %s to %s" % (duplicate['path'], dest)
            shutil.move(duplicate['path'], dest)

    print "Completed"
