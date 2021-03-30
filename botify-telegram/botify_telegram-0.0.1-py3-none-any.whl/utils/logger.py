import os
from datetime import datetime

class BotifyLogger():
    def __init__(self, name = "root", parent = None, children = []):
        self.name = name
        self.parent = parent
        self.children = children
        self.root = self.get_root()

    def __repr__(self): return f"<BotifyLogger '{self.root}' children: {self.children}>"

    def get_root(self):
        root = self.name
        if self.parent: root = self.parent.get_root() + "." + root
        return root

    def log(self, message, level = "INFO"):
        now = datetime.now()
        message = f"[{now.strftime('%H:%M:%S')}][{self.root}] {message}"
        print(message)

        filename = now.strftime(f"{level} %d-%m-%Y.log")
        path = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(path): os.mkdir(path)
        path = os.path.join(path, filename)
        with open(path, "a+", encoding = "utf-8") as _file: _file.write(f"{message}\n")

    def info(self, message): self.log(message)
    def error(self, message): self.log(message, level = "ERROR")
    def warning(self, message): self.log(message, level = "WARNING")