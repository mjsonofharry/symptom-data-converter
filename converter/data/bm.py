from dataclasses import dataclass

from data.base import EventData


@dataclass(frozen=True)
class BowelMovementData(EventData):
    pass
