from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yk-face-api-model",
    version="2.0.0",
    description="YooniK face API data model package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="YooniK",
    author_email="tech@yoonik.me",
    url="https://yoonik.me",
    license='MIT',
    packages=["yk_face_api_models"],
    install_requires=[
        'six',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)