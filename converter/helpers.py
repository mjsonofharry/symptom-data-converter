from datetime import datetime, timedelta

from parsec import *


def delimiter():
    """Parse the delimiter character."""
    return string(",") << spaces()


def not_delimiter():
    return regex(r"[^,]+")


def until_delimiter():
    """Parse text until the delimiter character."""
    return not_delimiter() << delimiter()


def end_of_string():
    """Parse the end of a string."""
    return regex(r"$")


def end_of_line():
    """Parse the end of a line."""
    return regex(r"[\n]")


def until_end_of_line():
    """Parse text the end of a line."""
    return regex(r"[^\n]+")


def number(digits: int):
    """Parse a positive integer with a fixed length."""
    return count(digit(), digits).parsecmap(lambda characters: int("".join(characters)))


def quoted():
    """Parse text between double-quotes."""
    return string('"') >> regex(r'[^\\"]+') << string('"')


def bracketed():
    """Parse text between square brackets."""
    return string("[") >> regex(r"[^\]]+") << string("]")


def event_notes():
    """Parse notes."""
    return string('"Notes:') >> spaces() >> regex(r'[^\\"]+') << string('"')


def delimited_sequence(p: Parser):
    """Parse a sequence of delimited parsers until the end of the string."""
    return many1(p << (delimiter() ^ end_of_string()))


def date_and_time():
    """Parse a date and time in the format of "MM/DD/YYYY, HH:MM"."""
    @generate
    def p():
        month = yield number(2) << string("/")
        day = yield number(2) << string("/")
        year = yield number(4) << delimiter()
        hour = yield number(2) << string(":")
        minute = yield number(2) << delimiter()
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    return p


def duration():
    """Parse a duration in the format of "HH:MM"."""
    @generate
    def p():
        hours = yield number(2) << string(":")
        minutes = yield number(2)
        return timedelta(hours=hours, minutes=minutes)

    return p




