from setuptools import setup, find_packages

setup(
    name="FD_byAgCl",
    version="1.2",
    author="AgCl",
    author_email="1914559880@qq.com",
    packages=find_packages("src"),
    package_dir={"": "src"},  # 告诉distutils包都在该目录下
    package_data={  # 配置其他文件的打包处理
        # 任何文件中含有.txt文件，都包含它
        "": ["*.txt", "*.info", "*.properties", "*.py"],
        # 包含demo包中data文件夹中的.bat文件
        "": ["data/*.*"]
    },
    exclude=["*.test", "*.test.*", "test.*", "test"],  # 包含所有src中的包，取消所有的测试包
    description='This is a program for downloading firmwares.'
)