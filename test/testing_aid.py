import os
import sys

def moveDirToSrcFolder() -> None:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

def thing():
    print("Hello")