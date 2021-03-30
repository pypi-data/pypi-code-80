import argparse
import os
import subprocess

from .__about__ import __author__, __author_email__, __version__, __website__

try:
    import ptvsd
    DEBUGGER_LOADED = True
    def start_debugger(timeout_sec=None):
        if not ptvsd.is_attached():
            # 5678 is the default attach port in the VS Code debug configurations
            print("Waiting for debugger attach from VsCode")
            ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
            ptvsd.wait_for_attach(timeout_sec)
except ImportError:
    DEBUGGER_LOADED = False

def dir_logic(pyfile):
    dirname = os.path.dirname(pyfile)
    if dirname:
        base_dir = os.getcwd()
        full_path = os.path.join(base_dir, dirname)
        cmd = "import sys; sys.path.append('{0}'); ".format(full_path)
    else:
        cmd = ""
    return cmd


def run(pyfile, function, debugger=False):

    cmd = dir_logic(pyfile)
    base_file_name = os.path.basename(pyfile).split(".")[0]

    if debugger:
        # start_debugger()
        cmd_db = """
import ptvsd
def start_debugger(timeout_sec=None):
    if not ptvsd.is_attached():
        # 5678 is the default attach port in the VS Code debug configurations
        print("Waiting for debugger attach from VsCode")
        ptvsd.enable_attach(address=('localhost', 5678))
        ptvsd.wait_for_attach(timeout_sec)
start_debugger()
"""
        print('Using debugger mode')
        cmd += cmd_db
    

    command = cmd + "import {0}; {0}.{1}()".format(base_file_name, function)

    subprocess.call(["python", "-c", command])


def main():

    parser = argparse.ArgumentParser(description="Run apython functions inside a file from the command line")
    parser.add_argument("pyfile", type=str, help="Python file")
    parser.add_argument("function", type=str, help="Python function")
    parser.add_argument("-b", "--debugger", action='store_true', help="Use VSCode Debugger")
    args = parser.parse_args()
    
    if args.debugger and (not DEBUGGER_LOADED):
        print('Please install ptvsd for vscode debugging.')

    run(args.pyfile, args.function, args.debugger)

    return


__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__website__",
    "main",
]
