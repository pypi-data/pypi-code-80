from setuptools import setup, find_packages

# with open("./README.md", "rb") as fh:
#     long_description = fh.read()
long_description = "生成代码"

setup(
    name='genCode',
    version='0.0.2',
    description='生成代码',
    author='hammer',
    author_email='liuzhuogood@foxmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    # scripts=['scripts/gcode.py'],
    # package_data={'db_hammer': ['README.md', 'LICENSE']},
    install_requires=["pydantic", 'db-hammer', 'PyMySQL', 'cx_Oracle'],
    entry_points={
        'console_scripts': ['driver=gcode.main:run'], }
)
