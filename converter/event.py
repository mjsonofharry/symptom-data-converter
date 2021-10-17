from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Type

from converter.data.base import EventData
from converter.data.symptom import SymptomData
from converter.data.bm import BowelMovementData

from parsec import *
from converter.helpers import *


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    kind: str
    data: EventData

    @staticmethod
    def kind_to_subclass(kind: str) -> Optional[Type["EventData"]]:
        return {
            "Symptom": SymptomData,
            "Bowel Movement": BowelMovementData,
        }.get(kind)

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            timestamp = yield date_and_time()
            kind = yield until_delimiter()
            event_data = yield until_end_of_line()
            event_data_cls = Event.kind_to_subclass(kind)
            if not event_data_cls:
                return None
            data = event_data_cls.parse(data=event_data)
            return cls(timestamp=timestamp, kind=kind, data=data)

        return p

    @classmethod
    def parse(cls, data: str) -> Optional["Event"]:
        return cls.Parser().parse(text=data)
