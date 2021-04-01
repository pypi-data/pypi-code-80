description = """
testcanarybot project package manager;
Copyright 2021 kensoi
"""

import argparse
import importlib
import traceback
import os
import sys
import time

from .packaet import *

packaet_parser = argparse.ArgumentParser(description = description)

packaet_parser.add_argument("--path", type = str, default = os.getcwd(), help='[OPTIONAL] workspace path')

packaet_parser.add_argument("--run", type = str, default = [], nargs='+', help='run a list/run all/get info of projects')
packaet_parser.add_argument("--create", type = str, default = "", help='Create project')
packaet_parser.add_argument("--project",type = str, default = "", help='setting project')

packaet_parser.add_argument("--assets", type = str, default = "assets", help='[OPTIONAL] assets directory')
packaet_parser.add_argument("--library", type = str, default = "library", help='[OPTIONAL] library directory')

packaet_parser.add_argument("--token", type = str, default = "REQUIRED_TO_FILL!", help='[CREATE] community access token')
packaet_parser.add_argument("--service", type = str, default = "", help='[CREATE] community access token [optional]')
packaet_parser.add_argument("--group", type = str, default = "REQUIRED_TO_FILL!", help='[CREATE] community identificator')

packaet_parser.add_argument("--cm", type = str, default = "", help='[PROJECT] create module testcanarybot')
packaet_parser.add_argument("-f", dest = "folder", action = 'store_true', help='[PROJECT] create module in a folder')

args = packaet_parser.parse_args()

packaet_project_directory =  args.create + args.project
packaet_project_assets = args.assets
packaet_project_library = args.library
workingProjects = []

if packaet_project_directory == '' and args.run == []:
    system_message('Try to run command \"python testcanarybot -h\"')
    quit()

elif packaet_project_directory not in [args.create, args.project] and args.run == []:
    raise RuntimeError('2 or more args! \nTry to run command \"python testcanarybot -h\"')

if len(args.run) > 0:
    sys.path.append(args.path + '\\')

    if args.run in [['info'], ['all']]:
        if args.run[0] == 'info':
            system_message('Projects at this directory:\n\t- ' + '\n\t- '.join(getProjects(args.path)))

        elif args.run[0] == 'all':
            for i in getProjects(args.path):
                testApp = importlib.import_module(i + '.root')
                testBot = threadBot(testApp, i, packaet_project_assets, packaet_project_library)
                workingProjects.append(testBot)
                time.sleep(1)

    else:
        for i in args.run:
            if i in getProjects(args.path):
                testApp = importlib.import_module(i + '.root')
                testBot = threadBot(testApp, i, packaet_project_assets, packaet_project_library)
                workingProjects.append(testBot)
                time.sleep(1)
            else:
                raise ValueError(f"Directory does not exist or is not a bot project. Run \"python testcanarybot --create {i}\" to create project, and try again")

    while True:
        for bot in range(len(workingProjects)):
            if not workingProjects[bot].is_alive():
                workingProjects.pop(bot)

        if len(workingProjects) == 0:
            quit()
        time.sleep(3)



elif args.create != '':
    system_message('Creating project <<', packaet_project_directory, '>>')
    
    if packaet_project_directory not in projects:
        system_message("Creating directories")

        os.mkdir(args.path + '\\' + packaet_project_directory)
        os.mkdir(args.path + '\\' + packaet_project_directory + '\\' + packaet_project_assets)
        os.mkdir(args.path + '\\' + packaet_project_directory + '\\' + packaet_project_library)

        system_message("Creating << root >>")

        with open(args.path + '\\' + packaet_project_directory + '\\' + 'root.py', 'w+') as root:
            root.write(packaet_root_raw.format(token = args.token, group = args.group, service_token = args.service))

        system_message("Creating << readme >>")

        with open(args.path + '\\' + packaet_project_directory + '\\' + packaet_project_library + '\\readme.txt', 'w+') as readme:
            readme.write(packaet_readme_library.format(packaet_project_directory = packaet_project_directory))
        
        with open(args.path + '\\' + packaet_project_directory + '\\' + packaet_project_assets + '\\readme.txt', 'w+') as readme:
            readme.write(packaet_readme_assets)
        system_message(f"Done! \n\tDirectory: ./{packaet_project_directory}/ \n\tUsage: python testcanarybot --run {packaet_project_directory}")
    
    else:
        raise RuntimeError("Folder exists! Try another name")

elif args.project != '':
    system_message("manager for <<", packaet_project_directory, ">>")

    if args.cm != '':
        packaet_module_name = parsename(args.cm) # if args.cm != '' else 'handler_' + gen_str(15)
        packaet_module_inFolder = args.folder

        if packaet_module_inFolder:
            if packaet_module_name not in os.listdir(args.path + '\\' + packaet_project_directory + '\\library\\'):
                os.mkdir(args.path + '\\' + packaet_project_directory + '\\library\\' + packaet_module_name)
            
            system_message("created folder <<", packaet_module_name, ">>")
            
            with open(args.path + '\\' + packaet_project_directory + '\\library\\' + packaet_module_name + "\\main.py", 'w+') as module:
                module.write(libraryModuleRaw)
            
            system_message("Done! Results at ./" + packaet_project_directory + "/library/")

        else:
            system_message("created file <<", packaet_module_name, ">>")
            
            with open(args.path + '\\' + packaet_project_directory + '\\library\\' + packaet_module_name + ".py", 'w+') as module:
                module.write(libraryModuleRaw)
            
            system_message("Done! Results at ./" + packaet_project_directory + "/library/")