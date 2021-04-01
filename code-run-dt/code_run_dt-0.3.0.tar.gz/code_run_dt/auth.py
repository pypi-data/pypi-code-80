from typing import Literal

from pydantic import BaseModel, Field

__all__ = ["AuthMsg", "AuthRet"]


class AuthMsg(BaseModel):
    typ: Literal["auth.msg"] = Field("auth.msg", title="认证请求类型", alias="type")
    token: str = Field(..., title="认证令牌")


class AuthRet(BaseModel):
    typ: Literal["auth.ret"] = Field("auth.ret", title="认证返回类型", alias="type")
    ok: bool = Field(..., title="是否成功", description="true => 成功, false => 失败, 失败必须断开连接")
