import argparse
from .build import buildinstaller
__version__="1.0.5"
def main():
    parser = argparse.ArgumentParser(description=f'pynim (python-nsis-installer-maker) V{__version__}')
    parser.add_argument('--icon',             dest='icon',     type=str,                    default="", nargs="?",  help='the icon of application exe and the installer')
    parser.add_argument('--ver',              dest='version',  type=str,                    default="", nargs="?",  help='the version of app (shows on the title of installer)')
    parser.add_argument('--add-file',         dest='files',    type=str,                    default=[], nargs="*",  help='add files to the app (you can use it more than one)')
    parser.add_argument('--add-folder',       dest='folders',  type=str,                    default=[], nargs="*",  help='add folder to the app (you can use it more than one)')
    parser.add_argument('--add-arg',          dest='args',     type=str,                    default="", nargs="?",  help='add arguments to pyinstaller for better build')
    parser.add_argument('-s', "--small",      dest='small',    default=False,   const=True,             nargs="?",  help='smaller file size for the applicatin (may brake installer)')
    parser.add_argument('-w', "--windowed",   dest='windowed', default=False,   const=True,             nargs="?",  help='hide consule when app in openning (installer is windowd always)')
    parser.add_argument('-l', "--add-launch", dest='launch',   default=False,   const=True,             nargs="?",  help='hide consule when app in openning (installer is windowd always)')
    parser.add_argument('--name', "-n",       dest='name',     type=str,                                            help='the name of app, on the installer title and the defult directory of app')
    parser.add_argument('pythonscript',       metavar='MAIN',  type=str,                                            help='the main python file of your script')
    args = parser.parse_args()
    buildinstaller(args.pythonscript, args.name, args.files, args.folders, args.icon,args.small, args.windowed, args.version, args.args, args.launch)
    # build this app:
    # python pynim.py "pynim.py" --ver "1.0.0" --add-file "installer.nsi"
if __name__ == "__main__":
    main()