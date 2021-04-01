from setuptools import setup
setup(
    name='QtSplashScreen',version='5.15.2',description='A PyQt5 Splash Screen Demo and Template',packages=['QtSplashScreen'],license='MIT',entry_points={
        'console_scripts':['QtSplashScreen=QtSplashScreen.__main__:main']
    },install_requires=['PyQt5==5.15.2','pip>=21.0.1','wheel','setuptools>=49.0.0'],python_requires='>=3.8',classifiers=['Programming Language :: Python','Programming Language :: Python :: 3.9','License :: OSI Approved :: MIT License'],author='Pranav',keywords=['QtSplashScreen','SplashScreen']
)