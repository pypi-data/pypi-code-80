"""
		Copyright (c) 2020 Discli
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from setuptools import setup
import os

def get_long_description():
        
        with open("README.md", encoding="utf-8") as f:
                readme = f.read()

        return readme

setup(
  name="discli", # I changed the name
  author="Zenqi",
  description="🎲 Discord Bot CLI for creating / deploying your discord bots!",
  long_description=get_long_description(),
  long_description_content_type='text/markdown',
  url="https://github.com/zenqii/discli",
  version=__import__("discli").__version__,
  python_requires=">=3.5",
  packages=["discli", "discli._ext"],
  platforms=["Windows"],
  license="MIT",
  keywords=["command line", "discord.py", "cli"],
  download_url="https://github.com/zenqii/discli/tarball/main",
  zip_safe=False,
  include_package_data=True,
  install_requires = [
	"rich",
	"requests",
	"discord"
  ],
  entry_points = {
	"console_scripts":[
		"discordcli = discli.__main__:discli",
		"discli = discli.__main__:discli"
	]
  },
  classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Operating System :: Microsoft :: Windows",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Topic :: Software Development",
		"Topic :: Software Development :: Libraries :: Python Modules",
	]
)
