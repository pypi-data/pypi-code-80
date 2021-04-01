from midas.util.logging_util import setup_logging
from midas.scenario import Configurator
from midas.tools import config


def main():
    setup_logging("DEBUG", "midas_debug")
    params = {}
    cfg = Configurator("midasmv_der")
    scenario = cfg.configure()
    cfg.run()


if __name__ == "__main__":
    main()
