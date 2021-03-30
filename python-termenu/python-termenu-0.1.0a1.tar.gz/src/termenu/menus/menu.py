# Modules
import colorama
from .options import OptionHandler

from ..utils.readchar import readkey, keys
from ..utils.ascii import AsciiHolder, clear

from ..utils.exceptions import OptionAlreadyExists

# Menu class
class Menu(object):

    """The main Menu class to use for creating menus"""

    def __init__(self, label = None):
        self.index = 0
        self.label = label

        self.after = None
        self.active = True

        self.ascii = AsciiHolder()
        self.options = OptionHandler()

    def add_option(self, text, callback):

        """Takes text and a callback and creates an option from it"""

        self.options.add(text, callback)

    def option(self, text):

        """Internal decorator for add_option"""

        def inner_wrapper(callback):
            return self.add_option(text, callback)

        return inner_wrapper

    def after_invoke(self):

        """Calls the given function everytime a callback is invoked"""

        def inner_wrapper(callback):
            self.after = callback

        return inner_wrapper

    def display(self):

        """Shows the menu on the screen once, use .mainLoop() for a repeating menu"""

        # Ensure colorama is initialized
        colorama.init()

        # Create a main loop
        while True:

            # Clear screen
            clear()

            # Print label
            if self.label is not None:
                print(self.label)
                print()

            # Print out all of our options
            for opt in self.options:

                i = self.options.index(opt)
                if i == self.index:
                    print(self.ascii.is_active(opt["text"]))

                else:
                    print(self.ascii.not_active(opt["text"]))

            # Read character input
            r = readkey()
            if r == keys.UP:
                self.index -= 1

            if r == keys.DOWN:
                self.index += 1

            if r == keys.ENTER:
                clear()  # Fix the screen

                opt = self.options.get(self.index)
                opt["callback"]()

                # Call our after invoke
                if self.after is not None:
                    self.after()

                return

            # Fix index
            if self.index < 0:
                self.index = len(self.options.options) - 1

            if self.index + 1 > len(self.options.options):
                self.index = 0

    def close(self):

        """'Kills' the menu instance, allowing you to stop it from reoccuring.
        In the event you end up mass spamming this, just use the .display() method
        on the menu rather than .mainLoop()

        This function can also be recreated simply by using .active = False"""

        self.active = False

    def mainLoop(self):

        """Makes an infinite loop of the menu"""

        # Main loop
        self.active = True
        while self.active:
            self.display()
