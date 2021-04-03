from feapder.utils import tools

url = "https://oapi.dingtalk.com/robot/send?access_token=5ce47232d4183665e93e7d7bf66a914d53c8c62d2d5b4558f94cd3475d24b653"

tools.dingding_warning("feapder test", url=url, user_phone="13811037553")
