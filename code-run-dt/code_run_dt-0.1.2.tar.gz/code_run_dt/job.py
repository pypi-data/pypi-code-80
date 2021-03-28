from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["CodeRunJob", "CodeRunState"]


class CodeRunJob(BaseModel):
    job_id: str = Field(..., title="任务ID")
    lang: str = Field(..., title="编程语言")
    code: str = Field(..., title="代码")
    args: str = Field(..., title="参数")
    stdin: str = Field(..., title="标准输入")


class CodeRunState(BaseModel):
    job_id: str = Field(..., title="任务ID")
    state: str = Field(..., title="任务状态")
    stdout: Optional[str] = Field(None, title="标准输出")
    stderr: Optional[str] = Field(None, title="标准错误")
