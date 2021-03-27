from pathlib import Path

from setuptools import find_packages, setup

import sqspy.about as about

if __name__ == "__main__":
    setup(
        name=about.NAME,
        version=about.VERSION,
        description="AWS SQS utility package for producing and consuming messages",
        long_description=Path("README.rst").read_text(),
        url="https://github.com/hjpotter92/sqspy",
        author=about.AUTHOR["name"],
        author_email=about.AUTHOR["email"],
        license="MIT",
        include_package_data=True,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: Implementation",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        python_requires=">=3.6",
        project_urls={
            "Documentation": "https://sqspy.rtfd.io/",
            "Code coverage": "https://app.codecov.io/gh/hjpotter92/sqspy",
            "Builds history": "https://travis-ci.com/hjpotter92/sqspy",
            # "Changelog": "https://sqspy.rtfd.io/changelog",
        },
        platforms=["any"],
        tests_require=(
            "codecov>=2.1.11",
            "coverage>=5.4",
            "pytest>=6.2.2",
        ),
        keywords="aws sqs messages producer consumer",
        packages=find_packages(exclude=["docs", "tests", "tests.*"]),
        install_requires=["boto3>=1"],
    )
