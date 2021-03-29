import setuptools

setuptools.setup(
    name="tail-envs",
    version="0.0.1",
    author="Tail-UFPB",
    author_email="tail.ufpb@gmail.com",
    description="OpenAI Gym environments produced by Tail-UFPB",
    url="https://github.com/TailUFPB/tail-envs",
    project_urls={
        'Source': "https://github.com/TailUFPB/tail-envs",
        'Tracker': "https://github.com/TailUFPB/tail-envs/issues"
    },
    license="MIT",
    packages=['tail_envs'],
    install_requires=['pygame','gym'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)