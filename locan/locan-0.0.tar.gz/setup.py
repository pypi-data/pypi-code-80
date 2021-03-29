from setuptools import setup
setup(
    use_scm_version={"write_to": "project/_version.py",
                     "fallback_version": "0.0.1"}
    )
