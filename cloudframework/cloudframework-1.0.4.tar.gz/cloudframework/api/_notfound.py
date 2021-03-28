from flask import request, jsonify

class API():

    core = None

    def __init__(self,core):
        self.core = core

    def main(self):

        res = {
            "not-found": ":("
        }
        return jsonify(res)
