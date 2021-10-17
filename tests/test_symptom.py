import pytest

from datetime import datetime, timedelta

from event import Event
from data.symptom import SymptomData


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
    assert symptom.duration is None


def test_with_duration():
    sample = """01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, Duration: 2:00"""
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
    assert symptom.duration == timedelta(hours=2, minutes=0)


def test_with_notes():
    sample = '''01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, "Notes: I had a cool test symptom"'''
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes == "I had a cool test symptom"
    assert isinstance(data, SymptomData)
    symptoms = data.symptoms
    assert len(symptoms) == 1
    symptom = symptoms[0]
    assert symptom.name == "My Symptom"
    assert symptom.intensity == 5
    assert symptom.duration is None


def test_with_duration_and_notes():
    sample = '''01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, Duration: 2:00, "Notes: I had a cool test symptom"'''
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes == "I had a cool test symptom"
    assert isinstance(data, SymptomData)
    symptoms = data.symptoms
    assert len(symptoms) == 1
    symptom = symptoms[0]
    assert symptom.name == "My Symptom"
    assert symptom.intensity == 5
    assert symptom.duration == timedelta(hours=2, minutes=0)


def test_multiple_minimal():
    sample = """01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, My Other Symptom, Intensity: 3"""
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes is None
    assert isinstance(data, SymptomData)
    symptoms = data.symptoms
    assert len(symptoms) == 2
    first_symptom = symptoms[0]
    assert first_symptom.name == "My Symptom"
    assert first_symptom.intensity == 5
    assert first_symptom.duration == None
    second_symptom = symptoms[1]
    assert second_symptom.name == "My Other Symptom"
    assert second_symptom.intensity == 3
    assert first_symptom.duration == None


def test_multiple_with_duration():
    sample = """01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, Duration: 2:00, My Other Symptom, Intensity: 3, Duration: 0:10"""
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes is None
    assert isinstance(data, SymptomData)
    symptoms = data.symptoms
    assert len(symptoms) == 2
    first_symptom = symptoms[0]
    assert first_symptom.name == "My Symptom"
    assert first_symptom.intensity == 5
    assert first_symptom.duration == timedelta(hours=2, minutes=0)
    second_symptom = symptoms[1]
    assert second_symptom.name == "My Other Symptom"
    assert second_symptom.intensity == 3
    assert second_symptom.duration == timedelta(hours=0, minutes=10)


def test_multiple_with_notes():
    sample = '''01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, My Other Symptom, Intensity: 3, "Notes: I had a couple of really cool test symptoms"'''
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes == "I had a couple of really cool test symptoms"
    assert isinstance(data, SymptomData)
    symptoms = data.symptoms
    assert len(symptoms) == 2
    first_symptom = symptoms[0]
    assert first_symptom.name == "My Symptom"
    assert first_symptom.intensity == 5
    assert first_symptom.duration == None
    second_symptom = symptoms[1]
    assert second_symptom.name == "My Other Symptom"
    assert second_symptom.intensity == 3
    assert first_symptom.duration == None


def test_multiple_with_duration_and_notes():
    sample = '''01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, Duration: 2:00, My Other Symptom, Intensity: 3, Duration: 0:10, "Notes: I had a couple of really cool test symptoms"'''
    event = Event.parse(data=sample)
    assert event.timestamp == datetime(year=2021, month=1, day=1, hour=9, minute=0)
    data = event.data
    assert data.notes == "I had a couple of really cool test symptoms"
    assert isinstance(data, SymptomData)
    symptoms = data.symptoms
    assert len(symptoms) == 2
    first_symptom = symptoms[0]
    assert first_symptom.name == "My Symptom"
    assert first_symptom.intensity == 5
    assert first_symptom.duration == timedelta(hours=2, minutes=0)
    second_symptom = symptoms[1]
    assert second_symptom.name == "My Other Symptom"
    assert second_symptom.intensity == 3
    assert second_symptom.duration == timedelta(hours=0, minutes=10)
