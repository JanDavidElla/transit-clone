from datetime import datetime, timedelta
from dataclasses import dataclass, field
from prediction import Prediction

@dataclass
class Stop:
    stop_id: str
    operator_id: str
    predictions: list[Prediction] = field(default_factory=list)

    def add_arrival(self, route: str, arrival_time: datetime):
        prediction = next(
            (
                prediction 
                for prediction in self.predictions
                if prediction.route == route
            ),
            None,
        )

        if prediction is None:
            prediction = Prediction(route=route)
            self.predictions.append(prediction)

        prediction.arrival_times.append(arrival_time)
    