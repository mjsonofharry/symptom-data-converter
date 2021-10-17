from dataclasses import dataclass

from converter.data.base import EventData

from parsec import *
from converter.helpers import *


@dataclass(frozen=True)
class BowelMovementData(EventData):
    intensity: int

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            _ = yield string("Bowel Movement") << delimiter()
            intensity = yield key_value("Intensity", number()) << maybe_more()
            notes = yield optional(event_notes())
            return cls(intensity=intensity, notes=notes)

        return p

    @classmethod
    def parse(cls, data: str) -> "BowelMovementData":
        return cls.Parser().parse(text=data)
