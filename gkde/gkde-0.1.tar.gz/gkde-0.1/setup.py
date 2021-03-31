from setuptools import setup, find_packages

setup(name='gkde',
      version='0.1',
      description='Gaussian kernel density estimation',
      long_description='Gaussian kernel density estimation',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'torch==1.7.0',
          
      ],
      include_package_data=True,
      zip_safe=False)