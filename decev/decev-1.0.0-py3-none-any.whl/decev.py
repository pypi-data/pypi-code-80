import inspect


class EventHandler:
    def __init__(self):
        self._events = {}  # { 'event1': { <function object>, <function object>} }
        self._function_tag = '_events'

    def run(self, event_name):
        for callback in self._events.get(event_name, []):
            callback()

    def cls(self, cls):
        old_init = cls.__init__

        # this is the new __init__ for the class
        def new_init(obj, *args, **kwargs):  # obj -> self
            # get all methods in object
            for method_name in dir(obj):
                method = getattr(obj, method_name)
                # get any & all event names stored in method's `_events` attribute
                events_names = getattr(method, self._function_tag, [])
                # for each event name
                for event_name in events_names:
                    # add the callback to the event's set
                    self.add_callback(method, event_name)

            # and run the old __init__ as if nothing happened (don't replace in case they want to re-run this)
            old_init(obj, *args, **kwargs)

        # and add the new __init__
        cls.__init__ = new_init
        return cls

    def add_callback(self, function, event_name):
        if event_name not in self._events:
            self._events[event_name] = set()
        self._events[event_name].add(function)

    def __getattr__(self, event_name):  # decorator function
        def decorator(function):
            parameters = len(inspect.signature(function).parameters)
            if parameters == 0:  # unbound function, add straight away
                self.add_callback(function, event_name)
            elif parameters == 1:  # method, requires self, tagged for later subscription
                event_names = getattr(function, self._function_tag, []) + [event_name]
                setattr(function, self._function_tag, event_names)
            else:  # too many parameters, throw error
                raise TypeError(f'{function.__name__}() was added to {event_name} event but had too many parameters')

            return function

        return decorator
