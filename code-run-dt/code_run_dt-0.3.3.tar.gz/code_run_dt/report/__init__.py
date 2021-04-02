from typing import Literal

from pydantic import BaseModel, Field

__all__ = ["ReportInfo"]


class ReportInfo(BaseModel):
    job_id: str = Field(..., title="任务ID")
    title: str = Field(..., title="名称")
    end: bool = Field(False, title="结束状态", description="任务是否已经结束")
    msg: str = Field("", title="其他信息", description="展示给用户的其他信息")
    stdout: str = Field("", title="标准输出", description="允许为空")
    stderr: str = Field("", title="标准错误", description="允许为空")
    # fixed value
    typ: Literal["job.report"] = Field("job.report", title="类型", alias="type")
