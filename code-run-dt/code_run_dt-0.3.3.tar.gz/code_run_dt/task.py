from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

__all__ = ["RunTask", "TaskType"]


class TaskType(str, Enum):
    c_run = "lang:c:run"
    c_asm = "lang:c:asm"  # 获取 asm 代码
    kotlin_run = "lang:kotlin:run"
    java_run = "lang:java:run"
    js_run = "lang:javascript:run"
    php_run = "lang:php:run"
    py_run = "lang:python:run"
    ruby_run = "lang:ruby:run"
    rust_run = "lang:rust:run"
    swift_run = "lang:swift:run"


class RunTask(BaseModel):
    """运行任务"""

    job_id: str = Field(..., title="任务ID")
    task_type: TaskType = Field(..., title="任务类型")
    task_config: Any = Field(..., title="任务配置")
