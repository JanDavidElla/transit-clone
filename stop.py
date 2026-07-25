from datetime import datetime, timedelta
from dataclasses import dataclass, field
from prediction import Prediction

@dataclass
class Stop:
    stop_id: str
    operator_id: str
    predictions: list[Prediction] = field(default_factory=list)
    