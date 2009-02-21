Introduction
============

This application help you cleaning your filesystem from duplicate files. The duplicate meaning here is:
*the same file is present with different names*.

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
                            Default is 10. Empty file are always ignored.

TODO
====

 * Work on more that a folder.
 * A way to specify filters, to skip files or directory.

Credits
=======

 * Thanks to **Lord Epzylon** for sending me some code and modifications.

Subversion and other
====================

The SVN repository is hosted at the `Keul's Python Libraries`__

__ https://sourceforge.net/projects/kpython-utils/

