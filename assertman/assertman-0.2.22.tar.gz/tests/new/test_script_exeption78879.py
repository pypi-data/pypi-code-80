from rich.console import Console
import io
from rich.traceback import install
import sys

install()

def get_error_text():
    install()
    console = Console(color_system="256", width=120, file=io.StringIO())
    data = {
        "firstName": "John",
        "lastName": "doe",
        "age": 26,
        "address": {
            "streetAddress": "naist street",
            "city": "Nara",
            "postalCode": "630-0192"
        },
        "phoneNumbers": [
            {
                "type": "iPhone",
                "number": "0123-4567-8888"
            },
            {
                "type": "home",
                "number": "0123-4567-8910"
            }
        ]
    }
    console.print(data)
    return console.file.getvalue()

def do():
    console = Console(file=sys.stderr)

    try:
        install()
        raise AssertionError("\n" + get_error_text())
    except:

        console.print_exception()


def test_ooo():
    install()
    do()





