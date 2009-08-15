Introduction
============

This application help you cleaning your filesystem from duplicate files. The duplicate meaning here is:
*two or more files have the same content but can have different names*.

You can use it in this way::

	Usage: duplicatefinder.py [options] [directories]
	
	Analyse all files in one or more directories and manage duplicate files (the
	same file present with different names)
	
	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -a ACTION, --action=ACTION
	                        choose an action to do when a duplicate is found.
	                        Valid options are print,rename,move,ask; print is the
	                        default
	  -r, --recursive       also check files in subdirectories recursively
	  -p PREFIX, --prefix=PREFIX
	                        prefix used for renaming duplicated files when the
	                        'rename' action is chosen. Default is "DUPLICATED"
	  -m PATH, --move-path=PATH
	                        the directory where duplicate will be moved when the
	                        'move' action is chosen
	  -v, --verbose         more verbose output
	  -q, --quiet           do not print any messages at all
	
	  Filters:
	    Use those options to limit and filter directories and files to check.
	    Options belowe that rely on file or directory name support usage of
	    jolly characters and can also be used multiple times
	
	    -s MIN_SIZE, --min-size=MIN_SIZE
	                        indicate the min size in bytes of a file for being
	                        checked. Default is 128. Empty file are always ignored
	    --include-dir=INCLUDE_DIR
	                        only check directories with this name
	    --exclude-dir=EXCLUDE_DIR
	                        do not check directories with this name
	    --include-file=INCLUDE_FILE
	                        limit the search inside file with that name
	    --exclude-file=EXCLUDE_FILE
	                        ignore the search inside file with that name
	
	Report bugs (and suggestions) to <luca@keul.it>.

TODO
====

 * More tests coverage (maybe some tests can be merged togheter).
 * Controls recursion maximum depth.
 * Internationalization (at least italian).
 * A "move to trash" action (dependency on `trash-cli`__ can be a great idea).

__ http://pypi.python.org/pypi/trash-cli/

Credits
=======

 * Thanks to **Lord Epzylon** for sending me some code and modifications.

Subversion and other
====================

The SVN repository is hosted at the `Keul's Python Libraries`__

__ https://sourceforge.net/projects/kpython-utils/

