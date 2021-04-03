from setuptools import setup, find_packages


setup(
    install_requires=[
        'google-cloud-storage',
        'google-cloud-bigquery',
        'PyYAML',
        'pandas_gbq',
        'gcsfs',
        'pytest'
    ],
    packages=find_packages(),
    name='gcp-data-ingestion',
    version='1.0.4'

)
