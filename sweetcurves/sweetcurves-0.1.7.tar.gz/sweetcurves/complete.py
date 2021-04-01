from pathlib import Path

import yaml
from devtools import debug
from loguru import logger
from toolz import first

from sweetcurves.catelog.stack import FunctionParameters
from sweetcurves.cloud_build import CloudBuildConfig
from sweetcurves.stackset import StackDockerContext


def update_builds(root_dir: Path):
    stacky = StackDockerContext(root_dir)
    cloudy = CloudBuildConfig(root_dir)

    server_fn = stacky.stack_model.functions
    fn_params: FunctionParameters = first(server_fn.values())

    working_dir: Path = Path.cwd()

    # Here I'm trying to create a dynamic context
    dynamic_context = stacky.ctx.relative_to(working_dir)

    # We're just going to hard code this piece.
    cloudy.name = "gcr.io/cloud-builders/docker"
    cloudy.context = dynamic_context
    cloudy.destination = fn_params.image
    cloudy.set_build_args(fn_params.build_args)
    cloudy.set_env(fn_params.environment)
    cloudy.bm.steps[0].args.append(".")

    cb_file: Path = working_dir / "cloudbuild.yml"
    clouddump = yaml.safe_dump(cloudy.to_dict(), sort_keys=False, indent=4)
    cb_file.write_text(clouddump)
