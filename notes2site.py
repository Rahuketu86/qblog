import os
import shutil
import subprocess
import contextlib
import subprocess
import shlex
import sys


def subdirs(fldr):
    dirnames = []
    for pth in os.listdir(fldr):
         if os.path.isdir(os.path.join(fldr, pth)):
            dirnames.append(pth)
    return dirnames

@contextlib.contextmanager
def chdir(target):
    try:
        start = os.getcwd()
        os.chdir(target)
        yield

    finally:
        os.chdir(start)


def notes2site():
    src = os.path.join("_logseq", "publish")
    dst = os.path.join("_site", "notes")
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"Finished copying from {src} to {dst}")

if __name__=='__main__':
    notes2site()
