from setuptools import setup

setup(name='infernite',
      version='0.0.1',
      description='Python client for Infernite',
      url='https://github.com/generative-technology/Infernite-python',
      author='Generative Technology Limited',
      author_email='li@generative.technology',
      license='MIT',
      packages=['infernite'],
      install_requires=["requests"],
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent"
      ],
      )
