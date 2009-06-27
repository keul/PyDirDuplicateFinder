Introduction
============

This application help you cleaning your filesystem from duplicate files. The duplicate meaning here is:
*two or more files have the same content but can have different names*.

You can use it in this way::

    Usage: pydirduplicatefinder.py [options] [directory]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -a ACTION, --action=ACTION
                            Choose an action to do when a duplicate is found.
                            Valid options are print,rename,move; print is the
                            default.
      -r, --recursive       Also check files in subdirectories recursively.
      -p PREFIX, --prefix=PREFIX
                            Prefix used for renaming duplicated files when the
                            'rename' action is chosen.
      -m PATH, --move-path=PATH
                            The directory where duplicate will be moved when the
                            'move' action is chosen.
      -s MIN_SIZE, --min-size=MIN_SIZE
                            Indicate the min size in byte of a file to be checked.
                            Default is 128. Empty file are always ignored.

TODO
====

 * A way to specify filters (regexp? jolly chars?), to include/exclude files or directories by name.
 * More tests coverage.
 * Controls recursion maximum depth.
 * Internationalization (at least italian).
 * A "move to trash" action (dependency on trash-cli?).

Credits
=======

 * Thanks to **Lord Epzylon** for sending me some code and modifications.

Subversion and other
====================

The SVN repository is hosted at the `Keul's Python Libraries`__

__ https://sourceforge.net/projects/kpython-utils/

