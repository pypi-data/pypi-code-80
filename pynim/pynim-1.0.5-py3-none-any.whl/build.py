import os
import time
from shutil import copy2, copytree, rmtree
from subprocess import STDOUT, Popen, getoutput, getstatusoutput, run
def buildinstaller(pythonfile: str, appName: str = None, AdditionalFiles: list = [], AdditionalFolders: list = [], appIcon: str = "", smallersize: bool = True, windowed: bool = False, version: str="", AdditionalArgs: str="", launchBtn: bool= None):
    installer = open("installer.nsi","r").read()
    def deldir(dir: str):
        if os.path.exists(os.path.join(ThisPath, dir)):
            rmtree(dir)

    def Print(txt):
        if level == "info":
            t = " -->"
            [print(t, line) for line in txt.split("\n")]
        elif level == "error":
            t = "Error:"
            [print(t, line) for line in txt.split("\n")]
        elif level == "normal":
            t = None
            print(txt)

    makensis = getoutput("where makensis.exe").replace("\r", "").split("\n")[0]
    if not "makensis.exe" in makensis:
        level = "error"
        Print("makensis not found!")
        return False
    if appIcon:
        appIcon = os.path.realpath(appIcon)
    name = '.'.join(pythonfile.split(
        '.')[:-1]).replace("/", "\\").split("\\")[-1]
    if not appName:
        appName = name
    Setup = appName + ".exe"
    DoNotDeleteList = ["base_library.zip", "unicodedata.pyd"]
    level = "normal"
    start = time.time()
    ThisPath = os.path.abspath(os.getcwd())
    Print('building ' + name + " installer:")
    level = "info"
    optional = ""
    if appIcon:
        optional += f' -i "{appIcon}" '
    if windowed:
        optional += " --windowed "
    optional += AdditionalArgs
    Print("running pyinstaller...")
    script = os.path.realpath(pythonfile)
    cmd = f'pyinstaller --log-level ERROR --onedir --noconfirm -n "{name}" {optional} "{script}"'
    if os.system(cmd):
        level = "error"
        Print("build failed!")
        return False
    Print("adding additional files and folders to dist...")
    SetupPath = f"dist\\{name}\\"
    os.replace(SetupPath + name + ".exe", SetupPath + Setup)
    for File in AdditionalFiles:
        copy2(os.path.realpath(File), SetupPath + File.replace("/","\\").split("\\")[-1])
    for folder in AdditionalFolders:
        Folder = os.path.realpath(folder)
        copytree(folder, SetupPath + Folder.replace("/", "\\").split("\\")[-1])
    if smallersize:
        Print("running app...")
        appexe = os.path.realpath(SetupPath + Setup)
        if windowed:
            Popen(appexe)
        else:
            FNULL = open(os.devnull, 'w')
            Popen(appexe, stdout=FNULL, stderr=FNULL)
        Print("removing unnesseseri files...")
        time.sleep(5)
        for File in os.listdir(SetupPath):
            if not ((File in AdditionalFiles) or (File in DoNotDeleteList)):
                try:
                    os.remove(SetupPath + File)
                except:
                    pass
        Print("killing app...")
        if os.system(f'TASKKILL /F /IM "{Setup}"'):
            level = "error"
            Print("Cannot create smaller file size for this script.")
            return False
    if appIcon:
        optional = f'!define MUI_ICON "{appIcon}"'
    else:
        optional = ""
    if version:
        ver = f" V{version}"
    else:
        ver = ""
    if launchBtn == None:
        launchBtn = windowed
    launch=""
    if launchBtn:
        launch = f'  !define MUI_FINISHPAGE_RUN "$instdir\\{appName}.exe"\n  !define MUI_FINISHPAGE_RUN_TEXT "Launch Application"'
    ins = installer.format(Name=name, appName=appName, optional=optional, thisPath=ThisPath,ver=ver, launch=launch, 
                            If="{If}", RunningX64="{RunningX64}", Else="{Else}", EndIf="{EndIf}")
    open("ins.nsi", "w").write(ins)
    Print("building installer...")
    exitCode, log = getstatusoutput(
        f'"{makensis}" /V1 /X"SetCompressor /FINAL lzma" ins.nsi')
    if exitCode:
        level = "error"
        Print(log)
        return False
    level = "normal"
    Print(f'deleteing build files...')
    level = "info"
    deldir('dist')
    deldir('build')
    os.remove("ins.nsi")
    os.remove(name + '.spec')
    end = time.time()
    print('done! time: ' + str(end - start))
    os.system('pause')
    return True
