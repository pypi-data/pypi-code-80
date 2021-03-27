from typing import Any, Dict, Union

from mmcc_framework import Process


def validate_process(process:  Union["Process", Dict[str, Any]]) -> None:
    """ Performs some checks on the description, both syntactic and semantic.

    If the check is successful this returns normally, otherwise raises an exception.

    This checks that:
    - If process is a dictionary
        - it contains the list of activities and the id of the first one
        - each activity has an id and a valid type
        - each activity provides some choices according to its type
        - every id used has a corresponding activity
    - no activity is linked to itself as the next or as a choice
    - no activity contains None or Null in the choices
    - there are not duplicate choices
    - there are no activities with the same id
    - the first activity id has a corresponding activity

    This does not check:
    - the knowledge base, its contents and how it is used
    - the callbacks, their existence and behavior

    :raises DescriptionException: if the check is not passed
    :raises KeyError: if an activity's type can not be recognized
    """
    if isinstance(process, Process):
        process.check()
    else:
        Process.from_dict(process)
