from abc import ABC, abstractmethod
from typing import List
from egp.epgchannel import EPGChannel


class EPGParser(ABC):
    epg: List[EPGChannel] = list()

    def get_epg(self, path):
        file = self.open_file(path)
        raw_data = self.extract_data(file)
        self.epg = self.parse_data(raw_data)
        self.print_egp()

    @abstractmethod
    def open_file(self, path: str) -> 'file':
        pass

    @abstractmethod
    def extract_data(self, file):
        pass

    @abstractmethod
    def parse_data(self, raw_data) -> List[EPGChannel]:
        pass

    def print_egp(self):
        for channel in self.epg:
            print(channel)

    def get_average_duration(self):
        return list(map(lambda channel: f'{channel.name} - {channel.get_average_duration()}', self.epg))
