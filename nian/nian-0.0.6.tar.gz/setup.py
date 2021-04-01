import setuptools
setuptools.setup(
    name="nian", # Replace with your own username  #自定义封装模块名与文件夹名相同
    version="0.0.6",
    author="初慕苏流年", #作者
    author_email="1274210585@qq.com", #邮箱
    description="白嫖音乐", #描述
    long_description='白嫖音乐', #描述
    long_description_content_type="text/markdown", #markdown
    url="", #github地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", #License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',  #支持python版本
)
