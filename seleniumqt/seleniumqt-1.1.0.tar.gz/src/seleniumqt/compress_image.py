# coding: utf-8
import base64
import os
from PIL import Image
from io import BytesIO

def screen2base64(window, rect, xy):
    p = './temp/screen_tmp.png'

    if os.path.isdir('./temp/'):
        os.mkdir('./temp/')

    ifpass = os.system(
        'screencapture -R %s,%s,%s,%s %s' % (rect['x'], window['y'] + window['height'] - rect['height'], rect['width'], rect['height'], p))
    if ifpass == 0:
        with open(p, "rb") as fl:
            screenshot = Image.open(fl)
            im = screenshot.convert('RGB')
            im.thumbnail((xy, xy))
            output_buffer = BytesIO()
            im.save(output_buffer, format='JPEG')
            base64_data = base64.b64encode(output_buffer.getvalue())
            t = base64_data.decode()
            return t
