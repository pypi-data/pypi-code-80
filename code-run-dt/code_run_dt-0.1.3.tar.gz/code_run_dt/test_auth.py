from .auth import AuthMsg, AuthRet

__all__ = []  # 测试不需要导入


def test_auth_msg():
    AuthMsg(token="1")
    AuthMsg(type="auth.msg", token="2")


def test_auth_ret():
    AuthRet(ok=True)
    AuthRet(type="auth.ret", ok=True)
