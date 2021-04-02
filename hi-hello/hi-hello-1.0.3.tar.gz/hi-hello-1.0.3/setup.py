import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hi-hello",
    version="1.0.3",
    author="Pru",
    author_email="pru@spike.sh",
    description="Just saying hello.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://spike.sh",
    install_requires=[],
    package_dir={"": "src"},
    #packages=['src/hi_hello'],
    # package_data={
    #     # 'needle_sdk': ['core/classes.py', 'core/needle_app.py', 'core/utilities.py', 'core/wrappers.py',
    #     #                'core/libinjection2/linux/_libinjection.so', 'core/libinjection2/linux/libinjection.py',
    #     #                'core/libinjection2/mac_x86_64/_libinjection.so',
    #     #                'core/libinjection2/mac_x86_64/libinjection.py',
    #     #                'core/data/js_event', 'core/data/unix_cmd', 'core/data/scan']
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
