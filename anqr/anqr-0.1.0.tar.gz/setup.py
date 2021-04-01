from distutils.core import setup

setup(
  name = 'anqr',
  packages = ['anqr'],
  version = '0.1.0',
  license='MIT',
  description = "ANQR, A New Quick Response: A new type of qr code, with unlimited space.",
  author = 'Georges Abdulahad',
  author_email = 'ghg.abdulahad@gmail.com',
  url = 'https://github.com/GHGDev-11/ANQR',
  download_url = 'https://github.com/GHGDev-11/ANQR/archive/refs/tags/0.1.0.zip',
  keywords = ["qr code", "scanning", "pillow", "pil", "image"],
  install_requires=['PIL'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)