from enum import Enum

from pydantic import BaseModel, Field

from .shared import GenericRunConfig

__all__ = ["JsTaskConfig", "JsVersion"]


class JsVersion(str, Enum):
    """Js 版本"""

    v15 = "v15"
    v14 = "v14"


class JsTaskConfig(BaseModel):
    """Js 语言任务配置"""

    code: str = Field(..., title="Js语言代码")
    version: JsVersion = Field(JsVersion.v15, title="Js版本")
    run: GenericRunConfig = Field(GenericRunConfig(), title="运行配置")
