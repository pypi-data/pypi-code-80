from setuptools import setup

with open("README.md", "r") as f:
	long_description = f.read()

setup(

	name = "hello-world-nagarjun",
	version = "0.2.1",
	py_modules =["hello_world"],
	package_dir = {'': 'src'},
	python_requires = ">=3.6.0",
	install_requires = ["numpy"],
	author = "Nagarjun",
	description='A sample Python project',
	long_description=long_description,
	long_description_content_type='text/markdown',
	license='MIT',
	)