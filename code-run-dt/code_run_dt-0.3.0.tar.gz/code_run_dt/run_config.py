from typing import Optional, Union, Literal

from pydantic import BaseModel, Field

__all__ = ["CConfig", "CppConfig", "PythonConfig", "RustConfig"]


class CConfig(BaseModel):
    """C语言运行配置"""

    compiler: Union[Literal["gcc", "clang"]] = Field("gcc", title="编译器")
    # 没有则使用最新版本
    version: Optional[str] = Field(None, title="编译器版本")
    # C 语言标准
    std: Optional[Literal["C89", "C99", "C11", "C17"]] = Field("C11", title="使用 C11 标准")


class CppConfig(BaseModel):
    """C++语言运行配置"""

    compiler: Literal["g++", "clang++"] = Field("g++", title="编译器")
    # 没有则使用最新版本
    version: Optional[str] = Field(None, title="版本")
    # C++ 语言标准
    std: Literal["C++98", "C++03", "C++11", "C++14", "C++17", "C++20"] = Field(
        "C++17", title="C++标准", description="默认使用 C++ 17 标准"
    )


class PythonConfig(BaseModel):
    """Python语言运行配置"""

    interpreter: Literal["CPython", "PyPy"] = Field(
        "CPython", title="Python 解释器", description="当前还不支持 PyPy"
    )
    # 默认是 CPython 3.9 版本
    version: Literal["3.6", "3.7", "3.8", "3.9"] = Field("3.9", title="版本")


class RustConfig(BaseModel):
    """Rust语言运行配置"""

    version: Literal["nightly", "beta", "1.51", "1.50"] = Field(
        "1.51", title="Rust 版本", description="默认使用当前稳定版"
    )
