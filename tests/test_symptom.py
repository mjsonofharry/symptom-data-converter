import pytest

from datetime import datetime

from converter.event import Event
from converter.data.symptom import SymptomData


def test_minimal():
    sample = """01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5"""
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes is None
    assert isinstance(data, SymptomData)
    symptoms = data.symptoms
    assert len(symptoms) == 1
    symptom = symptoms[0]
    assert symptom.name == "My Symptom"
    assert symptom.intensity == 5
