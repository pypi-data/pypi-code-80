import os

import click
from jinja2 import Template

from gencode.data import get_data
from gencode.models import Gcode
from gencode.utils import get_path_list


def render(data):
    from gencode.config import target_encoding, template_path
    # 路径经过模板
    for gcode in get_path_list(path=template_path, encode=target_encoding):
        g = to_template(gcode, data)
        if g is not None:
            gen_result(g)


def to_template(gcode: Gcode, data) -> Gcode:
    from gencode.config import jinja2_config
    try:
        if not gcode.is_dir:
            template = Template(gcode.temp_content, variable_start_string=jinja2_config["variable_start_string"],
                                variable_end_string=jinja2_config["variable_end_string"])
            txt = template.render(data)
            gcode.target_content = txt
        template = Template(gcode.target_path, variable_start_string=jinja2_config["variable_start_string"],
                            variable_end_string=jinja2_config["variable_end_string"])
        result = template.render(data)
        gcode.target_path = result
        return gcode
    except Exception as e:
        print("============错误==============")
        print(f"模板：{gcode.temp_path}")
        print(f"信息：{e}")


def gen_result(gcode: Gcode):
    """生成目录和文件"""
    if gcode.is_dir:
        os.makedirs(gcode.target_path, exist_ok=True)
    else:
        os.makedirs(os.path.dirname(gcode.target_path), exist_ok=True)
        f = open(gcode.target_path, mode="wb+")
        f.write(gcode.target_content.encode(encoding=gcode.encode))
        f.flush()
        f.close()


@click.command()
@click.option("-c", default="", help="配置文件")
@click.option("-ui", default=0, help="启动UI的端口")
def run(c, ui):
    if c == "":
        print("请使用 -c 参数，比如 gencode -c config.yml")

    from gencode.config import load_conf
    if load_conf(c):
        d = get_data(table_name="sys_menu_router")
        render(data=d)


if __name__ == '__main__':
    run()
