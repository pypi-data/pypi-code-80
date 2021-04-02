from sys import modules
from pathlib import Path as _asstpath
from . import pluginsdata as _Modules
from .wrappers import *


def pika_assistant(_pikasst=None):
    asstpath = _asstpath(f"./pikabot/Assistant/plugins/{_pikasst}.py")
    asstname = "pikabot.Assistant.plugins.{}".format(_pikasst)
    spec = spec_from_file_location(asstname, asstpath)
    asst = module_from_spec(spec)
    # ____Pikabot__Assistant__Plugins__Loader____
    asst.bot = bot
    asst.tgbot = tgbot
    asst.Var = Var
    asst.rx = rx
    asst.ItzSjDude = ItzSjDude
    asst.pikatgbot = pikatgbot
    modules['Asst_modules'] = _Modules
    PikaAsst[_pikasst] = asst
    modules["pikabot" + _pikasst] = asst
    tgbot.PikaAsst[_pikasst] = asst
    spec.loader.exec_module(asst)
    logpa.info("🔥Imported " + _pikasst)
