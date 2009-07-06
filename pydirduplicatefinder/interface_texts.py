# -*- coding: utf-8 -*-

STARTING_CHECKING_MSG = "Starting checking directories %s"
ENDING_NORMALLY_MSG = "\nCompleted"

FILE_IS_DUPLICATE = "The file %s is a duplicate of %s"
PATH_IS_NOT_VALID_DIR = "The path %s doesn't match a valid directory; ignoring it."

RENAMING_DUPLICATE = "  Renaming duplicate %s to %s"
MOVING_DUPLICATE = "  moving duplicate %s to %s"

SKIPPING_EMPTY = "skipping \"%s\"; is an empty file"
SKIPPING_TOO_SMALL = "skipping \"%s\"; is too small (%s bytes)."

# Asking for user action
ASK_MESSAGE_OPTION = """Do you want to:
  (s) - Skip and continue
  (d) - Delete one of the two files
  (r) - Rename one of the two files
  (m) - Move one of the two files
  (q) - Quit
"""

ASK_INPUT = "Insert your choice: "
NON_VALID_CHOICE = "Choice %s is invalid. Please retry."

ASK_MESSAGE_SELECTION = """Select one of the files:
  (1) - %s
  (2) - %s
"""

NON_VALID_SELECTION = "Selection %s is invalid. Please insert 1 for the original file, 2 for the duplicate."

ASK_INPUT_RENAME = "Insert the new name for '%s' file: "
ERROR_FILE_EXISTS = "  ERROR. File '%s' already exists. Rename operation failed."
ASK_INPUT_MOVE = "Insert the new path for '%s' file: "
DIRECTORY_NOT_EXISTS = "  ERROR. Directory '%s' not exists. Move operation failed."

NO_DIRS_TO_CHECK_LEFT = "No directories to check. Nothing done."

#                               80 chars                                       #
HELP_FINAL_INFOS = """
Report bugs (and suggestions) to <luca@keul.it>.
"""
