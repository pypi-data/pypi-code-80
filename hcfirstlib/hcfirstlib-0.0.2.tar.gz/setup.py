import setuptools
setuptools.setup(
    name='hcfirstlib',#库名
    version='0.0.2',#版本号，建议一开始取0.0.1
    author='haowen zhang',#你的名字，名在前，姓在后，例：张一一 Yiyi Zhang
    author_email='806670753@qq.com',#你的邮箱（任何邮箱都行，只要不是假的）
    description='红茶工作室专属库，这个库的代码有一些混杂，回头会进行分类',#库介绍
    long_descripition_content_type="text/markdown",
    url='https://github.com/',
    packages=setuptools.find_packages(),
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent" ,
    ],
)