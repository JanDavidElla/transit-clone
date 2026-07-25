from datetime import datetime, timedelta
class Stop:
    def __init__(self, origin, dictionary):
        self.origin = origin
        self.dictionary = dictionary

    def addTimestamp(self, origin, timestamp):
        self.dictionary[origin] = timestamp

    def printList(self):
        for stop, timestamp in self.dictionary.items():
            print(stop, timestamp)

#lets do origin, time dictionaries

from dataclasses import dataclass

@dataclass
class Stop:
    origin: str
    dictionary: dict

    def add_timestamp(self, origin: str, timestamp: datetime):
        self.dictionary[origin] = timestamp

    def print_list(self):
        for stop, timestamp in self.dictionary.items():
            print(stop, timestamp)