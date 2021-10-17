from dataclasses import dataclass

from data import EventData


@dataclass(frozen=True)
class BowelMovementData(EventData):
    pass
