from enum import Enum

from pydantic import BaseModel, Field

from .shared import GenericRunConfig

__all__ = ["PythonTaskConfig", "PythonVersion"]


class PythonVersion(str, Enum):
    """Python 版本"""

    v3_9 = "v3.9"
    v3_8 = "v3.8"


class PythonTaskConfig(BaseModel):
    """Python 语言任务配置"""

    code: str = Field(..., title="Python语言代码")
    version: PythonVersion = Field(PythonVersion.v3_9, title="Python版本")
    run: GenericRunConfig = Field(GenericRunConfig(), title="运行配置")
