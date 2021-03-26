from json.decoder import JSONDecodeError
import json
import driver
import os

absPath = os.path.dirname(os.path.abspath(__file__))


def open_projects():
  try:
    with open("{}/projects.json".format(absPath), "x") as f:
        json.dump([], f)
  except FileExistsError:
    with open("{}/projects.json".format(absPath), "r+") as f:
        try:
            projects = json.load(f)
        except JSONDecodeError:
            json.dump([], f)
            projects = []
            pass
        f.close()
    pass
    return projects

def select_project(title: str, project_list: list):
    for project in project_list:
        if project["title"].lower() == title.lower():
            return project
    return None


def find_project(project_title: str):
    project = None
    while True:
        project = select_project(project_title)
        if(project != None):
            break
        project_title = input('"{}" is not a known project. Enter a new project title.'.format(project_title))
    return project

def create_project_struct(title: str, summary: str, os: str, path: str, editor_cmd: str, cmds: list):
    print("Creating Project")




def print_cmd_details(cmds: list):
    """Prints Commands """
    if(len(cmds) > 0):
        print("Runtime Commands:")
        for i in range(len(cmds)):
            print("{}. {}".format(i+1,cmds[i]))

def print_details(project: dict):
    """Prints details about a project"""
    print("Title:\n\t{}".format(project["title"]))
    print("Summary:\n\t{}".format(project["summary"]))

    plat = driver.determinePlatform()
    print("Path:\n\t{}".format(project["os"][plat]["path"]))
    print("IDE Keyword:\n\t{}".format(project["os"][plat]["editor-cmd"]))
    print_cmd_details(project["os"][plat]["scripts"]["cmds"])