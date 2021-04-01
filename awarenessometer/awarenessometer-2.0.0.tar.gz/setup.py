import setuptools

setuptools.setup(name='awarenessometer',
                 version='2.0.0',
                 description='Report generator for artifact-o-mat results',
                 url='https://gitlab.com/itsape/awarenssometer',
                 author='Timo Pohl, Arnold Sykosch',
                 maintainer='Arnold Sykosch',
                 packages=['awarenessometer'],
                 entry_points={
                     'console_scripts': ['awareness-o-meter=awarenessometer'
                                         '.__main__:create_report']
                 },
                 python_requires='>=3.7',
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: OS Independent'
                 ],
                 include_package_data=True
                 )
