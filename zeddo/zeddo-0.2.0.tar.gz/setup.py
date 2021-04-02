import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent
readme = (here / 'README.md').read_text()

setup(
    name='zeddo',
    version='0.2.0',
    packages=find_packages(),
    install_requires=['click', 'requests', 'click-config-file', 'toml'],
    entry_points='''
        [console_scripts]
        zeddo=zeddo.__init__:main
    ''',
    description='News CLI for lazy people',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='cli news current events tool',
    url='http://github.com/clabe45/zeddo',
    author='Caleb Sacks',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Office/Business :: News/Diary'
    ]
)
