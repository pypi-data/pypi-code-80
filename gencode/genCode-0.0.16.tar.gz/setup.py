from setuptools import setup

with open("./README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='genCode',
    version='0.0.16',
    description='生成代码',
    author='hammer',
    author_email='liuzhuogood@foxmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['gencode'],
    package_data={'gencode': ['README.md', 'LICENSE']},
    install_requires=["pydantic", 'db-hammer', 'PyMySQL', 'cx_Oracle', 'click', 'jinja2', 'PyYAML'],
    entry_points={
        'console_scripts': [
            'gencode = gencode.main:run'
        ]
    },
)
