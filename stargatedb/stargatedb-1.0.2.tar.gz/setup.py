import setuptools
setuptools.setup(
    name="stargatedb", # Replace with your own username
    version="1.0.2",
    author="yangpai",
    author_email="wumeng@mail.yangpai.co",
    description="stargatedb is a microcomputer database developed by Chongqing Yangpai Information Technology Co., Ltd., which supports Chinese and English characters and multimedia data storage. It is mainly used in Internet of things, robot, intelligent hardware, industrial automation and other fields",
    long_description="stargatedb is a microcomputer database developed by Chongqing Yangpai Information Technology Co., Ltd., which supports Chinese and English characters and multimedia data storage. It is mainly used in Internet of things, robot, intelligent hardware, industrial automation and other fields",
    long_description_content_type="text/markdown",
    url="http://www.stargatedb.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7'
)
