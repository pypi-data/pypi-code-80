# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jurigged']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.17.12,<2.0.0', 'ovld>=0.2.7,<0.3.0', 'watchdog>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['jurigged = jurigged.live:cli']}

setup_kwargs = {
    'name': 'jurigged',
    'version': '0.2.2',
    'description': 'Live update of Python functions',
    'long_description': '\n# jurigged\n\nJurigged lets you update your code while it runs. Using it is trivial:\n\n1. `python -m jurigged your_script.py`\n2. Change some function or method with your favorite editor and save the file\n3. Jurigged will hot patch the new function into the running script\n\nJurigged updates live code smartly: changing a function or method will fudge code pointers so that all existing instances are simultaneously modified to implement the new behavior. When modifying a module, only changed lines will be re-run.\n\n\n## Install\n\n```bash\npip install jurigged\n```\n\n\n## Command line\n\nThe simplest way to use jurigged is to add `-m jurigged` to your script invocation, or to use `jurigged` instead of `python`. You can use `-v` to get feedback about what files are watched and what happens when you change a file.\n\n```bash\npython -m jurigged -v script.py\n\nOR\n\njurigged -v script.py\n```\n\nWith no arguments given, it will start a live REPL:\n\n```bash\npython -m jurigged\n```\n\nFull help:\n\n```\nusage: jurigged [-h] [--verbose] [--watch PATH] [-m MODULE] [PATH] ...\n\nRun a Python script so that it is live-editable.\n\npositional arguments:\n  PATH                  Path to the script to run\n  ...                   Script arguments\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --verbose, -v         Show watched files and changes as they happen\n  --watch PATH, -w PATH\n                        Wildcard path/directory for which files to watch\n  -m MODULE             Module or module:function to run\n```\n\n\n## Troubleshooting\n\nFirst, if there\'s a problem, use the verbose flag (`jurigged -v`) to get more information. It will output a `Watch <file>` statement for every file that it watches and `Update/Add/Delete <function>` statements when you update, add or delete a function in the original file and then save it.\n\n**The file is not being watched.**\n\nBy default, scripts are watched in the current working directory. Try `jurigged -w <file>` to watch a specific file, or `jurigged -w /` to watch all files.\n\n**The file is watched, but nothing happens when I change the function.**\n\nIt\'s possibly because you are using an editor that saves into a temporary swap file and moves it into place (vi does this). The `watchdog` library that Jurigged uses loses track of the file when that happens. Pending a better solution, you can try to configure your editor so that it writes to the file directly. For example, in vi, `:set nowritebackup` seems to do the trick (either put it in your .vimrc or execute it *before* you save for the first time).\n\n**Jurigged said it updated the function but it\'s still running the old code.**\n\nIf you are editing the body of a for loop inside a function that\'s currently running, the changes will only be in effect the next time that function is called. A workaround is to extract the body of the for loop into its own helper function, which you can then edit. Alternatively, you can use [reloading](https://github.com/julvo/reloading) alongside Jurigged.\n\nSimilarly, updating a generator or async function will not change the behavior of generators or async functions that are already running.\n\n**I can update some functions but not others.**\n\nThere may be issues updating some functions when they are decorated or stashed in some data structure that Jurigged does not understand. Jurigged does have to find them to update them, unfortunately.\n\n\n## API\n\nYou can call `jurigged.watch()` to programmatically start watching for changes. This should also work within IPython or Jupyter as an alternative to the `%autoreload` magic.\n\n```python\nimport jurigged\njurigged.watch()\n```\n\nBy default all files in the current directory will be watched, but you can use `jurigged.watch("script.py")` to only watch a single file, or `jurigged.watch("/")` to watch all modules.\n\n\n### Recoders\n\nFunctions can be programmatically changed using a Recoder. Make one with `jurigged.make_recoder`. This can be used to implement hot patching or mocking. The changes can also be written back to the filesystem.\n\n```python\nfrom jurigged import make_recoder\n\ndef f(x):\n    return x * x\n\nassert f(2) == 4\n\n# Change the behavior of the function, but not in the original file\nrecoder = make_recoder(f)\nrecoder.patch("def f(x): return x * x * x")\nassert f(2) == 8\n\n# Revert changes\nrecoder.revert()\nassert f(2) == 4\n\n# OR: write the patch to the original file itself\nrecoder.commit()\n```\n\n`revert` will only revert up to the last `commit`, or to the original contents if there was no commit.\n\nA recoder also allows you to add imports, helper functions and the like to a patch, but you have to use `recoder.patch_module(...)` in that case.\n\n\n## Caveats\n\nJurigged works in a surprisingly large number of situations, but there are several cases where it won\'t work, or where problems may arise:\n\n* **Functions that are already running will keep running with the existing code.** Only the next invocations will use the new code.\n  * When debugging with a breakpoint, functions currently on the stack can\'t be changed.\n  * A running generator or async function won\'t change.\n  * You can use [reloading](https://github.com/julvo/reloading) in addition to Jurigged if you want to be able to modify a running for loop.\n* **Changing initializers or attribute names may cause errors on existing instances.**\n  * Jurigged modifies all existing instances of a class, but it will not re-run `__init__` or rename attributes on existing instances, so you can easily end up with broken objects (new methods, but old data).\n* **Updating the code of a decorator or a closure may or may not work.** Jurigged will do its best, but it is possible that some closures will be updated but not others.\n* **Decorators that look at/tweak function code will probably not update properly.**\n  * Wrappers that try to compile/JIT Python code won\'t know about jurigged and won\'t be able to redo their work for the new code.\n  * They can be made to work if they set the (jurigged-specific) `__conform__` attribute on the old function. `__conform__` takes a reference to the function that should replace it.\n\n\n## How it works\n\nIn a nutshell, jurigged works as follows:\n\n1. Insert an import hook that collects and watches source files.\n2. Parse a source file into a set of definitions.\n3. Crawl through a module to find function objects and match them to definitions.\n   * It will go through class members, follow functions\' `__wrapped__` and `__closure__` pointers, and so on.\n4. When a file is modified, re-parse it into a set of definitions and match them against the original, yielding a set of changes, additions and deletions.\n5. For a change, exec the new code (with the decorators stripped out, if they haven\'t changed), then take the resulting function\'s internal `__code__` pointer and shove it into the old one. If the change fails, it will be reinterpreted as a deletion of the old code followed by the addition of the new code.\n6. New additions are run in the module namespace.\n\n\n## Comparison\n\nThe two most comparable implementations of Jurigged\'s feature set that I could find (but it can be a bit difficult to find everything comparable) are **%autoreload** in IPython and **[limeade](https://github.com/CFSworks/limeade)**. Here are the key differences:\n\n* They both re-execute the entire module when its code is changed. Jurigged, by contrast, surgically extracts changed functions from the parse tree and only replaces these. It only executes new or changed statements in a module.\n  \n  Which is better is somewhat situation-dependent: on one hand, re-executing the module will pick up more changes. On the other hand, it will reinitialize module variables and state, so certain things might break. Jurigged\'s approach is more conservative and will only pick up on modified functions, but it will not touch anything else, so I believe it is less likely to have unintended side effects. It also tells you what it is doing :)\n\n* They will re-execute decorators, whereas Jurigged will instead dig into them and update the functions it finds inside.\n  \n  Again, there\'s no objectively superior approach. `%autoreload` will properly re-execute changed decorators, but these decorators will return new objects, so if a module imports an already decorated function, it won\'t update to the new version. If you only modify the function\'s code and not the decorators, however, Jurigged will usually be able to change it inside the decorator, so all the old instances will use the new behavior.\n\n* They rely on synchronization points, whereas Jurigged can be run in its own thread.\n\n  This is a double-edged sword, because even though Jurigged can add live updates to existing scripts with zero lines of additional code, it is not thread safe at all (code could be executed in the middle of an update, which is possibly an inconsistent state).\n\nOther similar efforts:\n\n* [reloading](https://github.com/julvo/reloading) can wrap an iterator to make modifiable for loops. Jurigged cannot do that, but you can use both packages at the same time.\n',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/breuleux/jurigged',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
