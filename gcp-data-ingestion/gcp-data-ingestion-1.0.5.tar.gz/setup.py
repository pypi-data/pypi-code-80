from setuptools import setup

setup(
    name='gcp-data-ingestion',
    version='1.0.5',
    packages=['ingestion', 'ingestion.config', 'ingestion.storage', 'ingestion.storage.gcs',
              'ingestion.storage.bigquery'],
    package_dir={'': 'src'},
    url='',
    license='',
    author='Sriraman Gopalan',
    author_email='sreeraaman@gmail.com',
    description='Utility Functions for Data Ingestion in GCP',
    install_requires=[
        'google-cloud-storage',
        'google-cloud-bigquery',
        'PyYAML',
        'pandas_gbq',
        'gcsfs',
        'pytest'
    ]
)
