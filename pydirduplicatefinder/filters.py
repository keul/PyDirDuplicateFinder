# -*- coding: utf-8 -*-

import fnmatch
import os

def matchPatterns(path, patterns):
    """Check if the file/directory at the given path match at least one
    of the patterns.
    @path: a path to a file or directory
    @patterns: a list of possible patterns to check
    @return: True id the file/directory name at path match one of the patterns. False otherwise.
    """
    name = os.path.basename(path)
    for p in patterns:
        if fnmatch.fnmatch(name, p):
            return True
    return False