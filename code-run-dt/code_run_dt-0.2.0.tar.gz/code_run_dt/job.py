from enum import Enum
from typing import Optional, Any, Literal

from pydantic import BaseModel, Field

__all__ = ["CodeRunTask", "CodeRunReportMsg", "CodeRunTaskState"]


class CodeRunTask(BaseModel):
    """CodeRun 任务"""

    job_id: str = Field(..., title="任务ID")
    lang: Literal["c", "c++", "python", "rust"] = Field(
        "c", title="编程语言", description="code 使用的编程语言"
    )
    code: str = Field(..., title="代码")
    args: str = Field(..., title="参数")
    stdin: str = Field(..., title="标准输入")
    config: Optional[Any] = Field(
        None, title="运行配置", description="运行时配置,每种语言都不一样 参见: run_config 里面的具体配置"
    )


class CodeRunTaskState(str, Enum):
    """CoeRun 任务状态"""

    COMPILE_START = "compile_start"
    COMPILE_DONE = "compile_done"

    RUN_START = "run_start"
    RUN_DONE = "run_done"

    # 失败状态
    F_OK = "f_ok"
    F_COMPILE = "f_compile"
    F_RUN = "f_run"


class CodeRunReportMsg(BaseModel):
    """上报信息消息"""

    job_id: str = Field(..., title="任务ID")
    state: CodeRunTaskState = Field(..., title="任务状态")
    stdout: str = Field("", title="标准输出")
    stderr: str = Field("", title="标准错误")
    # fixed value
    typ: Literal["job.report"] = Field("job.report", title="类型", alias="type")
