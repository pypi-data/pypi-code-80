from pydantic import BaseModel, Field

__all__ = ["GenericCompileConfig", "GenericRunConfig"]


class GenericCompileConfig(BaseModel):
    """通用编译配置"""

    max_stdout: int = Field(64 * 1024, title="最大标准输出(stdout)输出长度")
    max_stderr: int = Field(64 * 1024, title="最大标准错误(stderr)输出长度")
    timeout: int = Field(10, title="编译超时", description="最长编译时间")


class GenericRunConfig(BaseModel):
    """通用运行配置"""

    args: str = Field("", title="命令行参数")
    stdin: str = Field("", title="标准输入")
    max_stdout: int = Field(64 * 1024, title="最大标准输出(stdout)输出长度")
    max_stderr: int = Field(64 * 1024, title="最大标准错误(stderr)输出长度")
    timeout: int = Field(10, title="运行超时", description="最长的运行时间")
