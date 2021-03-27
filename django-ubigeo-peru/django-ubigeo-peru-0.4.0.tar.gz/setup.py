import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name='django-ubigeo-peru',
    version='0.4.0',
    license='BSD',
    description='Django app for applications that require to use the ubigeos of INEI of Peru.',
    long_description=long_description,
    author='Miguel Ángel Cumpa Ascuña',
    author_email='miguel.cumpa@yandex.com',
    url='https://gitlab.com/miguelcumpa/django-ubigeo-peru',
    download_url='https://pypi.org/project/django-ubigeo-peru/',
    keywords=['ubigeos', 'peru'],
    packages=setuptools.find_packages(),
    install_requires=[
        'django',
        'djangorestframework',
        'django-filter',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    include_package_data=True,
    zip_safe=False,
)
