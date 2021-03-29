import setuptools

# 自动读取readme-->长描述使用的
with open("README.md", "r") as f:
    readme = f.read()

# 第三方依赖-->安装目标软件包之前,必须安装依赖的第三方包-->也可以写成requirements.txt文件形式
requires = [
    "requests>=2.25.1"
]

setuptools.setup(
    name='wzj',  # 包(模块)名称
    version='1.0',  # 包版本
    description='简单描述',  # 包详细描述
    long_description=readme,  # 长(详细)描述，通常是readme，打包到PiPy需要
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    author='wzj',  # 作者名称
    author_email='18238816520@qq.com',  # 作者邮箱
    url='https://github.com/wzj/wzj',  # 项目官网(模块地址、也可以自定义位置)
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块(from .. import ..),不用手动指定
    include_package_data=True,  # 是否需要导入静态数据文件
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖(3.4+)
    install_requires=requires,  # 第三方库依赖(也可以以requirements.txt文件)
    classifiers=[  # 程序的所属分类列表(元数据信息)-->这里列出部分
        'Development Status :: 5 - Production/Stable',
        "Environment :: Web Environment",
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
