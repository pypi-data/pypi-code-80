from .data import *
from .decorators import *
from .tools import tools

class libraryModule:
    codename = ""
    name = ""
    description = ""

    void_react = False
    event_handlers = {}
    action_handlers = {}

    def __init__(self):
        self.commands = []
        self.handler_dict = {}
        self.void_react = False
        self.event_handlers = {} # event.abstract_event: []