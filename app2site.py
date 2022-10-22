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

def build_flutterapp(fldr, base_href=None):
    print(f"Executing flutter build for {fldr}")
    print(os.listdir(fldr))
    with chdir(fldr):
        cmd = f'flutter build web --release'
        if base_href:
            cmd = f'flutter build web --release --base-href "{base_href}"'
        cmdlist = shlex.split(cmd)
        is_windows = sys.platform.startswith('win')
        out = subprocess.run(cmdlist, capture_output=True, text=True, shell=is_windows)
        print(out)


def app2site():
    print("Running Post Script")
    app_dirs = subdirs("apps")
    flutter_dirs = subdirs("flutter")
    sel_dirs = [dirname for dirname in app_dirs if dirname in flutter_dirs]
    for dirname in sel_dirs:
        build_flutterapp(os.path.abspath(os.path.join("flutter", dirname)), base_href= f"/apps/{dirname}/")
        src = os.path.join("flutter", dirname, "build", "web")
        dst = os.path.join("_site", "apps", dirname)
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"Finished copying from {src} to {dst}")

if __name__=='__main__':
    app2site()
