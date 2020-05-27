from dataclasses import dataclass
from datetime import datetime


@dataclass()
class EPGEvent:
    time_start: datetime
    time_end: datetime
    name: str

    def __str__(self):
        return f'{self.time_start.time()} - {self.time_end.time()} {self.name}'

    def get_duration(self):
        # datetime - datetime = timedelta;
        return (self.time_end - self.time_start).seconds / 60
