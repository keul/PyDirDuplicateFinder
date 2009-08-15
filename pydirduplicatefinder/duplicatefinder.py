#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
import sys, optparse
import shutil
import filecmp

from pydirduplicatefinder import interface_texts
from pydirduplicatefinder.raw_input_defaulted import raw_input_defaulted

from pydirduplicatefinder import filters

version = "0.3.0"
description = ("Analyse all files in one or more directories and manage duplicate files "
               "(the same file present with different names)")

ACTION_CHOICES = ('print','rename','move','ask')
SECRET_ACTION_CHOISES = ('tests',)

VALID_CHOICES = ('s', 'd', 'r', 'm', 'q', )

options = None
arguments = None
output = None
last_checked = {}

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
        message(interface_texts.FILE_IS_DUPLICATE % (duplicate['path'], original['path']))
    if action=='rename':
        prefix = options.prefix
        newName = str(prefix) + str( duplicate['name'])
        message(interface_texts.RENAMING_DUPLICATE % (duplicate['path'], newName))
        os.rename(duplicate['path'], os.path.join(os.path.dirname(duplicate['path']),newName))
    elif action=='move':
        # I only memoize duplicates for now, so I can move them later and I'm not forced to manage strange loop
        # (if I choose a target directory inside the checked directories)
        duplicates.append(duplicate)
    elif action=='ask':
        _askForUserAction(duplicate, original)

def _askForUserAction(duplicate, original):
    """Ask to the user what to do with duplicate"""
    message("\n" + interface_texts.FILE_IS_DUPLICATE % (duplicate['path'], original['path']))
    message(interface_texts.ASK_MESSAGE_OPTION)
    valid_choice = False
    while (not valid_choice):
        choice = raw_input(interface_texts.ASK_INPUT)
        valid_choice = choice in VALID_CHOICES
        if not valid_choice:
            message(interface_texts.NON_VALID_CHOICE % choice)
    # I've the choice, lets do something
    if choice=='q':
        raise KeyboardInterrupt()
    elif choice=='s':
        return
    #elif choice=='d' or choice=='r' or choice=='m':
    # I need to choose one of the two files
    message(interface_texts.ASK_MESSAGE_SELECTION % (original['path'], duplicate['path']))
    valid_selection = False
    while (not valid_selection):
        selection = raw_input(interface_texts.ASK_INPUT)
        valid_selection = selection in ('1', '2')
        if not valid_selection:
            message(interface_texts.NON_VALID_SELECTION % selection)
    # I have the choice and the selection, now REALLY do something!
    if choice=='d':
        response = manage_delete(original, duplicate, selection)
    elif choice=='r':
        response = manage_rename(original, duplicate, selection)
    elif choice=='m':
        response = manage_move(original, duplicate, selection)
    message(response or "Done.")

def manage_delete(original, duplicate, selection):
    """Delete the original (or the duplicate) file looking at selection parameter"""
    global last_checked
    if selection=='1':
        # Delete the original; the duplicate become the new original
        os.remove(original['path'])
        last_checked = duplicate
    else:
        # Delete the duplicate
        os.remove(duplicate['path'])

def manage_rename(original, duplicate, selection):
    """Rename the original (or the duplicate) file looking at selection parameter"""
    global last_checked
    prefix = options.prefix
    if selection=='1':
        # Rename the original; change all the last_checked structure
        file_name = os.path.basename(original['path'])
        dir_name = os.path.dirname(original['path'])
        new_name = raw_input_defaulted(interface_texts.ASK_INPUT_RENAME % file_name, default=prefix+file_name)
        if os.path.exists(os.path.join(dir_name, new_name)):
            return interface_texts.ERROR_FILE_EXISTS % new_name
        os.rename(os.path.join(dir_name, file_name), os.path.join(dir_name, new_name))
        last_checked = {'name': new_name, 'path' : os.path.join(dir_name, new_name), 'size': last_checked['size']}
    else:
        # Rename the duplicate
        file_name = os.path.basename(duplicate['path'])
        dir_name = os.path.dirname(duplicate['path'])
        new_name = raw_input_defaulted(interface_texts.ASK_INPUT_RENAME % file_name, default=prefix+file_name)
        if os.path.exists(os.path.join(dir_name, new_name)):
            return interface_texts.ERROR_FILE_EXISTS % new_name
        os.rename(os.path.join(dir_name, file_name), os.path.join(dir_name, new_name))

