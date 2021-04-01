from pathlib import Path

import sh
from loguru import logger


def process_output(line: str):
    line = line.strip('\n')
    logger.log("BASH", line)


def run_pex_build(project_name: str, origin: Path = Path.cwd()):
    logger.info(f"{project_name} is starting ... ")
    pex = sh.Command("pex")
    _origin = str(origin.resolve())
    pex_process = pex(
        _origin,
        "-v",
        "-c",
        project_name,
        "-o",
        project_name,
        "--disable-cache",
        "--interpreter-constraint",
        ">=3.7.0,<4.0.0",
        _out=process_output,
        _err=process_output,
        _bg=True,
    )

    pex_process.wait()
    pex_path = origin / "project_name"
    if pex_path.exists():
        logger.error("The PEX build failed")
        return False
    logger.success("Successfully built PEX file")
    return True
