import os
import glob

modulel_list = glob.glob(os.path.join(
    os.path.dirname(__file__), '[a-zA-Z0-9]*.py'))
__all__ = [
    os.path.split(os.path.splitext(file)[0])[1]
    for file in modulel_list
]