def manage_move(original, duplicate, selection):
    """Move the original (or the duplicate) file looking at selection parameter"""
    global last_checked
    if selection=='1':
        # Move the original; change all the last_checked structure
        file_name = os.path.basename(original['path'])
        dir_name = os.path.dirname(original['path'])
        file_path = original['path']
        new_dir = raw_input_defaulted(interface_texts.ASK_INPUT_MOVE % file_name, default=dir_name)
        if not os.path.exists(new_dir) or not os.path.isdir(new_dir):
            return interface_texts.DIRECTORY_NOT_EXISTS % new_dir
        new_path = os.path.join(new_dir, file_name)
        os.rename(file_path, new_path)
        last_checked = {'name': last_checked['name'], 'path' : new_path, 'size': last_checked['size']}
    else:
        # Rename the duplicate
        file_name = os.path.basename(duplicate['path'])
        dir_name = os.path.dirname(duplicate['path'])
        file_path = duplicate['path']
        new_dir = raw_input_defaulted(interface_texts.ASK_INPUT_MOVE % file_name, default=dir_name)
        if not os.path.exists(new_dir) or not os.path.isdir(new_dir):
            return interface_texts.DIRECTORY_NOT_EXISTS % new_dir
        new_path = os.path.join(new_dir, file_name)
        os.rename(file_path, new_path)

def recurse_dir(directory):
    """List all files inside a directory, recursively"""
    dirs = os.walk(directory)
    all_files = []
    for dirpath, dirnames, filenames in dirs:
        if options.include_dirs:
            dirnames[:] = [d for d in dirnames if filters.matchPatterns(d, options.include_dirs)]
        if options.exclude_dirs:
            dirnames[:] = [d for d in dirnames if not filters.matchPatterns(d, options.exclude_dirs)]
        dirnames[:] = sorted(dirnames) # BBB: in facts this is needed only for tests purposes
        files_in = []
        filenames.sort()
        for f in filenames:
            joined = os.path.join (dirpath, f)
            all_files.append(joined)
    return all_files


