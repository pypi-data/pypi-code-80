#                    Copyright (c) 2021 discli.
#                
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from rich.console import Console
from rich.progress import track
import requests
from rich.prompt import Prompt, Confirm
import os
import subprocess
import json
import time
import getpass
import shutil
import sys

class Heroku:
    def __init__(self, path):
        self.path = path
        self.email = Prompt.ask("Enter your email for git (require in order to commit via git)")
        self.username = Prompt.ask("Enter your username", default=getpass.getuser())

        while self.email == "":
            Prompt.ask("Enter your email for git")

        try:

            with open(self.path + "\\config.json", "r") as f:
                data = json.load(f)

        except FileNotFoundError:
            print("config.json is missing..")
            sys.exit()
        
        
        self.name = str(data["name"]).replace(" ", "").lower()
        self.console = Console()
        self.is_heroku_in_path()
        self.login()
        self.main()

    def is_heroku_in_path(self):
        self.heroku_path = shutil.which("heroku") 
        
        if self.heroku_path: return
        else: 
            self.console.log("[red]» [magenta]heroku.bat[/magenta] is missing. Install heroku @ https://devcenter.heroku.com/articles/heroku-cli.") 
            sys.exit()

    def login(self):
        self.console.log("[red]»[/red] executing [magenta]heroku login[/magenta].")
        self.procress("heroku login")


    def main(self):
        self._git = shutil.which("git")

        if self._git: pass
        else: self.console.print("[red]» [magenta]git[/magenta] is missing. Install git @ https://git-scm.com/downloads")

        # init 
        self.console.log("\n[red]»[/red] executing [magenta]git init[/magenta].") 
        self.procress("git init")

        self.console.log(f'\n[red]»[/red] executing [magenta]git config --global user.name "{self.username}"[/magenta].')
        self.procress(f"git config --global user.name '{self.username}'")

        self.console.log(f'\n[red]»[/red] executing [magenta]git config user.email "{self.email}"[/magenta].')
        self.procress(f'git config user.email "{self.email}"')

        self.console.log(f"\n[red]»[/red] executing [magenta]heroku create {self.name}[/magenta].")
        self.procress(f"heroku create {self.name}")

        self.console.log(f"\n[red]»[/red] executing [magenta]heroku git:remote -a {self.name}[/magenta].")
        self.procress(f"heroku git:remote -a {self.name}")

        self.console.log("\n[red]»[/red] executing [magenta]git add .[/magenta].")
        self.procress("git add .")

        self.console.log('\n[red]»[/red] executing [magenta]git commit -am "upload"[/magenta].')
        self.procress('git commit') 

        self.console.log("\n[red]»[/red] executing [magenta]git push heroku master[/magenta].")
        self.procress("git push heroku master")       

    def push_to_heroku(self):
        pass
    
    def procress(self, command):
        p = subprocess.run(command, shell=True)
        if p.returncode != 0:
            self.console.print(f"[red]»[/red] error executing [magenta]{command}[/magenta].")

        return p



class Variables:
    BANNER = """[cyan]
█████  ███                   ████   ███ 
░░███  ░░░                   ░░███  ░░░  
███████  ████   █████   ██████  ░███  ████ 
███░░███ ░░███  ███░░   ███░░███ ░███ ░░███ 
░███ ░███  ░███ ░░█████ ░███ ░░░  ░███  ░███ 
░███ ░███  ░███  ░░░░███░███  ███ ░███  ░███ 
░░████████ █████ ██████ ░░██████  █████ █████
░░░░░░░░ ░░░░░ ░░░░░░   ░░░░░░  ░░░░░ ░░░░░ """

    
    r = requests.get("https://raw.githubusercontent.com/zenqii/discli/main/version.json").json()
    VERSION = r["version"]
    UPDATE = r["update"]
    RELEASENOTE = r["release_note"]

