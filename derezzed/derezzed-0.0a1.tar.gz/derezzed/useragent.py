from derezzed.rechain import RegularExpressionChain

app_patterns = [
    ("keanu", r"^keanu_example/.*"),
    ("riot-desktop", r"^mozilla/5\.0.+riot/[0-9].+electron/[0-9].*$"),
    ("riot.im", r"^riot\.im/.*$"),
    ("riot", r"^riot/.*"),
    ("zom", r"^zom 2/.*$"),
    ("edge", r".*edge.*"),
    ("opera", r".*opera.*"),
    ("firefox", r".*focus.*"),
    ("baidu box app", r".*baiduboxapp.*"),
    ("samsung browser", r".*samsungbrowser.*"),
    ("uc browser", r".*ucbrowser.*"),
    ("chrome", r".*chrome.*"),
    ("safari", r".*safari.*"),
    ("firefox", r".*firefox.*"),
    ("msie", r".*msie.*"),
    ("msie", r".*trident.*"),
    ("wget", r".*wget.*"),
    ("curl", r".*curl.*"),
    ("lynx", r".*lynx.*"),
]

os_patterns = [
    ("ios", r".*ipad.*"),
    ("ios", r".*iphone.*"),
    ("winphone", r".*windows phone.*"),
    ("winphone", r".*windows mobile.*"),
    ("android", r".*android.*"),
    ("windows", r".*windows.*"),
    ("linux", r".*linux.*"),
    ("linux", r".*ubuntu.*"),
    ("mac os x", r".*mac os x.*"),
    ("mac os x", r".*darwin.*"),
    ("mac", r".*mac os.*"),
    ("chrome os", r".*cros.*"),
    ("freebsd", r".*freebsd.*"),
    ("openbsd", r".*openbsd.*"),
    ("watch os", r".*watch.*"),
]


class UserAgentApp(RegularExpressionChain):
    """
    Reduces a user agent string to an application name.
    """
    def __init__(self):
        super().__init__(app_patterns)


class UserAgentOS(RegularExpressionChain):
    """
    Reduces a user agent string to an operating system name.
    """
    def __init__(self):
        super().__init__(os_patterns)
