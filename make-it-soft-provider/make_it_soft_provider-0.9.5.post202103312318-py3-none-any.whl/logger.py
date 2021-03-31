# -*-coding:utf8 -*

from colorama import Fore


def info(text, **keyword_parameters):
    write_log(text, Fore.RESET, '[INFO] ', **keyword_parameters)


def error(text, **keyword_parameters):
    write_log(text, Fore.RED, '[ERROR] ', **keyword_parameters)


def success(text, **keyword_parameters):
    write_log(text, Fore.GREEN, '[SUCCESS] ', **keyword_parameters)


def warn(text, **keyword_parameters):
    write_log(text, Fore.YELLOW, '[WARN] ', **keyword_parameters)


def write_log(text, color, preffix, **keyword_parameters):
    if ('show_preffix' in keyword_parameters and not keyword_parameters['show_preffix']):
        preffix = ''
    print(color, preffix, text)
