from .rm_option import RMOption
import sys

'''
RMOptionHandler class

Main class for the rm_options package.
Here you can create options, and it takes the handling with it.
'''


class RMOptionHandler(object):
    def __init__(self, usage_title="Usage", usage_description="python {}".format(sys.argv[0]),
                 help_option_short_name="h", help_option_long_name="help", help_option_description="show usage",
                 ask_for_missing_values=True, ask_for_required_options=True):
        self.usage_title = usage_title
        self.usage_description = usage_description
        self.options = []
        self.ask_for_missing_values = ask_for_missing_values
        self.ask_for_required_options = ask_for_required_options
        self.error = None

        # create help option
        self.create_option(help_option_long_name, help_option_description, False, short_name=help_option_short_name)

    # create an option, and add it to options array
    def create_option(self, long_name: str, description: str, needs_value: bool = False,
                      required: bool = False, default_value=None, short_name: str = None,
                      multiple_values: bool = False, mapper=None):
        option = RMOption(long_name, description, needs_value=needs_value,
                          required=required, default_value=default_value, short_name=short_name,
                          multiple_values=multiple_values, mapper=mapper)
        self.options.append(option)
        return option

    def print_error(self):
        print(self.error)

    # prints the usage
    # TODO: seperate required arguments from the optional arguments
    def print_usage(self):
        print(self.usage_title)
        if self.usage_description:
            print("\n{}\n".format(self.usage_description))

        for option in self.options:
            print(
                "--{}{}: {}".format(option.long_name, (lambda: " -" + option.short_name if option.short_name else "")(),
                                    option.description))

    # parse, check and maps the options.
    # for errors it returns False.
    def check(self):
        current_option = None

        # parsing process
        for i in range(1, len(sys.argv)):

            # invalid state, because we have no options, but values
            if not current_option and not sys.argv[i].startswith("-"):
                return False

            # if we have a new option, parse the name, and set it to current_option
            # if the option not exists, return False
            if sys.argv[i].startswith("-"):
                current_option = self.get_option_with_name(sys.argv[i], with_prefix=True)
                if not current_option:
                    return False
                current_option.in_use = True
                continue

            # parse values to the current_option
            if current_option.multiple_values:
                current_option.value.append(sys.argv[i])
            else:
                if current_option.value:
                    return False
                current_option.value = sys.argv[i]

        # checking process
        for option in self.options:
            if not option.complete():
                if not self.ask_for_missing_values:
                    return False
                if option.multiple_values:
                    while "quit" not in option.value:
                        option.value.append(input("values for option {}({}) are needed (input quit to quit): "
                                                  .format(option.long_name, option.description)))
                    option.value.remove("quit")
                    continue
                while option.value == None or option.value == "":
                    option.value = input("option {}({}) is needed: ".format(option.long_name, option.description))

        # mapping process
        for option in self.options:
            if option.mapper:
                if type(option.value) == str:
                    mapper = option.mapper()
                    mapped_value = mapper.map(option.value)
                    if not mapped_value:
                        self.error = "cannot parse '{}' to {} for option '{}'".format(option.value,
                                                                                      mapper.get_target_type_name(),
                                                                                      option.long_name)
                        return False
                    option.value = mapped_value
                else:
                    if option.multiple_values:
                        for i, value in enumerate(option.value):
                            if type(value) == str:
                                mapper = option.mapper()
                                mapped_value = mapper.map(value)
                                if not mapped_value:
                                    self.error = "cannot parse '{}' to {} for option '{}'".format(value,
                                                                                                  mapper.get_target_type_name(),
                                                                                                  option.long_name)
                                    return False
                                option.value[i] = mapped_value

        return True

    # get an option with a name
    # if you have the prefix '-' characters, please set with_prefix = True
    def get_option_with_name(self, name: str, with_prefix: bool = False):
        if with_prefix:
            while name.startswith("-"):
                name = name[1:]

        for option in self.options:
            if name == option.long_name or name == option.short_name:
                return option
