from setuptools import setup

setup(
    name='stockcodes',     # 包名字
    version='0.0.1',   # 包版本
    description='get stock codes of open listed companies in China',   # 简单描述
    author='jopil',  # 作者
    maintainer='jopil',
    author_email='jopil@163.com',  # 作者邮箱
    maintainer_email='jopil@163.com',
    license='MIT',

    packages=['stockcodes'],   # 包
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0"
    ],
    python_requires='>=3.6',
    classifiers = [
        # 发展时期,常见的如下
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # 开发的目标用户
        'Intended Audience :: Developers',

        # 属于什么类型
        'Topic :: Software Development :: Build Tools',

        # 许可证信息
        'License :: OSI Approved :: MIT License',

        # 目标 Python 版本
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)