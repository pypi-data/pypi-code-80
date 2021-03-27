"""
callooktools
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
from datetime import datetime

from gridtools import LatLong, Grid


URL = "https://callook.info/{callsign}/json"


class CallookError(Exception):
    """The exception raised when something goes wrong in callooktools"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


@dataclass
class Address:
    """Represents an address in a :class:`CallookCallsignData` object"""
    #: Attention address line, this line should be prepended to the address
    attn: str = ""
    #: address line 1 (i.e. house # and street)
    line1: str = ""
    #: address line 2 (i.e. city name, state ZIP code)
    line2: str = ""


class LicenseType(enum.Enum):
    """Describes what kind of license the license holder has"""
    CLUB = "Club"
    MILITARY = "Military"
    RACES = "RACES"
    RECREATION = "Military Recration"
    PERSON = "Individual"
    NONE = "None"


class EntryStatus(enum.Enum):
    """Callsign license status"""
    VALID = "Valid"
    INVALID = "Invalid"
    UPDATING = "Updating"
    UNKNOWN = "Unknown"


class LicenseClass(enum.Enum):
    """Describes the class of a license"""
    NOVICE = "Novice"
    TECHNICIAN = "Technician"
    TECHNICIAN_PLUS = "Technician Plus"
    GENERAL = "General"
    ADVANCED = "Advanced"
    EXTRA = "Amateur Extra"
    NONE = "None"


@dataclass
class CallookCallsignData:
    """A callook callsign query result."""
    #: Callsign
    call: str
    #: License class
    lic_class: LicenseClass = LicenseClass.NONE
    #: License status
    status: EntryStatus = EntryStatus.UNKNOWN
    #: License type
    type: LicenseType = LicenseType.NONE
    #: Previous callsign
    prev_call: str = ""
    #: Previous callsign class
    prev_class: LicenseClass = LicenseClass.NONE
    #: Trustee callsign
    trustee_call: str = ""
    #: Trustee name
    trustee_name: str = ""
    #: License name
    name: str = ""
    #: Operator mailing address
    address: Address = Address()
    #: approximate lat/long of address
    latlong: LatLong = LatLong(0, 0)
    #: grid locator of address
    grid: Grid = Grid(LatLong(0, 0))
    #: FCC ULS url
    uls_url: str = ""
    #: FRN
    frn: str = ""
    #: callsign last modified date
    mod_date: datetime = datetime.min
    #: callsign grant date
    grant_date: datetime = datetime.min
    #: callsign expiry date
    expire_date: datetime = datetime.min


class CallookAbc(ABC):
    """The base class for CallookSync and CallookAsync. **This should not be used directly.**"""
    def __init__(self):
        pass

    @property
    @abstractmethod
    def session(self):
        pass

    @session.setter
    @abstractmethod
    def session(self, val) -> None:
        pass

    @abstractmethod
    def get_callsign(self, callsign: str) -> CallookCallsignData:
        """Gets QRZ data for a callsign.

        :param callsign: the callsign to search for
        :type callsign: str
        :return: the QRZ data for the callsign
        :rtype: CallookCallsignData
        """
        pass

    @abstractmethod
    def _do_query(self, query: str) -> Dict:
        pass

    def _process_callsign(self, data: Dict) -> CallookCallsignData:
        # check for errors
        if data.get("status", "") == "INVALID":
            return CallookCallsignData(call="", status=EntryStatus.INVALID)
        elif data.get("status", "") == "UPDATING":
            return CallookCallsignData(call="", status=EntryStatus.UPDATING)

        current = data.get("current", {})
        previous = data.get("previous", {})
        trustee = data.get("trustee", {})
        address = data.get("address", {})
        location = data.get("location", {})
        other_info = data.get("otherInfo", {})

        calldata = CallookCallsignData(call=current.get("callsign", "").upper())
        lic_class = current.get("operClass", LicenseClass.NONE)
        if lic_class == "NOVICE":
            calldata.lic_class = LicenseClass.NOVICE
        elif lic_class == "TECHNICIAN":
            calldata.lic_class = LicenseClass.TECHNICIAN
        elif lic_class == "TECHNICIAN PLUS":
            calldata.lic_class = LicenseClass.TECHNICIAN_PLUS
        elif lic_class == "GENERAL":
            calldata.lic_class = LicenseClass.GENERAL
        elif lic_class == "ADVANCED":
            calldata.lic_class = LicenseClass.ADVANCED
        elif lic_class == "EXTRA":
            calldata.lic_class = LicenseClass.EXTRA
        else:
            calldata.lic_class = LicenseClass.NONE

        calldata.status = EntryStatus.VALID

        lic_type = data.get("type", LicenseType.NONE)
        if lic_type == "CLUB":
            calldata.type = LicenseType.CLUB
        elif lic_type == "MILITARY":
            calldata.type = LicenseType.MILITARY
        elif lic_type == "RACES":
            calldata.type = LicenseType.RACES
        elif lic_type == "RECREATION":
            calldata.type = LicenseType.RECREATION
        elif lic_type == "PERSON":
            calldata.type = LicenseType.PERSON

        calldata.prev_call = previous.get("callsign", "").upper()

        prev_class = previous.get("operClass", LicenseClass.NONE)
        if prev_class == "NOVICE":
            calldata.prev_class = LicenseClass.NOVICE
        elif prev_class == "TECHNICIAN":
            calldata.prev_class = LicenseClass.TECHNICIAN
        elif prev_class == "TECHNICIAN PLUS":
            calldata.prev_class = LicenseClass.TECHNICIAN_PLUS
        elif prev_class == "GENERAL":
            calldata.prev_class = LicenseClass.GENERAL
        elif prev_class == "ADVANCED":
            calldata.prev_class = LicenseClass.ADVANCED
        elif prev_class == "EXTRA":
            calldata.prev_class = LicenseClass.EXTRA
        else:
            calldata.prev_class = LicenseClass.NONE

        calldata.trustee_call = trustee.get("callsign", "").upper()
        calldata.trustee_name = trustee.get("name", "").title()

        calldata.name = data.get("name", "").title()
        calldata.address = Address(
            attn=address.get("attn", ""),
            line1=address.get("line1", ""),
            line2=address.get("line2", "")
        )

        calldata.latlong = LatLong(float(location.get("latitude", 0)), float(location.get("longitude", 0)))
        calldata.grid = Grid(location.get("gridsquare", LatLong(0, 0)))

        calldata.uls_url = other_info.get("ulsUrl", "")
        calldata.frn = other_info.get("frn", "")

        ladate = other_info.get("grantDate", datetime.min)
        try:
            calldata.mod_date = datetime.strptime(ladate, "%m/%d/%Y") if not isinstance(ladate, datetime) else ladate
        except ValueError:
            calldata.mod_date = datetime.min

        efdate = other_info.get("grantDate", datetime.min)
        try:
            calldata.grant_date = datetime.strptime(efdate, "%m/%d/%Y") if not isinstance(efdate, datetime) else efdate
        except ValueError:
            calldata.grant_date = datetime.min

        exdate = other_info.get("expiryDate", datetime.min)
        try:
            calldata.expire_date = datetime.strptime(exdate, "%m/%d/%Y") if not isinstance(exdate, datetime) else exdate
        except ValueError:
            calldata.expire_date = datetime.min

        return calldata
