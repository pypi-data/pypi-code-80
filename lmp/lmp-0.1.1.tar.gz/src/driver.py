#!/usr/bin/env python


import os
import errno
import json
import subprocess
import sys
import platform
import signal

from click.decorators import option
try:
    import applescript
except ImportError:
    """This exception is expected on non apple"""


# temp = {
#     "action": "ADD",
#     "payload": {
#         "project": {
#             "title": "My project title",
#             "summary": "tbd",
#             "os": {
#                 "windows": {
#                     "path": "C:\\Users\\jacob\\Documents\\Projects\\StartMyProject",
#                     "editor-cmd": "code .",
#                     "scripts": {
#                         "cmds": [""],
#                         "bash-scripts": []
#                     }
#                 }
#             }
#         }
#     }
# }


def parseArg(args: dict):

    action = args["action"]

    if(action == "ADD"):
        return args["payload"]
    elif(action == "REMOVE"):
        return args["payload"]
    elif(action == "EDIT"):
        return args["payload"]
    elif(action == "START"):
        return args["payload"]

    print("Parsing arguments")

def determinePlatform():
    plat = platform.system()
    if plat == "Darwin":
        return "macOS"
    elif plat == "Windows":
        return "windows"
    elif plat == "Linux":
        return "linux"
    else:
        sys.exit("Unknown OS, please report. 0-0")



def create_commands():
    """Create commands"""

def __exit(message: str):
    sys.exit(message)

def edit_project(project: dict, field: str):
    project_to_add = project
    os = determinePlatform()
    
    if(project_to_add[field] != None):
        
        if(field == "title"):
            newVal = input("Enter new title. ")
            project_to_add['title'] = newVal
        elif(field == "summary"):
            newVal = input("Enter new summary. ")
            project_to_add['summary'] = newVal
        elif(project_to_add["os"][os][field] != None):
            project_to_add["os"][field] == os

            if(field == "path"):
                newVal = input("new path")
                project_to_add["os"][os]["path"] = newVal
            elif(field == "editor-cmd"):
                newVal = input("New editor cmd")
                project_to_add["os"][os]["editor-cmd"] = newVal

            elif(project_to_add["os"][os]["scripts"][field] != None):
                if(field == "cmds"):
                    newVal = input("Enter new cmd")
                    project_to_add["os"][os]["scripts"]["cmds"] = newVal
                elif(field == "cmds"):
                    newVal = input("Enter new cmd")
                    project_to_add["os"][os]["scripts"]["cmds"] = newVal
                else:
                    __exit("Invalid field")

    return project_to_add

   
def is_pathname_valid(pathname: str) -> bool:
    ERROR_INVALID_NAME = 123
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        _, pathname = os.path.splitdrive(pathname)

        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
           
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True

def write_to_projects(projects: list):
    absPath = os.path.dirname(os.path.abspath(__file__))
    with open("{}/projects.json".format(absPath), "w") as outfile:
        json.dump(projects, outfile)


def removeProject(projects: list, selected: dict):
    return [i for i in projects if not (i['title'] == selected['title'])]


def start(payload: dict):
    options = payload["options"]
    selected = payload["project"]
    title = selected["title"]
    plat = determinePlatform()
    path = None
    editor = None
    fileSys = None
    openTerminal = None

    if plat == "macOS":
        if(is_pathname_valid(selected["os"][plat]["path"])):
            path = selected["os"][plat]["path"]
        else:
            sys.exit("Invalid path provided")
        editor = selected["os"][plat]["editor-cmd"]
        fileSys = "finder"
        openTerminal = "open {}".format(path)
    elif plat == "windows":
        if(is_pathname_valid(selected["os"][plat]["path"])):
            path = selected["os"][plat]["path"]
        else:
            sys.exit("Invalid path provided")
        editor = selected["os"]["windows"]["editor-cmd"]
        fileSys = "explorer"
        openTerminal = 'start cmd.exe /k "{} && cd {}"'.format(path[:2], path)
    elif plat == "linux":
        # We are on Linux
        sys.exit("Linux is not supported yet")
    else:
        sys.exit("Unknown OS, please report. 0-0")

    limStr = "in limited mode"
    print("Loading {} {}\nFrom: $> {}\n".format(limStr,
        title, path))

    # Open Editor
    subprocess.Popen("{} {}".format(editor, path), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if(options["limited"]):
        sys.exit("")

    # Open File System
    subprocess.Popen('{} {}'.format(fileSys, path), shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Open cmd/terminal
    os.system(openTerminal)
    # Execute any scripts
    cmds = selected["os"][plat]["scripts"]["cmds"]
    if plat == "macOS":
        # We are on MacOS
        for cmd in cmds:
            script = "cd {} && {}".format(path, cmd)
            applescript.tell.app('Terminal', 'do script "' + script + '"')
    elif plat == "windows":
        # We are on Windows
        for cmd in cmds:
            os.system(
                'start cmd.exe /k "{} && cd {} && {}"'.format(path[:2], path, cmd))

    elif plat == "Linux":
        # We are on Linux
        print("Run commands on Linux not yet supported")
    else:
        sys.exit("Unknown OS, please report. 0-1")

    if(selected == None):
        sys.exit("No project was selected. Exiting")

    if(option["quit"]):
        if plat == "macOS":
            os.system("exit")
        elif plat == "windows":
            os.system("exit")

    print("Project opened")
    printArt("Happy Hacking")



def add(payload: dict):
    """ Add a project to projects.json """
    projects = payload["projects"]
    new_project = payload["project"]
    projects.append(new_project)

    write_to_projects(projects)


def rm(payload: dict):
    """ Removed a project from projects.json """
    projects = payload["projects"]
    selected = payload["project"]

    res = removeProject(projects=projects, selected=selected)
    write_to_projects(res)


def edit(payload: dict):
    """ Edit a project in projects.json """

    projects = payload["projects"]
    selected = payload["project"]
    field = payload["field"]
    print("--")
    newProject = edit_project(selected, field)

    # Only remove after new details are recorded in case of user ending reconfig early.
    removeProject(projects=projects, selected=selected)
    projects.append(newProject)
    write_to_projects(projects)


def printArt(word: str):
    if(word == "Happy Hacking"):
        happyHacking = "\u001B[32m.  .             .  .      .         \n|__| _.._ ._   . |__| _. _.;_/*._  _ \n|  |(_][_)[_)\_| |  |(_](_.| \|[ )(_]\n       |  |  ._|                  ._|\n\u001B[0m"
        print(happyHacking)
    # print("Project {}, has started. Happy Hacking".format(title))
