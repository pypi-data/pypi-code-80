from setuptools import setup

setup(
    name='gcp-data-ingestion',
    version='1.0.6',
    packages=['ingestion', 'ingestion.config', 'ingestion.storage', 'ingestion.storage.gcs',
              'ingestion.storage.bigquery'],
    package_dir={'': 'src'},
    url='https://github.com/sreeraaman/data-ingestion',
    license='MIT',
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
    ]
)
