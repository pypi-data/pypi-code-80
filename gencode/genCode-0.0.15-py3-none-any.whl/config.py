import os

import pymysql
import yaml

DB_CONF = {
    "db_type": "MySQL",
    "db_name": "mysql",
    "user": "root",
    "pwd": "123456",
    "host": "127.0.0.1",
    "table_name": ["sys_menu_router"]
}

data_type_mapping = {
    "varchar(*)|text": "String"
}

target_encoding = "utf-8"
jinja2_config = {}
template_path = ""
myself = {}


def load_conf(path):
    if not os.path.isfile(path):
        pwd = os.path.dirname(__file__)
        if os.path.isfile(os.path.join(pwd, path)):
            path = os.path.join(pwd, path)
        else:
            print(f"找不到配置文件：{path}")
            return False

    global DB_CONF, data_type_mapping, target_encoding, template_path, myself
    c = yaml.safe_load(open(path).read())
    template_path = c.get("templatePath", os.path.dirname(path))
    DB_CONF = c.get("dbConf", DB_CONF)
    data_type_mapping = c["dataTypeMapping"]
    data_type_mapping = c["dataTypeMapping"]
    jinja2_config["variable_start_string"] = c.get("variable_start_string", "{{")
    jinja2_config["variable_end_string"] = c.get("variable_end_string", "}}")
    myself = c.get("myself", "{}")
    return True