def main(args=[]):
    """Main function.
    @args: used in test environment, to simulate different command line calls. Default is sys.argv[1:]
    """
    usage = "usage: %prog [options] [directories]"
    p = optparse.OptionParser(usage=usage, version="%prog " + version, description=description, prog="duplicatefinder.py")

    p.remove_option("--help")
    p.add_option('--help', '-h', action="store_true", default=False, help='show this help message and exit')
    
    p.add_option('--action', '-a', default="print", action="store", choices=ACTION_CHOICES+SECRET_ACTION_CHOISES, help='choose an action to do when a duplicate is found. Valid options are %s; print is the default' % ','.join(ACTION_CHOICES))
    p.add_option('--recursive', '-r', action="store_true", default=False, help='also check files in subdirectories recursively')
    #p.add_option('--recursion-level', '-l', type="int", default=0, help="when the --recursive option is used, you can also set the maximum deep to explore. This value to 0 (the default) is for no limit")
    p.add_option('--prefix', '-p', default="DUPLICATED", help="prefix used for renaming duplicated files when the 'rename' action is chosen. Default is \"DUPLICATED\"")
    p.add_option('--move-path', '-m', dest="move_to", default=None, metavar="PATH", help="the directory where duplicate will be moved when the 'move' action is chosen")
    p.add_option('--verbose', '-v', action="store_true", default=False, help='more verbose output')
    p.add_option('--quiet', '-q', action="store_true", default=False, help='do not print any messages at all')

    group = optparse.OptionGroup(p, "Filters",
                                    "Use those options to limit and filter directories and files to check.\n"
                                    "Options belowe that rely on file or directory name support usage of jolly characters "
                                    "and can also be used multiple times")

    group.add_option('--min-size', '-s', dest="min_size", type="int", default=128, help='indicate the min size in bytes of a file for being checked. Default is 128. Empty file are always ignored')
    group.add_option("--include-dir", dest="include_dirs", default=[], metavar="INCLUDE_DIR", action="append", help="only check directories with this name")
    group.add_option("--exclude-dir", dest="exclude_dirs", default=[], metavar="EXCLUDE_DIR", action="append", help="do not check directories with this name")
    group.add_option("--include-file", dest="include_files", default=[], metavar="INCLUDE_FILE", action="append", help="limit the search inside file with that name")
    group.add_option("--exclude-file", dest="exclude_files", default=[], metavar="EXCLUDE_FILE", action="append", help="ignore the search inside file with that name")

    p.add_option_group(group)

    global options
    global arguments
    global output
    global last_checked
    
    if args:
        # Explicit argument passed; not not print output but save it in the output string
        output = ''
    args = args or sys.argv[1:]
    options, arguments = p.parse_args(args)
    
    if options.help:
        p.print_help()
        print interface_texts.HELP_FINAL_INFOS
        sys.exit(0)
    
    action = options.action

    if action=='tests':
        testrunner()
        return
    
    dir_paths = arguments or ['.']
    dir_paths = [os.path.abspath(x) for x in dir_paths]

    min_size = options.min_size
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
            message(interface_texts.PATH_IS_NOT_VALID_DIR % dir_path)
        else:
            valid_dir_paths.append(dir_path)
    
    # Include only dirs that match filters (if used)
    if options.include_dirs:
        valid_dir_paths = [d for d in valid_dir_paths if filters.matchPatterns(d, options.include_dirs)]

    # Exclude dirs that do not match filters (if used)
    if options.exclude_dirs:
        valid_dir_paths = [d for d in valid_dir_paths if not filters.matchPatterns(d, options.exclude_dirs)]

    dir_paths = sorted(list(set(valid_dir_paths)))

    if not dir_paths:
        message(interface_texts.NO_DIRS_TO_CHECK_LEFT)

    message(interface_texts.STARTING_CHECKING_MSG % ", ".join(dir_paths))

    try:
        # phase 1 - walking directories
        message("Phase 1: walking directories", mandatory=True)
        files = []
        for dir_path in dir_paths:
            if options.recursive:
               entries = recurse_dir(dir_path)
               for entry_path in entries:
                   stats = os.stat(entry_path)
                   entry = os.path.basename(entry_path)
                   files.append({'name': entry, 'path' : entry_path, 'size': stats.st_size}) 
            else:
                entries = os.listdir(dir_path)
                entries.sort()
                for entry in entries:
                    entry_path = os.path.join(dir_path, entry)
                    if not os.path.isdir(entry_path):
                        stats = os.stat(entry_path)
                        files.append({'name': entry, 'path' : entry_path, 'size': stats.st_size})

        # Limit only to file name used in the include_files option
        if options.include_files:
            files = [f for f in files if filters.matchPatterns(f['path'], options.include_files)]

        # Skip files indicated using exclude_files option
        if options.exclude_files:
            files = [f for f in files if not filters.matchPatterns(f['path'], options.exclude_files)]

        # phase 2 - sorting by size
        message("Phase 2: sorting by size", mandatory=True)
        files.sort(lambda x, y: int(x['size']-y['size']))
    
        # phase 3 - iterate files and seek only file with same size
        message("Phase 3: seek files with same size", mandatory=True)
        last_checked = {'name': '', 'path' : '', 'size': -1}
        for file in files:
            if file['size']==0:
                message(interface_texts.SKIPPING_EMPTY % file['path'], mandatory=True)
                continue
            if file['size']<min_size:
                message(interface_texts.SKIPPING_TOO_SMALL % (file['path'], file['size']), mandatory=True)
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
                message(interface_texts.MOVING_DUPLICATE % (duplicate['path'], dest))
                shutil.move(duplicate['path'], dest)

        message(interface_texts.ENDING_NORMALLY_MSG)

    except KeyboardInterrupt:
        message("\nTerminated by user action")
    
    if output is not None:
        return output

def testrunner():
    from pydirduplicatefinder import tests as pddf_tests
    import unittest
    unittest.TextTestRunner(verbosity=2).run(pddf_tests.test_functions.alltests)
    unittest.TextTestRunner(verbosity=2).run(pddf_tests.test_filters.alltests)

if __name__ == "__main__":
    main()


