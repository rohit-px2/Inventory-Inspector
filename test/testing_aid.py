import os
import sys


def moveDirToSrcFolder() -> None:
    ''' Moves the parent directory to the "src" folder. This enables the importing
    of the source code modules. \n
    Requires: "src" is a child folder in the parent directory and must exist.'''
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
    