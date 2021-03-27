import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


def install_deps():
    """Reads requirements.txt and preprocess it
    to be feed into setuptools.

    This is the only possible way (we found)
    how requirements.txt can be reused in setup.py
    using dependencies from private github repositories.

    Links must be appendend by `-{StringWithAtLeastOneNumber}`
    or something like that, so e.g. `-9231` works as well as
    `1.1.0`. This is ignored by the setuptools, but has to be there.

    Warnings:
        to make pip respect the links, you have to use
        `--process-dependency-links` switch. So e.g.:
        `pip install --process-dependency-links {git-url}`

    Returns:
         list of packages and dependency links.
    """
    default = open("requirements.txt", "r").readlines()
    new_pkgs = []
    links = []
    for resource in default:
        if "git+ssh" in resource:
            pkg = resource.split("#")[-1]
            links.append(resource.strip() + "-9876543210")
            new_pkgs.append(pkg.replace("egg=", "").rstrip())
        else:
            new_pkgs.append(resource.strip())
    return new_pkgs, links


pkgs, new_links = install_deps()

setuptools.setup(
    name="narkdown",
    version="1.3.3",
    author="younho9",
    author_email="younho9.choo@gmail.com",
    description="A tool to use Notion as a Markdown editor.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/younho9/narkdown",
    install_requires=pkgs,
    dependency_links=new_links,
    include_package_data=True,
    packages=setuptools.find_packages(),
    keywords=["notion", "github", "markdown"],
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
