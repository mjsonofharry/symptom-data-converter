import dataclasses
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

from data.base import EventData
import helpers


@dataclass(frozen=True)
class Symptom:
    name: str
    intensity: Optional[int] = None
    duration: Optional[timedelta] = None


@dataclass(frozen=True)
class SymptomData(EventData):
    symptoms: List[Symptom]

    @classmethod
    def process(cls, data: List[str]):
        if not data:
            return cls(_data=data, symptoms=[])
        symptoms: List[Symptom] = []
        next_symptom: Optional[Symptom] = Symptom(name=data.pop(0))
        for col in data:
            if col.startswith("Intensity:"):
                intensity = helpers.parse_intensity(col)
                next_symptom = dataclasses.replace(next_symptom, intensity=intensity)
            elif col.startswith("Duration"):
                duration = helpers.parse_duration(col)
                next_symptom = dataclasses.replace(next_symptom, duration=duration)
            else:
                symptoms.append(next_symptom)
                next_symptom = Symptom(name=col)
        return cls(_data=data, symptoms=[*symptoms, next_symptom])
