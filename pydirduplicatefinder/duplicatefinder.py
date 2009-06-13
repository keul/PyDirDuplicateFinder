#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
import sys, optparse
import shutil
import filecmp

version = "1.0.0"
description = ("Analyse all files in one or more directories and manage duplicate files "
               "(the same file present with different names)")

ACTION_CHOICES = ('print','rename','move',)
SECRET_ACTION_CHOISES = ('tests',)

options = None
arguments = None
output = None

duplicates = []

def message(text, mandatory=False):
    """Print, or not, a message to stdout based onto program arguments preferences.
    @mandatory: if True and the --verbose options is not set, the message will be not printed.
    """
    global output
    if options.quiet:
        return
    if mandatory and not options.verbose:
        return

    if output is not None:
        output+=text+"\n"
    else:
        print text

def _manageDuplicate(duplicate, original, action):
    """Choose what to do finding a duplicate"""
    if action=='print' or options.verbose:
        message("The file %s is a duplicate of %s" % (duplicate['path'], original['path']))
    if action=='rename':
        prefix = options.prefix
        newName = str(prefix) + str( duplicate['name'])
        message("  Renaming duplicate %s to %s" % (duplicate['path'], newName))
        os.rename(duplicate['path'], os.path.join(os.path.dirname(duplicate['path']),newName))
    elif action=='move':
        # I only memoize duplicates for now, so I can move them later and I'm not forced to manage strange loop
        # (if I choose a target directory inside the checked directories)
        duplicates.append(duplicate)


def recurse_dir(dir):
    """List files all files inside dir, recursively"""
    dirs = os.walk(dir)
    all_files = []
    for dirpath, dirnames, filenames in dirs:
        files_in = []
        for f in filenames:
            joined = os.path.join (dirpath, f)
            all_files.append(joined)
    return all_files


def main(args=[]):
    """Main function.
    @args: used in test environment, to simulate different command line calls. Default is sys.argv[1:]
    """
    usage = "usage: %prog [options] [directories]"
    p = optparse.OptionParser(usage=usage, version="%prog " + version, description=description, prog="dirduplicatefinder.py")
    p.add_option('--action', '-a', default="print", action="store", choices=ACTION_CHOICES+SECRET_ACTION_CHOISES, help='Choose an action to do when a duplicate is found. Valid options are %s; print is the default.' % ','.join(ACTION_CHOICES))
    p.add_option('--recursive', '-r', action="store_true", default=False, help='Also check files in subdirectories recursively.')
    #p.add_option('--recursion-level', '-l', default=0, help="When the --recursive option is used, you can also set the maximum deep to explore. This value to 0 (the default) is for no limit.")
    p.add_option('--prefix', '-p', default="DUPLICATED", help="Prefix used for renaming duplicated files when the 'rename' action is chosen. Default is \"DUPLICATED\".")
    p.add_option('--move-path', '-m', dest="move_to", default=None, metavar="PATH", help="The directory where duplicate will be moved when the 'move' action is chosen.")
    p.add_option('--min-size', '-s', dest="min_size", default=10, help='Indicate the min size in byte of a file to be checked. Default is 10. Empty file are always ignored.')
    p.add_option('--verbose', '-v', action="store_true", default=False, help='More verbose output.')
    p.add_option('--quiet', '-q', action="store_true", default=False, help='Do not print any messages at all.')

    global options
    global arguments
    global output
    if args:
        # Explicit argument passed; not not print output but save it in the output string
        output = ''
    args = args or sys.argv[1:]
    options, arguments = p.parse_args(args)
    
    action = options.action

    if action=='tests':
        testrunner()
        return
    
    dir_paths = arguments or ['.']

    try:
        min_size = int(options.min_size)
    except ValueError:
        print "The --min-size options must be an integer"
        sys.exit(1)
    if min_size<=0:
        print "The --min-size options must a positive value"
        sys.exit(1)

    if action=='move' and not options.move_to:
        print "\nYou must specify the --move-path option with the 'move' action"
        sys.exit(1)

    if action=='print' and options.quiet:
        print "\nDone nothing! You can't choose to only print results and also using the quiet mode!"
        sys.exit(1)        

    valid_dir_paths = []
    for dir_path in dir_paths:
        if not os.path.isdir(dir_path):
            message("The path %s doesn't match a valid directory; ignoring it." % dir_path)
        else:
            valid_dir_paths.append(dir_path)
    dir_paths = valid_dir_paths

    message("Starting checking directories %s" % ", ".join(dir_paths))

    try:
        # phase 1 - walking directories
        message("Phase 1: walking directories", mandatory=True)
        files = []
        for dir_path in dir_paths:
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
    
        # phase 2 - sorting by size
        message("Phase 2: sorting by size", mandatory=True)
        files.sort(lambda x, y: int(x['size']-y['size']))
    
        # phase 3 - iterate files and seek only file with same size
        message("Phase 3: seek files with same size", mandatory=True)
        last_checked = {'name': '', 'path' : '', 'size': -1}
        for file in files:
            if file['size']==0:
                message("skipping \"%s\"; is an empty file" % file['path'], mandatory=True)
                continue
            if file['size']<min_size:
                message("skipping \"%s\"; is too small (%s bytes)." % (file['path'], file['size']), mandatory=True)
                continue            
            if file['size']==last_checked['size']:
                # warning: two files with the same size
                if filecmp.cmp(file['path'], last_checked['path'], shallow=False):
                    _manageDuplicate(file, last_checked, action=action)
            else:
                # a new original file has been found
                last_checked = file
    
        # Now, if I choosed the move action, I need to really move files.
        if duplicates and options.action=='move':
            message("Phase 4: moving files away", mandatory=True)
            dest = options.move_to
            for duplicate in duplicates:
                message("  moving duplicate %s to %s" % (duplicate['path'], dest))
                shutil.move(duplicate['path'], dest)

        message("\nCompleted")

    except KeyboardInterrupt:
        message("\nTerminated by user action")
    
    if output is not None:
        return output

def testrunner():
    from pydirduplicatefinder import tests as pddf_tests
    import unittest
    unittest.TextTestRunner(verbosity=2).run(pddf_tests.test_functions.alltests)


if __name__ == "__main__":
    main()


