import glob
from lyncs_setuptools import setup

setup(
    "lyncs_cppyy",
    install_requires=[
        "cppyy>=1.8.1",
        "numpy",
        "deprecated",
        "lyncs_utils",
    ],
    keywords=[
        "Lyncs",
        "cppyy",
    ],
    extras_require={
        "test": ["pytest", "pytest-cov", "meson", "ninja"],
    },
    data_files=[
        ("test/cnumbers", glob.glob("test/cnumbers/*")),
        ("lyncs_cppyy", glob.glob("lyncs_cppyy/*.h")),
    ],
    package_data={"lyncs_cppyy": ["*.h"]},
    include_package_data=True,
)
