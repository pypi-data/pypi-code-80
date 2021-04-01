import typing
from .. import exceptions


def ContextManager(
        events: typing.Optional[list] = None, 
        commands: typing.Optional[list] = None, 
        action: typing.Optional[list] = None, 
        # payload: typing.Optional[list] = None
        ):

    def decorator(coro: typing.Callable):
        def registerCommand(self):
            if events:
                from .enums import events as enums_events
                for i in events:
                    if not isinstance(i, enums_events):
                        raise TypeError("Incorrect type!")

                    elif i not in self.event_handlers and i != enums_events.message_new:
                        self.event_handlers[i] = coro
                    else:
                        raise exceptions.LibraryRewriteError(f"{str(i)} is already registered event")
                
                return # coro(self, *args, **kwargs) 

            if commands:
                self.commands.extend(commands)
                self.handler_dict[coro.__name__] = {'handler': coro, 'commands': commands}

                return # coro(self, *args, **kwargs)

            if action:
                from .enums import action as enums_action
                for i in action:
                    if not isinstance(i, enums_action):
                        raise TypeError("use testcanarybot.enums.action for this context!")
                    
                    if i not in self.action_handlers:
                        self.action_handlers[i] = coro
                    
                    else:
                        raise exceptions.LibraryRewriteError(f"{str(i)} is already registered action")


                return # coro(self, *args, **kwargs)

            if not (events or commands or action):
                if self.void_react:
                    raise NameError("Void handler is already created")

                self.void_react = coro
                return # coro(self, *args, **kwargs)
        
        return registerCommand
    return decorator
    
def event(events: list):
    return ContextManager(events = events)


def priority(commands: list):
    return ContextManager(commands = commands)


def void(coro: typing.Callable):
    return ContextManager()(coro)
    

def action(action: list()):
    return ContextManager(action = action)