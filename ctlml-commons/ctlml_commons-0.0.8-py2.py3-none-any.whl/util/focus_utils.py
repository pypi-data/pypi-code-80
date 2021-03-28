from copy import deepcopy
from typing import Dict, Any, Union

from ctlml_commons.entity.focus.percentage_focus import PercentageFocus
from ctlml_commons.entity.focus.price_focus import PriceFocus
from ctlml_commons.entity.price_window import PriceWindow


def str_to_focus(input_blob: Dict[str, Any]) -> Union[PercentageFocus, PriceFocus]:
    data = deepcopy(input_blob)

    focus_type: str = data["focus_type"]

    if focus_type == "PriceFocus":
        return deserialize_price_focus(data)
    elif focus_type == "PercentageFocus":
        return deserialize_percentage_focus(data)

    raise Exception(f"Unknown focus type: {focus_type}")


def focus_to_str(focus: Union[PercentageFocus, PriceFocus]) -> Dict[str, Any]:

    if focus.__class__.__name__ == "PriceFocus":
        return serialize_price_focus(focus)
    elif focus.__class__.__name__ == "PercentageFocus":
        return serialize_percentage_focus(focus)

    raise Exception(f"Unknown focus: {focus.__class__.__name__}")


def serialize_price_focus(focus: PriceFocus) -> Dict[str, Any]:

    data = deepcopy(focus.__dict__)
    data["share_price_window"] = data["share_price_window"].__dict__
    data["focus_type"] = focus.__class__.__name__
    return data


def deserialize_price_focus(input_data: Dict[str, Any]) -> PriceFocus:
    data = deepcopy(input_data)

    del data["focus_type"]
    data["share_price_window"] = PriceWindow.deserialize(data["share_price_window"])

    return PriceFocus(**data)


def serialize_percentage_focus(focus: PercentageFocus) -> Dict[str, Any]:

    data = deepcopy(focus.__dict__)
    data["focus_type"] = focus.__class__.__name__
    return data


def deserialize_percentage_focus(input_data: Dict[str, Any]) -> PercentageFocus:
    data = deepcopy(input_data)

    del data["focus_type"]

    return PercentageFocus(**data)
