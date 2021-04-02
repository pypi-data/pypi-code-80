"""
RMOption class

represents a single option.
It's better if you use the RMOptionHandler class, which automatically handles this options.
"""


class RMOption(object):

    def __init__(self, long_name: str, description: str, required: bool = False,
                 default_value=None, short_name: str = None,
                 needs_value=False, multiple_values: bool = False, mapper=None):
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.required = required
        self.default_value = default_value
        self.needs_value = needs_value
        self.multiple_values = multiple_values
        self.value = (lambda: [] if multiple_values else None)()
        self.in_use = False
        self.mapper = mapper

    # usage of this option
    def usage(self):
        return "--{}{}: {}{}{}{}".format(self.long_name, (lambda: " -" + self.short_name if self.short_name else "")(),
                                         self.description,
                                         (lambda: " {value needed}" if self.needs_value else "")(),
                                         (lambda: " {{default: {}}}".format(
                                             self.default_value) if self.default_value is not None else "")(),
                                         (lambda: " {multiple values possible}" if self.multiple_values else "")())

    # check if the option has a value
    def has_value(self):
        return self.value is not None and self.value != []

    # check if the input of the option was complete
    def complete(self):
        # check if the option is in use, and check also the required state
        if not self.in_use:
            if self.required:
                # set the default_value if it's required, but not given by user.
                # because we have a default_value we don't need an input. #github issue #2
                if self.default_value is not None:
                    self.value = self.default_value
                    return True
                return False
            return True

        # if we don't need a value
        if not self.needs_value:
            return True

        if self.value is not None and self.value != []:
            return True

        # if we don't have a value, but we have a default value, we set it to the value
        # and return true
        if self.default_value is not None:
            self.value = self.default_value
            return True

        return False
