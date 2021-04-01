from enum import Enum

from pydantic import BaseModel, Field

from .shared import GenericCompileConfig, GenericRunConfig

__all__ = ["RustTaskConfig", "RustVersion"]


class RustVersion(str, Enum):
    """Rust 版本"""

    v1_51_0 = "v1.51.0"
    v1_50_0 = "v1.50.0"


class RustTaskConfig(BaseModel):
    """Rust 语言任务配置"""

    code: str = Field(..., title="Rust语言代码")
    version: RustVersion = Field(RustVersion.v1_51_0, title="Rust版本")
    compile: GenericCompileConfig = Field(GenericCompileConfig(), title="编译配置")
    run: GenericRunConfig = Field(GenericRunConfig(), title="运行配置")
