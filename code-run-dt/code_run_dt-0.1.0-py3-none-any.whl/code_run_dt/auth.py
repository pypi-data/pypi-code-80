from pydantic import BaseModel, Field

__all__ = ["AuthMsg", "AuthRet"]


class AuthMsg(BaseModel):
    typ: str = Field("auth_msg", title="认证请求类型")
    token: str = Field(..., title="认证令牌")


class AuthRet(BaseModel):
    typ: str = Field("auth_ret", title="认证返回类型")
    ok: bool = Field(..., title="是否成功", description="true => 成功, false => 失败, 失败必须断开连接")
