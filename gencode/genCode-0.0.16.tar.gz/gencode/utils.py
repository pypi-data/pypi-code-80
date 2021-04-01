import os
import re

from db_hammer.util.file import get_dir_files

from gencode.models import Gcode


def get_XxTableName(xx_table_name):
    ts = str(xx_table_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t.capitalize()
        else:
            s += t.capitalize()
    return s


def get_xxTableName(xx_table_name):
    ts = str(xx_table_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t
        else:
            s += t.capitalize()
    return s


def get_table_name(xx_table_name):
    ind = str(xx_table_name).find("_")
    return str(xx_table_name[ind + 1:]).lower()


def get_table_package(xx_table_name):
    ind = str(xx_table_name).find("_")
    return str(xx_table_name[0:ind]).lower()


def get_tableName(xx_table_name):
    table_name = get_table_name(xx_table_name)
    ts = str(table_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t
        else:
            s += t.capitalize()
    return s


def get_TableName(xx_table_name):
    table_name = get_table_name(xx_table_name)
    ts = str(table_name).lower().split("_")
    s = ''
    for t in ts:
        s += t.capitalize()
    return s


def get_columnName(coulum_name):
    ts = str(coulum_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t
        else:
            s += t.capitalize()
    return s


def get_ColumnName(coulum_name):
    ts = str(coulum_name).lower().split("_")
    s = ''
    for t in ts:
        s += t.capitalize()
    return s


def get_path_list(path, encode="utf-8") -> [Gcode]:
    if path is None or path == "":
        path = "./"
    path = os.path.dirname(path)
    ll = get_dir_files(path=path, absolute=True, mode="AFD")
    ls = []
    for a in ll:
        from gencode.config import jinja2_config
        if a.endswith(".gcode") or os.path.isdir(a):
            g = Gcode()
            g.temp_path = a
            g.encode = encode
            if os.path.isdir(a) and jinja2_config["variable_start_string"] in a and jinja2_config[
                "variable_end_string"] in a:
                g.is_dir = True
                g.target_path = a
                ls.append(g)
            if os.path.isfile(a):
                g.is_dir = False
                g.target_path = re.sub("\.gcode$", "", a)
                f = open(g.temp_path, 'rb')
                g.temp_content = f.read().decode(encode)
                f.close()
                ls.append(g)

    return ls


def get_dataType(db_data_type, data_length):
    from gencode.config import data_type_mapping
    for d_key in data_type_mapping.keys():
        d_keys = d_key.split("|")
        if db_data_type in d_keys or f"{db_data_type}({data_length})" in d_keys:
            return data_type_mapping[d_key]
    return db_data_type
