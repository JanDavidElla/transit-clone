from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Prediction:
    route: str
    arrival_times: list[datetime] = field(default_factory=list)