from dataclasses import dataclass

from event import EventData


@dataclass(frozen=True)
class BowelMovementData(EventData):
    pass
