# Modules
import sys

# System-based imports
if sys.platform.startswith("linux"):
    from .readchar_linux import readchar

elif sys.platform == "darwin":
    from .readchar_linux import readchar

elif sys.platform in ("win32", "cygwin"):

    import msvcrt
    from . import keys
    from .readchar_windows import readchar

else:
    raise NotImplementedError("The platform %s is not supported yet" % sys.platform)

# Windows-based codes
if sys.platform in ("win32", "cygwin"):

    #
    # Windows uses scan codes for extended characters. The ordinal returned is
    # 256 * the scan code.  This dictionary translates scan codes to the
    # unicode sequences expected by readkey.
    #
    # for windows scan codes see:
    #   https://msdn.microsoft.com/en-us/library/aa299374
    #      or
    #   http://www.quadibloc.com/comp/scan.htm

    xlate_dict = {
        13: keys.ENTER,
        27: keys.ESC,
        15104: keys.F1,
        15360: keys.F2,
        15616: keys.F3,
        15872: keys.F4,
        16128: keys.F5,
        16384: keys.F6,
        16640: keys.F7,
        16896: keys.F8,
        17152: keys.F9,
        17408: keys.F10,
        22272: keys.F11,
        34528: keys.F12,

        7680: keys.ALT_A,

        # don"t have table entries for...
        # CTRL_ALT_A, # Ctrl-Alt-A, etc.
        # CTRL_ALT_SUPR,
        # CTRL-F1

        21216: keys.INSERT,
        21472: keys.SUPR,    # keys.py uses SUPR, not DELETE
        18912: keys.PAGE_UP,
        20960: keys.PAGE_DOWN,
        18400: keys.HOME,
        20448: keys.END,

        18432: keys.UP,
        20480: keys.DOWN,
        19424: keys.LEFT,
        19936: keys.RIGHT,
    }

    # Main readkey function
    def readkey(getchar_fn = None):

        # Main loop
        while True:

            # Check for a keypress
            if msvcrt.kbhit():

                # Locate key
                ch = msvcrt.getch()
                a = ord(ch)

                # Check key
                if a == 0 or a == 224:
                    b = ord(msvcrt.getch())
                    x = a + (b * 256)

                    try:
                        return xlate_dict[x]

                    except KeyError:
                        return None

                    return x

                else:
                    return ch.decode()
else:

    # Linux-based readkey
    def readkey(getchar_fn = None):

        getchar = getchar_fn or readchar

        # Get character
        c1 = getchar()
        if ord(c1) != 0x1b:
            return c1

        c2 = getchar()
        if ord(c2) != 0x5b:
            return c1 + c2

        c3 = getchar()
        if ord(c3) != 0x33:
            return c1 + c2 + c3

        c4 = getchar()
        return c1 + c2 + c3 + c4
