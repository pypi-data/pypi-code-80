     
##############################################
from setuptools.command.install import install
class PostCMD(install):
      # """cmdclass={'install': XXCMD,'install': EEECMD }"""
      def   run(self):
            # ## 引用專屬 boos 目錄
            # # from boos import sitePY
            # # sitePY(siteD.lib)       ## 宣告內涵

            # import os
            # ## getcwd() --> /tmp/pip-install-hbr_rpcp/cmd.py 這個位置
            # # os.system(f"echo {os.getcwd()}> /usr/local/lib/python3.7/dist-packages/cmds/CC.py")

            # ## 提示
            # BL= os.path.isdir("/usr/local/lib/python3.7/dist-packages/cmds")
            # # os.system(f"echo {BL}")
            # # os.chdir("/usr/local/lib/python3.7/dist-packages/cmds") ##失敗
            
            # os.chdir("/usr/local/lib/python3.7/dist-packages")    ## 成功
            # # if  self.Linux:
            # #     os.system("echo SSS.VMx")
                
            # # p = subprocess.Popen(r'start cmd /k "'+P.SSQ+'"', shell=True)
            # # ping 127.0.0.1 -n 5 -w 1000 >nul && rmdir /S /Q   C:\Users\moon\AppData\Local\pip\cache\wheels
            install.run(self)


with open("/content/QQ/README.md", "r") as fh:
          long_description = fh.read()


#### setup.py ################################
from setuptools import setup, find_packages
setup(
      # name  =  "cmd.py"  ,
      ## version
      # version= "9.4",
      # version="1.307",
      name  =  "cmdOS"  ,
      version= "1.0.0",
      description="My CMD 模組",
      long_description=long_description,
      long_description_content_type="text/markdown",
      # author="moon-start",
      # author_email="login0516mp4@gmail.com",
      # url="https://gitlab.com/moon-start/cmd.py",
      license="LGPL",
      ####################### 宣告目錄 #### 使用 __init__.py
      ## 1 ################################################ 
      packages=find_packages(include=['cmds','cmds.*']),
      ## 2 ###############################################
      # packages=['git','git.cmd',"git.mingw64"],
      # packages=['cmds'],
      # packages = ['moonXP'],
      # package_data = {'': ["moon"] },
      #################################
      cmdclass={
            'install': PostCMD
      }
      #################################      
)