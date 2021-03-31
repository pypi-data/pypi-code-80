from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Union

from sym.sdk._internal.sym_error_lookups import SymErrorLookups, register_enum_codes
from sym.sdk.errors import SymSystemError
from sym.sdk.resource import SRN
from sym.sdk.user import User

OrganizationHandle = Union[SRN, str]


@register_enum_codes("SymHandler")
class SymHandlerErrors(Enum):
    HANDLER_NOT_INITIALIZED = "The Sym infrastructure handler has not been initialized.  Please contact Sym Support <support@symops.io>"
    USER_NOT_FOUND = "The user: {user_id} is not registered with Sym"
    ENVIRONMENT_NAME_NOT_FOUND = "The requested environment: {environment_name} could not be found"
    FLOW_NOT_REGISTERED = "The requested flow: {flow_name} could not be found in the requested environment: {environment_name}"
    UNKNOWN_ERROR = "An unknown error has occurred"


class SymHandler(ABC):
    _handler = None

    @classmethod
    def set_handler(cls, handler):
        cls._handler = handler

    @classmethod
    def get_handler(cls):
        if not cls._handler:
            raise SymSystemError(
                SymHandlerErrors.HANDLER_NOT_INITIALIZED,
                "Please contact Sym Support <support@symops.io>",
            )
        return cls._handler

    @abstractmethod
    def get_flows(
        self,
        user_id: str,
        org_handle: Optional[OrganizationHandle],
        environment_name: Optional[str] = None,
        flow_name: Optional[str] = None,
        show_all_environments: bool = False,
    ) -> Dict[str, Dict]:
        pass

    @abstractmethod
    def map_users(
        self, integration_category: str, integration_srn: Optional[str], user_handles: List[str]
    ) -> Dict[str, User]:
        pass
