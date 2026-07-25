from datetime import datetime
from dataclasses import dataclass

@dataclass
class Prediction:
    route: str
    arrival_times: list[datetime]