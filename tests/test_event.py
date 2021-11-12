import pytest

from datetime import datetime, timedelta

from event import Event
import helpers


def test_bm_to_dicts():
    sample = '''01/01/2021, 09:00, Bowel Movement, Bowel Movement, Intensity: 5, "Notes: Hello world."'''
    event = Event.from_cols(data=helpers.parse_csv_sample(sample))
    event_dicts = event.to_dicts()
    assert len(event_dicts) == 1
    bm_dict = event_dicts[0]
    assert len(bm_dict["event_uuid"]) == 36
    assert (
        bm_dict["timestamp"]
        == datetime(year=2021, month=1, day=1, hour=9, minute=0).isoformat()
    )
    assert bm_dict["notes"] == "Hello world."
    assert bm_dict["intensity"] == 5


def test_symptom_to_dicts():
    sample = '''01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, Duration: 2:00, "Notes: I had a cool test symptom"'''
    event = Event.from_cols(data=helpers.parse_csv_sample(sample))
    event_dicts = event.to_dicts()
    assert len(event_dicts) == 1
    symptom_dict = event_dicts[0]
    assert len(symptom_dict["event_uuid"]) == 36
    assert (
        symptom_dict["timestamp"]
        == datetime(year=2021, month=1, day=1, hour=9, minute=0).isoformat()
    )
    assert symptom_dict["notes"] == "I had a cool test symptom"
    assert symptom_dict["name"] == "My Symptom"
    assert symptom_dict["intensity"] == 5
    assert symptom_dict["duration_seconds"] == timedelta(hours=2).seconds


def test_multiple_symptoms_to_dicts():
    sample = '''01/01/2021, 09:00, Symptom, My Symptom, Intensity: 5, Duration: 2:00, My Other Symptom, Intensity: 3, Duration: 0:10, "Notes: I had a couple of really cool test symptoms"'''
    event = Event.from_cols(data=helpers.parse_csv_sample(sample))
    event_dicts = event.to_dicts()
    assert len(event_dicts) == 2

    first_symptom_dict = [x for x in event_dicts if x["name"] == "My Symptom"][0]
    assert len(first_symptom_dict["event_uuid"]) == 36
    assert (
        first_symptom_dict["timestamp"]
        == datetime(year=2021, month=1, day=1, hour=9, minute=0).isoformat()
    )
    assert first_symptom_dict["notes"] == "I had a couple of really cool test symptoms"
    assert first_symptom_dict["name"] == "My Symptom"
    assert first_symptom_dict["intensity"] == 5
    assert first_symptom_dict["duration_seconds"] == timedelta(hours=2).seconds

    second_symptom_dict = [x for x in event_dicts if x["name"] == "My Other Symptom"][0]
    assert len(second_symptom_dict["event_uuid"]) == 36
    assert (
        second_symptom_dict["timestamp"]
        == datetime(year=2021, month=1, day=1, hour=9, minute=0).isoformat()
    )
    assert second_symptom_dict["notes"] == "I had a couple of really cool test symptoms"
    assert second_symptom_dict["name"] == "My Other Symptom"
    assert second_symptom_dict["intensity"] == 3
    assert second_symptom_dict["duration_seconds"] == timedelta(minutes=10).seconds
