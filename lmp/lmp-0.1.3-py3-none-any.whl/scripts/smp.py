#!/usr/bin/env python

from json.decoder import JSONDecodeError
import os
import json
# from src.driver import determinePlatform
import click
import subprocess
import pathlib
import driver


# OPEN PROJECT DATA FILE
absPath = os.path.dirname(os.path.abspath(__file__))


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
    


def selectProject(title: str):
    for project in projects:
        if project["title"].lower() == title.lower():
            return project
    return None


def findProject(project_title):
    project = None
    while True:
        project = selectProject(project_title)
        if(project != None):
            break
        project_title = input('"{}" is not a known project. Enter a new project title.'.format(project_title))
    return project

def create_project_struct(title: str, summary: str, os: str, path: str, editor_cmd: str, cmds: list):
    print("Creating Project")


def truthyQuestion(message: str):
    while True:
        res = input("{} (y/n)".format(message))
        if(res.lower() in "yes"):
            return True
        elif(res.lower() in "no"):
            return False
        else:
            print("{} is not understood.".format(res))

def printCMDDetails(cmds: list):
    """Prints Commands """
    if(len(cmds) > 0):
        print("Runtime Commands:")
        for i in range(len(cmds)):
            print("{}. {}".format(i+1,cmds[i]))

def printDetails(project: dict):
    """Prints details about a project"""
    print("Title:\n\t{}".format(project["title"]))
    print("Summary:\n\t{}".format(project["summary"]))

    plat = driver.determinePlatform()
    print("Path:\n\t{}".format(project["os"][plat]["path"]))
    print("IDE Keyword:\n\t{}".format(project["os"][plat]["editor-cmd"]))
    printCMDDetails(project["os"][plat]["scripts"]["cmds"])

@click.group()
def smp():
    """A CLI wrapper for StartMyProject"""
    pass


@click.option('-l', '--lim', default=None, help='Limit the number of projects that are listed')
@click.option('-A', '--show-All', is_flag=True, help='Show all projects that are listed')
@smp.command()
def li(lim: str, show_all: str):
    """List projects, Prints all project if a limit is not defined."""

    if(len(projects) == 0):
        print("There are no created projects. Created projects are listed here.")

    p = 1
    SHOW_LIMIT = 10
    for i in range(len(projects)):
        if(lim != None and i == int(lim)):
            break
        p = i
        if(p % SHOW_LIMIT == 0 and p != 0 and not show_all):
            cont = truthyQuestion(
                "Continue listing? {} more projects to display.".format(len(projects) - i))
            if(not cont):
                break
        print(projects[i]["title"])


@ click.argument('project_title')
@smp.command()
def info(project_title: str):
    """Display details about a project"""

    project = findProject(project_title)
    printDetails(project)



@click.option('-Q', '--quit-Console', is_flag=True, default=False, help='Process terminates shell after execution.')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Provide more verbose detail about started project.')
@ click.argument('project_title')
@ smp.command()
def start(project_title: str, quit_console: bool, verbose: bool):
    """Start project [PROJECT_TITLE]"""
    

    project = findProject(project_title)

    print("Starting {}".format(project["title"]))

    if(verbose):
        print(project["summary"])

    args = {
        "action": "START",
        "payload": {
            "project": project,
            "options": [
                {
                    "key": "quit",
                    "val": quit_console
                }
            ]
        }
    }

    driver.start(driver.parseArg(args))


@ smp.group()
def config():
    """ A Wrapper for adding, removing, and configuring projects """
    pass


@ config.command()
def add():
    """ Goes through the process of adding a project to the project list """

    print("Creating a new project.")

    # Create new project
    title = input("Project title? ")
    summary = input("Project summary? ")
    os = driver.determinePlatform()
    path = input("Absolute path to project: ")

    if(not driver.is_pathname_valid(path)):
        if(not truthyQuestion("Provided path is invalid, continue anyway? (y/n)")):
            driver.__exit("Process terminated.")

    editor_cmd = input(
        'Command to open editor (use "code ." to open vscode): ')

    makeCMDS = truthyQuestion(
        "Would you like to add any run time commands? (Remember these commands are run from the console relative to the provided path)")
    cmds = []
    if(makeCMDS):
        while True:
            cmd = input('Enter command. (Enter "end" to end)')
            if(cmd.lower() == "end"):
                break
            cmds.append(cmd)

    project_to_add = {
        "title": title,
        "summary": summary,
        "os": {
            "{}".format(os): {
                "path": path,
                "editor-cmd": editor_cmd,
                "scripts": {
                    "cmds": cmds,
                    "bash-scripts": []
                }
            }

        }
    }

    args = {
        "action": "REMOVE",
        "payload": {
            "projects": projects,
            "project": project_to_add
        }
    }
    driver.add(driver.parseArg(args))


@ click.argument('project_title')
@ config.command()
def rm(project_title: str):
    """ Goes through the process of removing a project from the project list """

    project_to_remove = findProject(project_title)

    
    
    args = {
        "action": "REMOVE",
        "payload": {
            "projects": projects,
            "project": project_to_remove
        }
    }

    driver.rm(driver.parseArg(args))

@ click.argument('project_title')
@ config.command()
def edit(project_title: str):
    """ Goes through the process of editing a project in the project list """

    
    project_to_edit = findProject(project_title)

    printDetails(project_to_edit)

    FIELDS = ["title", "summary", "path", "editor-cmd", "cmds"]

    field = input("Choose field to edit: ").lower()

    

    while (not (field in set(FIELDS))):
        field = input('Invalid field "{}": '.format(field)).lower()

    args = {
        "action": "EDIT",
        "payload": {
            "projects": projects,
            "project": project_to_edit,
            "field": field,
        }
    }
    driver.edit(driver.parseArg(args))


if __name__ == '__main__':
    smp(prog_name="smp")
