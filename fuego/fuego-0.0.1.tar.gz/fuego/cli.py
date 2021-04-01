from enum import Enum
from pathlib import Path

import typer
from tabulate import tabulate

from .azml_utils import submit_basic_run

app = typer.Typer()


class GPUType(str, Enum):
    k80 = "K80"
    m60 = "M60"
    v100 = "V100"
    none = "CPU"


def num_gpus_callback(ctx: typer.Context, param: typer.CallbackParam, value: int):
    if value not in [0, 1, 2, 4]:
        raise typer.BadParameter("Num GPUs choice must be 1, 2, or 4.")
    return value


@app.command()
def hello():
    print("hello")


@app.command(
    name="run",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def run(
    ctx: typer.Context,
    script: Path,
    workspace_config: Path = typer.Option(
        "./config.json",
        help="AzureML resource config.json file. Download from Azure portal by going to your resource's page and selecting 'Download config.json'",
    ),
    target_name: str = typer.Option(
        "my-cluster",
        help="The name of the compute cluster to run your script on. If it doesn't exist, we'll create it for you.",
    ),
    gpu_type: GPUType = typer.Option(
        GPUType.k80,
        help="The type of GPU you'd like to be on your cluster. Pass 'CPU' if you don't require a GPU.",
        case_sensitive=False,
    ),
    num_gpus: int = typer.Option(
        1,
        callback=num_gpus_callback,
        help="Number of GPUs per node. Can be 1, 2, or 4. If --gpu_type is CPU, this argument will be ignored, effectively setting it to 0.",
    ),
    min_nodes: int = 0,
    max_nodes: int = 10,
    num_nodes: int = 1,
    dataset_name: str = None,
    dataset_mount_dir: Path = "/dataset",
    experiment_name: str = "pyazml-experiments",
    requirements_file: Path = "./requirements.txt",
    docker_image: str = "mcr.microsoft.com/azureml/openmpi3.1.2-cuda10.2-cudnn8-ubuntu18.04",
):

    assert script.exists(), f"Script file '{script}' does not exist"
    assert (
        workspace_config.exists()
    ), f"Workspace config file '{workspace_config}' does not exist"
    assert (
        requirements_file.exists()
    ), f"Requirements file '{requirements_file}' does not exist"

    submit_basic_run(
        script,
        ctx.args,
        workspace_config,
        target_name,
        gpu_type,
        num_gpus,
        min_nodes,
        max_nodes,
        num_nodes,
        dataset_name,
        dataset_mount_dir,
        experiment_name,
        requirements_file,
        docker_image,
    )


if __name__ == "__main__":
    app()
