import csv
from datetime import datetime, timedelta
from typing import Iterable, List, Optional


def get_csv_reader(csvfile: Iterable[str]):
    return csv.reader(
        csvfile,
        quotechar='"',
        delimiter=",",
        quoting=csv.QUOTE_ALL,
        skipinitialspace=True,
    )


def parse_csv_sample(csv_sample: str) -> List[str]:
    reader = get_csv_reader(csvfile=[csv_sample])
    return [row for row in reader][0]


DATE_FORMAT = "%m/%d/%Y"
TIME_FORMAT = "%H:%M"


def parse_timestamp(date_string: str, time_string: str):
    return datetime.strptime(
        f"{date_string}T{time_string}", f"{DATE_FORMAT}T{TIME_FORMAT}"
    )


def parse_intensity(intensity_str: str) -> int:
    _, intensity_value = intensity_str.split("Intensity:", 1)
    return int(intensity_value.strip())


def parse_duration(duration_str: str):
    _, duration_value = duration_str.split("Duration:", 1)
    hours, minutes = duration_value.strip().split(":")
    return timedelta(hours=int(hours), minutes=int(minutes))
