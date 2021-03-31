from setuptools import setup

if __name__ == "__main__":
    setup()

# python setup.py sdist bdist_wheel
# twine check dist/*
# twine upload --repository pypi dist/*