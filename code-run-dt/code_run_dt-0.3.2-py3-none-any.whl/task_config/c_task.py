from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .shared import GenericCompileConfig, GenericRunConfig

__all__ = ["CTaskConfig", "CRunConfig", "CAsmConfig", "CCompiler"]


class CCompiler(str, Enum):
    gcc_v10_2 = "gcc:v10.2.0"
    gcc_v10_1 = "gcc:v10.1.0"


class CRunConfig(BaseModel):
    """C语言运行配置"""

    compile: GenericCompileConfig = Field(GenericCompileConfig(), title="编译配置")
    run: GenericRunConfig = Field(GenericRunConfig(), title="运行配置")


class CAsmConfig(BaseModel):
    """C语言汇编配置"""

    timeout: int = Field(10, title="编译超时", description="超时时间")
    max_size: int = Field(64 * 1024, title="ASM 最大的大小")


class CTaskConfig(BaseModel):
    """C语言任务配置"""

    code: str = Field(..., title="C语言代码")
    compiler: CCompiler = Field(
        CCompiler.gcc_v10_2, title="编译器", description="使用的编译器版本"
    )
    asm: Optional[CAsmConfig] = Field(
        None, title="获取汇编", description="asm run 只能有一个不为 None"
    )
    run: Optional[CRunConfig] = Field(
        None, title="运行配置", description="asm run 只能有一个不为 None"
    )
