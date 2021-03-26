from setuptools import setup, find_packages

setup(name='SamplePackage192940',
      version='0.2',
      description='Sample functions',
      long_description='Really, the sampliest functions.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='idk',
      url='http://vk.com/red.snail',
      author='Me',
      author_email='rsanddrs-company@yandex.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)