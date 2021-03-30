import setuptools
with open("README.md", "r",encoding="utf-8") as fh:
	long_description=fh.read()


setuptools.setup(
	name="tidy_project",
	version="0.1",
	author="colinsarah",
	author_email="",
	desciption = "test delploy python to pypi",
	long_description=long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/colinsarah/tidy_project",
	packages=setuptools.find_packages(),
	install_requires=["flask>=1.1.0"],
	entry_points={
		"console_scripts":[
			"tidy_project=tidy_project:main"
		],
	},
	classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),


)