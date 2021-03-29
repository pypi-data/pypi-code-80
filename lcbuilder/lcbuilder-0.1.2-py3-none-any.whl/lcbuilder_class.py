import re

from lcbuilder.objectinfo.InputObjectInfo import InputObjectInfo
from lcbuilder.objectinfo.MissionFfiCoordsObjectInfo import MissionFfiCoordsObjectInfo
from lcbuilder.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from lcbuilder.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from lcbuilder.objectinfo.MissionObjectInfo import MissionObjectInfo
from lcbuilder.objectinfo.ObjectInfo import ObjectInfo
from lcbuilder.objectinfo.preparer.MissionFfiLightcurveBuilder import MissionFfiLightcurveBuilder
from lcbuilder.objectinfo.preparer.MissionInputLightcurveBuilder import MissionInputLightcurveBuilder
from lcbuilder.objectinfo.preparer.MissionLightcurveBuilder import MissionLightcurveBuilder



class LcBuilder:
    COORDS_REGEX = "^(-{0,1}[0-9.]+)_(-{0,1}[0-9.]+)$"

    def __init__(self) -> None:
        self.lightcurve_builders = {InputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionInputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionObjectInfo: MissionLightcurveBuilder(),
                                    MissionFfiIdObjectInfo: MissionFfiLightcurveBuilder(),
                                    MissionFfiCoordsObjectInfo: MissionFfiLightcurveBuilder()}

    def build(self, object_info: ObjectInfo, object_dir: str):
        return self.lightcurve_builders[type(object_info)].build(object_info, object_dir)

    def build_object_info(self, mission, id, coords, author, sectors, file, cadence, initial_mask, initial_transit_mask,
                          initial_detrend_period, star_info, aperture):
        if mission is not None and file is None and cadence <= 300:
            MissionObjectInfo(id, sectors, author, cadence, initial_mask, initial_transit_mask, initial_detrend_period,
                              star_info, aperture)
        if mission is not None and file is None and cadence > 300:
            MissionFfiIdObjectInfo(id, sectors, author, cadence, initial_mask, initial_transit_mask,
                                   initial_detrend_period, star_info, aperture)
        elif mission is not None and file is not None:
            MissionInputObjectInfo(id, file, initial_mask, initial_transit_mask, initial_detrend_period, star_info,
                                   aperture)
        elif mission is None and coords is not None and cadence > 300:
            MissionFfiCoordsObjectInfo(coords[0], coords[1], sectors, author, cadence, initial_mask,
                                       initial_transit_mask, initial_detrend_period, star_info, aperture)
        elif mission is None and file is not None:
            InputObjectInfo(file, initial_mask, initial_transit_mask, initial_detrend_period, star_info, aperture)
        else:
            raise ValueError(
                "Invalid target definition with mission=%s, id=%s, coords=%s, sectors=%s, file=%s, cadence=%s")

    def parse_coords(self, target: str):
        coords_parsed = re.search(self.COORDS_REGEX, target)
        coords = [coords_parsed.group(1), coords_parsed.group(2)] if coords_parsed is not None else None
        return coords
