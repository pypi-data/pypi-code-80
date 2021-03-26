from setuptools import setup, find_packages
filepath = 'README.md'
setup(
        name="tziot",
        version="1.4",
        description="tziot sdk",
        long_description=open(filepath, encoding='utf-8').read(),
        long_description_content_type="text/markdown",
        author="jdh99",
        author_email="jdh821@163.com",
        url="https://github.com/jdhxyy/tziot-python",
        packages=find_packages(),
        data_files=[filepath]
    )
