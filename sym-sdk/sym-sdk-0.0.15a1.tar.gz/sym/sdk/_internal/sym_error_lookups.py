from typing import Optional


class SymErrorLookups:
    base_doc_url = "https://docs.symops.com/docs/support"
    code_lookups = {}

    @classmethod
    def register_code(cls, error_code: str, message: str):
        cls.code_lookups[error_code] = message

    @classmethod
    def format_message(cls, error_code: str, params: Optional[dict]):
        base_message = cls.code_lookups.get(error_code)
        if base_message:
            return base_message.format_map(params) if params else base_message
        else:
            return f"Error Code: {error_code}"


class register_enum_codes:
    """Decorator to be applied to an enumeration of error codes within which the values are format strings"""

    def __init__(self, target_type):
        self.target_type = target_type

    def __call__(self, cls):
        for error_code in cls:
            SymErrorLookups.register_code(error_code, error_code.value)

        return cls
