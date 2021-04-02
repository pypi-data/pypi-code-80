import json

class LabelData():
    def __init__(self):
        self.labels = []

    def AddLabels(self, label="", instance="", attrs={}, ltype="", data={}):
        label = {
            "label":label,
            "instance":instance,
            "ltype":ltype,
            "attrs":attrs,
            "data":data,
        }
        self.labels.append(label)

    def ToString(self):
        return json.dumps(self.labels)