class DiscordCLI:
    def __init__(self, folder_name = None):
        os.system("cls")
        self.console = Console()
        self.folder_name = folder_name

        

        if self.folder_name != None:
            os.system("mkdir {}".format(folder_name))
            os.chdir(os.getcwd() + f"\\{folder_name}")
            

        # check for update

        if Variables.UPDATE:
            self.console.print(f"New version is released please install via [red]pip install --upgrade discli [/red], {Variables.VERSION}: {Variables.RELEASENOTE}")
            sys.exit()
    
        
        self.console.print(Variables.BANNER)
        self.console.print(f"\nDiscord Bot CLI v{Variables.VERSION} for creating projects")
        self.console.print("Copyright (c) 2020, [link=https://github.com/zenqii][magenta]Zenqi[/magenta][/link]. All rights reserved.")

        user_name = getpass.getuser() +"bot"
        config = {}
        bot_token = ""


        bot_name = Prompt.ask("\n[green]»[yellow] Enter your desire bot name", default=user_name)        

        while bot_token == "":
            bot_token = Prompt.ask("[green]»[yellow] Enter your bot token [red](required)")

        prefix = Prompt.ask("[green]»[yellow] Enter bot prefix", default="!")
        is_heroku = Confirm.ask("\n[green]»[magenta] Would you like to add heroku support?")

        

        config["name"] = bot_name
        config["token"] = bot_token
        config["prefix"] = prefix
        config["heroku"] = is_heroku
        
        for _ in track(range(50), description="[green]»[cyan] Initializing discli.."):
            time.sleep(.1)

        work = True
        with self.console.status("[green]»[bold magenta] Creating ext folder...",) as status:
            while work:

                self.console.log("[green]»[cyan] Config file created: [blue]{}".format(config))
                self.create_config(os.getcwd(), config, is_heroku)
                self.create_main_file(os.getcwd())
                self.copy_extension(os.getcwd())
                work = False
                time.sleep(1)
                break

    def create_config(self, path, config, is_heroku):   
        with open(path + "\\config.json", 'w') as f:
            json.dump(config, f, indent=5)
            f.close()

        if is_heroku:

            with open(path + "\\requirements.txt", "w") as fw:
                fw.write("# Requirements file used for heroku. Please enter every needed module here\ndiscord\n#discord['voice'] <- Use this if you want voice support")
                fw.close()

            with open("Procfile", "w") as f:
                f.write("worker: python main.py")


    def copy_extension(self, path):
        abs_path = os.path.dirname(os.path.realpath(__file__))
        try:
            os.mkdir(path + "\\ext")
        except FileExistsError:
            self.console.log("[magenta]» ext folder already exist, skipping the creation of new one")
        
        copying = True

        try:
            self.console.log(f"[cyan]» Copying {abs_path}\\ext\\moderation.py to {path}\\ext")
            shutil.copy(f"{abs_path}\\_ext\\moderation.py", f"{path}\\ext")
        
        except FileNotFoundError:
            self.console.log("[red]» _ext folder is missing, skipping this")

    def create_main_file(self, path):
        
        _ = """\n\n#                    Copyright (c) 2021 <your_name>.\n#                 This project was created by Discord CLI\n# \n# Permission is hereby granted, free of charge, to any person obtaining a copy\n# of this software and associated documentation files (the "Software"), to deal\n# in the Software without restriction, including without limitation the rights\n# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n# copies of the Software, and to permit persons to whom the Software is\n# furnished to do so, subject to the following conditions:\n# The above copyright notice and this permission notice shall be included in all\n# copies or substantial portions of the Software.\n# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n# SOFTWARE.\n\n\nfrom discord.ext import commands\nimport discord\nimport json\nimport os\n\ntry:\n\n    with open("config.json", "r") as f:\n        data = json.load(f)\n\nexcept FileNotFoundError:\n    print("config.json is missing")\n\nbot = commands.Bot(command_prefix="{}".format(data["prefix"]))\n\n\ndef get_cogs(bot):\n    try:\n        print("cogs found")\n        for filename in os.listdir("./ext"):\n            if filename.endswith(".py"):\n                bot.load_extension(f"ext.%s"%(filename[:-3]))\n            else:\n                print("unable to load %s"%(filename[:-3]))\n    except FileNotFoundError:\n        print("cogs not found")\n\n@bot.event\nasync def on_ready():\n\n    print("Discord Bot template by discli")\n    print("-"*50)\n    print("Logged in as: %s" %(bot.user.name)) \n\n    serverlist = []\n    for server in bot.guilds:\n        serverlist.append(server.name)\n\n    # set the presence of the bot\n\n    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="%s servers"%(len(serverlist))))\n\nprint("-"*50)\nprint("Loading Cogs")\nget_cogs(bot)\nbot.run("{}".format(data["token"]))\n"""
        with open(path + "\\main.py", "w") as f:
            f.write(_)

        self.console.log("[green]»[cyan] main file file created")


def help_command():

    os.system("cls")
    console = Console()
    console.print(Variables.BANNER)
    console.print("""\n[red]Welcome to Discli Help Center (Discord Bot CLI) v{} [/]
[magenta]help[/] | [yellow]Show help text[/]
[magenta]create[/] | [yellow]Create project in current directory[/]
[magenta]create[/] <dir> | [yellow]Create project in specific directory (optional)[/]
[magenta]run[/] | [yellow]Run the bot[/]
[magenta]heroku[/] | [yellow]Create heroku app for free hosting.[/] 
Example:
[green]»[cyan] discli [magenta]create """.format(Variables.VERSION))

def run(path):
    import subprocess

    main_file = path + "\\main.py"
    interpreter = sys.executable

    console = Console()
    console.print("[green]»[cyan] Running [magenta]main.py[/]")
    
    p = subprocess.run(f"{interpreter} {main_file}")
    
    if p.returncode != 0:
        console.print("[red]» [magenta]main.py[/magenta] is missing")
        sys.exit()

    console.print("[green]»[cyan][magenta] main.py[/magenta] is now running")

 
def discli():
    console = Console()
    if __import__("discli").__version__ != Variables.VERSION:
            console.print(f"New version is released please install via [red]pip install --upgrade discli [/red], {Variables.VERSION}: {Variables.RELEASENOTE}")
            sys.exit()
    
    try:
        if sys.argv[1] == "create":
            try:
                DiscordCLI(sys.argv[2])
            except IndexError:
                DiscordCLI()

        elif sys.argv[1] == "run":
            run(os.getcwd())

        elif sys.argv[1] == "heroku":
            heroku = Heroku(os.getcwd())
            #print("Comming soon! I'll inform you whenever the update comes in.")

    except IndexError:
        help_command()
        
if __name__ == "__main__":
    discli()
