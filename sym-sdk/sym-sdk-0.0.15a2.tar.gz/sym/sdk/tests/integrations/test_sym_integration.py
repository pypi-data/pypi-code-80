import pytest

from sym.sdk._internal.utils import wrap_with_typed_error
from sym.sdk.errors import SymSystemError
from sym.sdk.integrations.sym import SymHandlerErrors, get_flows


@wrap_with_typed_error(SymSystemError, SymHandlerErrors)
def function_that_throws(to_throw: str):
    raise RuntimeError(to_throw)


class TestSymIntegrationInterface:
    def test_missing_integration(self):
        with pytest.raises(SymSystemError) as exc_info:
            get_flows("unused_id", "unused_org")

        assert exc_info.value.error_code == SymHandlerErrors.HANDLER_NOT_INITIALIZED
        assert exc_info.value.message == SymHandlerErrors.HANDLER_NOT_INITIALIZED.value

    def test_general_error(self):
        with pytest.raises(SymSystemError) as exc_info:
            function_that_throws("missing")

        assert exc_info.value.error_code == SymHandlerErrors.UNKNOWN_ERROR
