import pytest

from datetime import datetime

from converter.event import Event
from converter.data.bm import BowelMovementData


def test_bm_minimal():
    sample = """01/01/2021, 09:00, Bowel Movement, Bowel Movement, Intensity: 5"""
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes is None
    assert isinstance(data, BowelMovementData)
    assert data.intensity == 5


def test_bm_with_notes():
    sample = '''01/01/2021, 09:00, Bowel Movement, Bowel Movement, Intensity: 5, "Notes: Hello world."'''
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes == "Hello world."
    assert isinstance(data, BowelMovementData)
    assert data.intensity == 5
