from dataclasses import dataclass
from typing import List, Optional

from data.base import EventData
import helpers


@dataclass(frozen=True)
class BowelMovementData(EventData):
    intensity: Optional[int]

    @classmethod
    def from_cols(cls, data: List[str]):
        if not data:
            return cls(_data=data, intensity=None)
        _ = data.pop(0)  # Bowel Movement
        intensity = helpers.parse_intensity(data.pop(0)) if data else None
        return cls(_data=data, intensity=intensity)

    def to_dicts(self):
        return [dict(intensity=self.intensity)]
