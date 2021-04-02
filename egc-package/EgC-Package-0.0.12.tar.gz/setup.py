import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EgC-Package", # Replace with your python folder name 
    version="0.0.12",
    install_requires=["requests", "keras"],
    author="rrpari",# Replace with your own username
    author_email="EGC@example.com",# Replace with your own username
    description="A small example package from EGC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EgC-Team/EngineeringGoesCloud",
    #packages=["src","src.demo"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)