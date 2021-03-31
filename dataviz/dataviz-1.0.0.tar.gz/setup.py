from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dataviz",
    version="1.0.0",
    author_email="info@librecube.org",
    description="Create plots quickly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/librecube/lib/python-dataviz",
    license="MIT",
    python_requires='>=3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
        'pandas',
        'matplotlib',
        'bokeh'],
)
