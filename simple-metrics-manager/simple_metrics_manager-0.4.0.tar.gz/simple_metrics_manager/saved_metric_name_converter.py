"""Utility to convert saved metric data to a new name and arguments"""

import os
import glob
import shutil

from .dated_cache_manager import _default_name_generation_function


def convert_metric_name(storage_interface, old_name, new_name, simulate=True):
    """Convert a stored metric to a new name.

    This is a simple find-and-replace method for changing a metric's files to have a new name.

    This is useful for things like misspellings, preventing future name clashes,
    and general code refactoring in the case where it is prohibitively expensive
    to delete the cached files and rebuild them.

    The parameters will not be changed.
    If you need them to change as well, see convert_metric_name_and_arguments.

    The storage_interface is used to find the metrics directory.

    By default, this simulates (aka prints) the files to transfer.
    To actually do the transfer, set "simulate=False".
    """

    metrics_dir = storage_interface.metrics_dir
    file_ext = storage_interface.file_ext

    old_base_name = os.path.join(metrics_dir, old_name)
    new_base_name = os.path.join(metrics_dir, new_name)
    existing_cached_metrics = glob.glob(f"{old_base_name}*{file_ext}")
    for old_file in existing_cached_metrics:
        params_and_extension = old_file[len(old_base_name) :]
        new_file = new_base_name + params_and_extension
        if simulate:
            print(f"simulate move {old_file} to {new_file}")
        else:
            shutil.move(old_file, new_file)

    print(f"Moved all {old_base_name}* to {new_base_name}*")
    print(f"Moved a total of {len(existing_cached_metrics)} files")


def convert_metric_name_and_arguments(
    storage_interface,
    old_name,
    new_name,
    old_params_list,
    new_params_list,
    name_generation_function=None,
    simulate=True,
):
    """A method for surgically replacing a metric with an updated name and parameters.

    This is most useful for when you decide to reorder or add more parameters to a metric,
    but it is prohibitively expensive to delete the cached files and rebuild them.

    IMPORTANT:
    It is up to you to ensure that the new metric with the new parameters is actually
    equivalent to the old one.
    This is basically a fancy hack, so USE AT YOUR OWN RISK.
    If possbile, make a copy of your metrics directory before running this to be safe.

    Parameters are passed as two matched lists (old_params_list and new_params_list)
    where the file names will be replaced one by one based on finding the old file
    that matches the name and parameters and converting a file with the new name and parameters.

    The storage_interface is used to find the metrics directory and the file extension.

    The default name_generation_function is used, but if you provide a custom one instead,
    make sure to pass it here as well.

    Any "*_date*" files are automatically included as well (see DatedCacheManager for more details on date files).

    Any files that are not covered by the old_params_list will throw errors (even in simulation mode).
    This is intentional as it protects against many types of mistakes.
    If you need more nuanced behavior, feel free to hack this function to your own ends.

    By default, this simulates (aka prints) the files to transfer.
    To actually do the transfer, set "simulate=False".
    """

    metrics_dir = storage_interface.metrics_dir
    file_ext = storage_interface.file_ext

    if name_generation_function is None:
        name_generation_function = _default_name_generation_function

    old_base_name = os.path.join(metrics_dir, old_name)
    new_base_name = os.path.join(metrics_dir, new_name)

    existing_cached_metrics_files = glob.glob(f"{old_base_name}*{file_ext}")

    file_name_conversion_dict = {}
    for old_params, new_params in zip(old_params_list, new_params_list):
        old_str = name_generation_function(old_base_name, old_params)
        new_str = name_generation_function(new_base_name, new_params)
        file_name_conversion_dict[f"{old_str}{file_ext}"] = f"{new_str}{file_ext}"
        file_name_conversion_dict[
            f"{old_str}_date{file_ext}"
        ] = f"{new_str}_date{file_ext}"

    for old_file in existing_cached_metrics_files:
        new_file = file_name_conversion_dict[old_file]
        if simulate:
            print(f"simulate move {old_file} to {new_file}")
        else:
            shutil.move(old_file, new_file)

    print(
        f"Moved all {old_base_name}* that matched input parameters to {new_base_name}*"
    )
    print(f"Moved a total of {len(existing_cached_metrics_files)} files")

