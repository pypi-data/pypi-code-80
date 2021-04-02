_tag = '__events'  # method attribute to store events
_init_tag = '__custom_init'  # class attribute to mark it having a new __init__


# inserts code into class __init__ to subscribe methods after instantiation
def cls(evt_class):
    # check the class doesn't already have a new_init
    if not hasattr(evt_class, _init_tag):
        old_init = evt_class.__init__

        # this is the new __init__ for the class
        def new_init(obj, *args, **kwargs):  # obj -> self
            # get all methods in object
            for method_name in dir(obj):
                method = getattr(obj, method_name)
                # get method's `_event` event dictionary
                event_dict = getattr(method, _tag, {})
                # for each handler in the dict
                for event_handler, event_names in event_dict.items():
                    # and for each event for each handler
                    for event_name in event_names:
                        # add the method to that handler's event
                        event_handler.add(event_name, method)

            # and run the old __init__ as if nothing happened (don't replace in case they want to re-run this)
            old_init(obj, *args, **kwargs)

        # set the _init_tag attribute to prevent adding another new_init
        setattr(evt_class, _init_tag, True)
        # and add the new __init__
        evt_class.__init__ = new_init

    return evt_class


class EventHandler:
    def __init__(self):
        self._events = {}  # { 'event1': { <function object>, <function object>} }
        self.m = self.method = MethodEventHandler(self)

    def run(self, event_name, *args, **kwargs):
        for callback in self._events.get(event_name, []):
            callback(*args, **kwargs)

    def add(self, event_name, fn):
        if event_name not in self._events:
            self._events[event_name] = set()
        self._events[event_name].add(fn)

    def __getattr__(self, event_name):  # function decorator
        def decorator(fn):
            self.add(event_name, fn)
            return fn

        return decorator


class MethodEventHandler:
    def __init__(self, event_handler):
        self.handler = event_handler

    def __getattr__(self, event_name):  # method decorator
        def decorator(fn):
            event_dict = getattr(fn, _tag, {})  # { <EventHandler object>: [ 'event1', 'EVENT_TWO' ], }
            event_dict[self.handler] = event_dict.get(self.handler, []) + [event_name]
            setattr(fn, _tag, event_dict)
            return fn

        return decorator
