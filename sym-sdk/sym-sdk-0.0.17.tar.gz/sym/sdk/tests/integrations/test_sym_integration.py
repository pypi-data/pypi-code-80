from enum import Enum

import pytest

from sym.sdk._internal.integrations.sym_handler import SymHandler, SymHandlerErrors
from sym.sdk._internal.sym_error_lookups import register_enum_codes
from sym.sdk._internal.utils import wrap_with_typed_error
from sym.sdk.errors import SymSystemError


@register_enum_codes("TestSymHandler")
class TestExceptionHandlerErrors(Enum):
    HANDLER_NOT_INITIALIZED = "The Sym infrastructure handler has not been initialized.  Please contact Sym Support <support@symops.io>"


@wrap_with_typed_error(SymSystemError, SymHandlerErrors)
def function_that_throws(to_throw: str):
    raise RuntimeError(to_throw)


@wrap_with_typed_error(SymSystemError, TestExceptionHandlerErrors)
def function_that_throws_badly(to_throw: str):
    raise RuntimeError(to_throw)


class TestSymIntegrationInterface:
    def test_missing_integration(self):
        with pytest.raises(SymSystemError) as exc_info:
            SymHandler().get_flows("unused_id", "unused_org")

        assert exc_info.value.error_code == SymHandlerErrors.HANDLER_NOT_INITIALIZED
        assert exc_info.value.message == SymHandlerErrors.HANDLER_NOT_INITIALIZED.value

    def test_general_error(self):
        with pytest.raises(SymSystemError) as exc_info:
            function_that_throws("missing")

        assert exc_info.value.error_code == SymHandlerErrors.UNKNOWN_ERROR

    def test_error_mapping_error(self):
        with pytest.raises(RuntimeError) as exc_info:
            function_that_throws_badly("missing")

        assert exc_info.value is not None
