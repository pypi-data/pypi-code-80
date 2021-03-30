from pydantic import ValidationError

from .auth import AuthMsg, AuthRet
from .job import CodeRunReportMsg

__all__ = []  # 测试不需要导入


def test_auth_msg():
    AuthMsg(token="1")
    AuthMsg(type="auth.msg", token="2")


def test_auth_ret():
    AuthRet(ok=True)
    AuthRet(type="auth.ret", ok=True)


def test_good_code_run_state():
    v = CodeRunReportMsg(job_id="123", state="compile_start")  # noqa
    print(v.json())


def test_bad_code_run_state():
    try:
        CodeRunReportMsg(job_id="123", state="this is a bad state")  # noqa
    except ValidationError:
        pass
