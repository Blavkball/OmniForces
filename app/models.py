from dataclasses import dataclass
from typing import Optional


@dataclass
class AIResponse:
    model: str
    response: str
    thinking: Optional[str] = None
    done: bool = False