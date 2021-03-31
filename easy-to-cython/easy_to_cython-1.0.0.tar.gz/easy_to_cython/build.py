import json
import os
import shutil
from distutils.command.build_ext import build_ext
from multiprocessing import cpu_count
from pathlib import Path

from Cython.Build import cythonize
from setuptools import find_packages, Extension, setup

if os.path.exists('./build'):
    shutil.rmtree('./build')

config_entity = None
if os.path.exists('./easy_to_cython.json'):
    with open('./easy_to_cython.json', 'r', encoding='utf-8') as file:
        config_entity = json.load(file)

local_packages = find_packages()

if config_entity is not None:
    for modules in config_entity['remove_models']:
        if modules in local_packages:
            local_packages.remove(modules)

extentions = []
for obj in local_packages:
    dir_path = os.path.join('.', obj.replace(".", "/"))
    for name in os.listdir(dir_path):
        if "__" in name or os.path.isdir(dir_path + "/" + name):
            continue
        if config_entity is not None and name in config_entity['remove_files']:
            continue
        extentions.append(Extension(obj + '.' + name.replace('.py', ''), ["%s/%s" % (obj.replace(".", "/"), name)]))


class KitBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir

        """
        把__init__.py拷贝到cython的编译目录，cython会编译不过这种脚本
        """
        for obj in local_packages:
            dir_path = obj.replace(".", "/")
            self.copy_file(Path(dir_path) / "__init__.py",
                           os.getcwd(), target_dir)

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


def build():
    setup(
        name='easy_to_cython',
        version='1.0.0',
        packages=local_packages,
        platforms="any",
        ext_modules=cythonize(
            extentions,
            build_dir="build",
            annotate=True,
            compiler_directives=dict(always_allow_keywords=True),
            language_level=3,
            nthreads=cpu_count()
        ),
        cmdclass=dict(build_ext=KitBuildExt),
    )
