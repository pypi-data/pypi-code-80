from dataclasses import dataclass
from typing import Optional


@dataclass
class LambdaResponse:
    message: Optional[str] = None
    error: Optional[str] = None
