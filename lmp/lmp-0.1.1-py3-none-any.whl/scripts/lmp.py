#!/usr/bin/env python


import os
import json
# from src.driver import determinePlatform
import click
import subprocess

import driver
import projects
import utils

# OPEN PROJECT DATA FILE



projects_list: list = projects.openProjects()




@click.group()
def lmp():
    """A CLI wrapper for StartMyProject"""
    pass


@click.option('-l', '--lim', default=None, help='Limit the number of projects that are listed')
@click.option('-A', '--show-All', is_flag=True, help='Show all projects that are listed')
@lmp.command()
def li(lim: str, show_all: str):
    """List projects, Prints all project if a limit is not defined."""

    if(len(projects_list) == 0):
        print("There are no created projects. Created projects are listed here.")

    p = 1
    SHOW_LIMIT = 10
    for i in range(len(projects_list)):
        if(lim != None and i == int(lim)):
            break
        p = i
        if(p % SHOW_LIMIT == 0 and p != 0 and not show_all):
            cont = utils.truthy_question(
                "Continue listing? {} more projects to display.".format(len(projects_list) - i))
            if(not cont):
                break
        print(projects_list[i]["title"])


@ click.argument('project_title')
@lmp.command()
def info(project_title: str):
    """Display details about a project"""

    project = projects.find_project(project_title)
    projects.print_details(project)



@click.option('-Q', '--quit-Console', is_flag=True, default=False, help='Process terminates shell after execution.')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Provide more verbose detail about started project.')
@click.option('-l', '--limited', is_flag=True, default=False, help='Launch only code editor.')
@ click.argument('project_title')
@ lmp.command()
def start(project_title: str, quit_console: bool, verbose: bool, limited: bool):
    """Start project [PROJECT_TITLE]"""
    

    project = projects.find_project(project_title)

    print("Starting {}".format(project["title"]))

    if(verbose):
        print(project["summary"])

    args = {
        "action": "START",
        "payload": {
            "project": project,
            "options": 
                {
                    "quit": quit_console,
                    "limited": limited,
                }
        }
    }

    driver.start(driver.parseArg(args))


@ lmp.group()
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
        if(not utils.truthy_question("Provided path is invalid, continue anyway? (y/n)")):
            driver.__exit("Process terminated.")

    editor_cmd: str = input(
        'Command to open editor (use "code ." to open vscode): ')

    CMDS: bool = utils.truthy_question(
        "Would you like to add any run time commands? (Remember these commands are run from the console relative to the provided path)")
    cmds: list = []
    if(CMDS):
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

    project_to_remove = projects.find_project(project_title)

    
    
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

    
    project_to_edit = projects.find_project(project_title)

    projects.print_details(project_to_edit)

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
    lmp(prog_name="lmp")
