import random
import string
from PIL import Image, ImageDraw, ImageFont
import pathlib

FONT_DIR = pathlib.Path(__file__).resolve().parent.parent.joinpath('font')
print(FONT_DIR)


def rand_chr():
    """
    返回一个随机的大写字母或者数字
    :return:
    """

    ori_chars = string.ascii_uppercase + string.digits
    return random.choice(ori_chars)


def rand_color():
    """
    返回一个随机颜色RGB值
    :return: 返回值是一个元组类似于：(255, 30, 45)
    """

    return random.randint(65, 255), random.randint(65, 255), random.randint(65, 255)


def core_func():
    """
    实现创建一个随机验证码
    :return:
    """

    width, height = 240, 60
    # 创建img对象
    img = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建font对象
    font = ImageFont.truetype(font=f'{FONT_DIR}/PingFang Regular.ttf', size=36)

    # 创建draw对象
    draw = ImageDraw.Draw(img)

    # 填充每个像素
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rand_color())

    # 输出文字
    for t in range(4):
        draw.text((60 * t + 10, 10), rand_chr(), fill=rand_color(), font=font)

    img.save('verify_code.png')


if __name__ == '__main__':
    core_func()
