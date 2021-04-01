class StrUtil:
    @staticmethod
    def isblank(s: str):
        # [None, "", whitespace_str]
        return s is None or not len(s) or s.isspace()
