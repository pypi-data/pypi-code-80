import json

class MateData():
    def __init__(self, matedata):
        # 数据格式检查
        if not type(matedata) is dict:
            raise Exception(f"box must be a dict, {type(matedata)} gavin")
        self.meta = matedata

    def ToString(self):
        return json.dumps(self.meta)
