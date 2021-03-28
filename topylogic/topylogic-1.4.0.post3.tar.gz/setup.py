import setuptools
from glob import glob

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

sources = glob('src/*.c')
#'src/src/' + f for f in ['AVL.c', 'stack.c', 'edge.c', 'fireable.c', 'graph.c', 'request.c', 'topologic.c', 'topologic_json.c', 'vertex.c', 'windows_wrap.c', 'topylogic_wrap.c']]

module = setuptools.Extension('_topylogic',
		    sources  = sources,
		    include_dirs = ['./src/include/'],
		   )



setuptools.setup(
        name="topylogic",
        version="1.4.0r3",
        author="Matthew Stern",
        author_email="msstern98@gmail.com",
        description="Context Free/Switching DFA/NFA library",
        url="https://github.com/mstern98/topylogic-git",
        keywords = ['NFA', 'DFA', 'Context-Switching', 'Threading', 'Graph'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        package_dir={"": "src", "include": "include"},
        ext_modules = [module],
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.9",
)
