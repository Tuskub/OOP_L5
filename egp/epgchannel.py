from dataclasses import dataclass
from typing import List

from egp.epgevent import EPGEvent


@dataclass()
class EPGChannel:
    name: str
    programme: List[EPGEvent]

    def __str__(self):
        # chr(10) == '\n' какой ужас
        return f'{self.name}\n' \
               f'{chr(10).join(list(map(str, self.programme)))}'

    def get_average_duration(self):
        return sum(map(lambda event: event.get_duration(), self.programme)) / len(self.programme)
