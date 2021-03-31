import os
import sys
import dofast.utils as df

path = sys.path[-1]


def decode(keyword: str):
    return df.shell(f'{path}/vps/decode {keyword}').strip()
