from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nickffs-transliteration", # Replace with your own username
    version="0.0.6",
    author="bhavnicksm",
    author_email="bhavnicksm@gmail.com",
    description="Hinglish --> Hindi transliteration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bhavnicksm/nickffs-transliteration",
    project_urls={
        "Bug Tracker": "https://github.com/Bhavnicksm/nickffs-transliteration/issues",
    },
    keywords = [
        'Artificial Intelligence',
        'Transliteration',
        'PyTorch',
        'Hindi',
        'Hinglish'
    ],
    install_requires=[
        "torch >= 1.6", 
        "torchtext>=0.8",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "model"},
    packages= find_packages(where="model"),
    python_requires=">=3.6",
)