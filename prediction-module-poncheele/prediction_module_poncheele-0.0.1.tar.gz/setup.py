from setuptools import setup

setup(
  name='prediction_module_poncheele',
  version="0.0.1",
  description='make a prediction for fds mtp',
  url='https://github.com/Poncheele/Prediction_velo',
  author='Poncheele',
  author_email='clementponcheele@gmail.com',
  license='FDS',
  packages=['prediction_module', 'prediction_module.io',
            'prediction_module.preprocess', 'prediction_module.data'],
  zip_safe=False
)
