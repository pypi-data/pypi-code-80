from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional, Type

from sym.sdk._internal.sym_error_lookups import register_enum_codes
from sym.sdk.errors import SymSystemError


@register_enum_codes("SymHandler")
class SymHandlerErrors(Enum):
    HANDLER_NOT_INITIALIZED = "The Sym infrastructure handler has not been initialized.  Please contact Sym Support <support@symops.io>"
    USER_NOT_FOUND = "The user: {user_id} is not registered with Sym"
    ENVIRONMENT_NAME_NOT_FOUND = "The requested environment: {environment_name} could not be found"
    FLOW_NOT_REGISTERED = "The requested flow: {flow_name} could not be found in the requested environment: {environment_name}"
    UNKNOWN_ERROR = "An unknown error has occurred"


class IntegrationType(Enum):
    UNSET = "unset"
    PAGERDUTY = "pagerduty"
    SYM = "sym"


class IntegrationHandler(ABC):
    integration_type = IntegrationType.UNSET

    api_key_location = None
    pagerduty_handler = None

    @classmethod
    def register_handler(cls, handler: Type["IntegrationHandler"]) -> None:
        setattr(cls, f"{handler.integration_type.value}_handler", handler)

    @classmethod
    def deregister_handler(cls, integration_type: IntegrationType) -> None:
        setattr(cls, f"{integration_type.value}_handler", None)

    @classmethod
    def get_handler(cls, integration_type: IntegrationType) -> "IntegrationHandler":
        handler = getattr(cls, f"{integration_type.value}_handler", None)
        if not handler:
            raise SymSystemError(
                SymHandlerErrors.HANDLER_NOT_INITIALIZED,
                "Please contact Sym Support <support@symops.io>",
            )
        return handler()

    @classmethod
    def set_api_key_location(cls, location: str) -> None:
        cls.api_key_location = location

    @classmethod
    def set_runtime_context(cls, context) -> None:
        cls.context = context

    @staticmethod
    def get_required_key_value(key: str, lookups: dict):
        val = lookups.get(key)
        if not val:
            raise KeyError(f"Must provide a non-trivial {key} value for handler")
        return val

    @abstractmethod
    def execute(self, method_name: str, parameter_lookups: Optional[Dict[str, Any]] = None):
        raise NotImplementedError
