from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='gcp-data-ingestion',
    version='1.0.22',
    packages=['ingestion', 'ingestion.config', 'ingestion.storage', 'ingestion.storage.gcs',
              'ingestion.storage.bigquery'],
    package_dir={'': 'src'},
    url='https://github.com/sreeraaman/data-ingestion',
    # license='MIT',
    author='Sriraman Gopalan',
    author_email='sreeraaman@gmail.com',
    description='Utility Functions for Data Ingestion in GCP',
    python_requires='>=3.8',
    install_requires=[
        'google-cloud-storage',
        'google-cloud-bigquery',
        'PyYAML',
        'pandas_gbq',
        'gcsfs',
        'pytest'
    ],
    long_description=long_description,
    include_package_data=True
)
