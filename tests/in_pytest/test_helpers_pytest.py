import pytest
from helpers import time_in_minutes, minutes_to_time, format_available_minutes


# Simple unit tests (in pytest).


def test_time_in_minutes():
    assert time_in_minutes('00:00') == 0
    assert time_in_minutes('00:01') == 1
    assert time_in_minutes('01:00') == 60
    assert time_in_minutes('23:59') == 1439


def test_minutes_to_time():
    assert minutes_to_time(0) == '00:00'
    assert minutes_to_time(1) == '00:01'
    assert minutes_to_time(60) == '01:00'
    assert minutes_to_time(1439) == '23:59'


def test_format_available_minutes():
    assert format_available_minutes([0, 1, 2, 60, 61, 120]) == ['00:00 - 00:02', '01:00 - 01:01', '02:00 - 02:00']
    assert format_available_minutes([0]) == ['00:00 - 00:00']


# Parametrized tests (in pytest).


@pytest.mark.parametrize("time_str, minutes", [
    ('00:00', 0),
    ('01:00', 60),
    ('23:59', 1439),
])
def test_time_in_minutes(time_str, minutes):
    assert time_in_minutes(time_str) == minutes


@pytest.mark.parametrize("minutes, time_str", [
    (0, '00:00'),
    (60, '01:00'),
    (1439, '23:59'),
])
def test_minutes_to_time(minutes, time_str):
    assert minutes_to_time(minutes) == time_str


@pytest.mark.parametrize("array,expected", [
    ([0, 1, 2, 60, 61, 62], ['00:00 - 00:02', '01:00 - 01:02']),
    ([0, 1, 2, 4, 5, 6], ['00:00 - 00:02', '00:04 - 00:06']),
])
def test_format_available_minutes(array, expected):
    assert format_available_minutes(array) == expected
