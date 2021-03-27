import builtins
import functools

from segno import QRCode


def check_is_notebook() -> bool:
    """Checks if the current environment is a Python notebook."""
    return hasattr(builtins, "__IPYTHON__")


IS_NOTEBOOK = check_is_notebook()


def only_notebook(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if IS_NOTEBOOK:
            return func(*args, **kwargs)
        else:
            raise RuntimeError("Attempting to run notebook utility in a non-notebook environment.")

    return wrapper


@only_notebook
def show_qr(qr: QRCode):
    """Generates and displays a QR code."""
    from IPython.display import SVG
    return SVG(
        qr.svg_inline(scale=10, light="#fff")
    )
