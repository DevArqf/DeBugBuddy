from dataclasses import dataclass
from typing import Optional

@dataclass
class Prediction:
    file: str
    line: int
    column: Optional[int]
    error_type: str
    message: str
    confidence: float  # 0.0 to 1.0
    suggestion: str
    severity: str  # 'low', 'medium', 'high', 'critical'