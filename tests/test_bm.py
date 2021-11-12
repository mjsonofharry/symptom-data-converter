import pytest

from datetime import datetime

from event import Event
from data.bm import BowelMovementData
import helpers


def test_bm_minimal():
    sample = """01/01/2021, 09:00, Bowel Movement, Bowel Movement"""
    event = Event.process(data=helpers.parse_csv_sample(sample))
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert event.notes is None
    assert data is not None
    assert isinstance(data, BowelMovementData)
    assert data.intensity is None


def test_bm_with_intensity():
    sample = """01/01/2021, 09:00, Bowel Movement, Bowel Movement, Intensity: 5"""
    event = Event.process(data=helpers.parse_csv_sample(sample))
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert event.notes is None
    assert data is not None
    assert isinstance(data, BowelMovementData)
    assert data.intensity == 5


def test_bm_with_notes():
    sample = '''01/01/2021, 09:00, Bowel Movement, Bowel Movement, Intensity: 5, "Notes: Hello world."'''
    event = Event.process(data=helpers.parse_csv_sample(sample))
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    assert event.notes == "Hello world."
    data = event.data
    assert data is not None
    assert isinstance(data, BowelMovementData)
    assert data.intensity == 5
