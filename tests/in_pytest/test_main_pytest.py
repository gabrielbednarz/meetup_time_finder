import pytest
from main import Time, Colleague, valid_time_format


# Simple unit tests (in pytest).


def test_valid_time_format():
    assert valid_time_format('00:00')
    assert valid_time_format('23:59')
    assert not valid_time_format('24:00')
    assert not valid_time_format('00:60')
    assert not valid_time_format('0000')


def test_time_class():
    time_obj = Time('00:00', '01:00')
    assert time_obj.from_in_minutes == 0
    assert time_obj.to_in_minutes == 60
    assert time_obj.time_in_minutes == [range(0, 61)]


def test_colleague_class():
    Colleague.busy_range_list = []
    colleague = Colleague("John")
    time_obj = Time('00:00', '01:00')
    colleague.append_to_busy_range_list(time_obj)
    assert colleague.name == "John"
    assert Colleague.busy_range_list == [range(0, 61)]


# Parametrized tests (in pytest).


@pytest.mark.parametrize("time_str, expected", [
    ('00:00', True),
    ('23:59', True),
    ('24:00', False),
    ('00:60', False),
    ('0000', False),
])
def test_valid_time_format(time_str, expected):
    assert valid_time_format(time_str) == expected


@pytest.mark.parametrize("busy_from, busy_to, from_in_minutes, to_in_minutes, time_in_minutes", [
    ('00:00', '01:00', 0, 60, [range(0, 61)]),
])
def test_time_class(busy_from, busy_to, from_in_minutes, to_in_minutes, time_in_minutes):
    time_obj = Time(busy_from, busy_to)
    assert time_obj.from_in_minutes == from_in_minutes
    assert time_obj.to_in_minutes == to_in_minutes
    assert time_obj.time_in_minutes == time_in_minutes


@pytest.mark.parametrize("colleague_name, time_obj, busy_range_list", [
    ("John", Time('00:00', '01:00'), [range(0, 61)]),
])
def test_colleague_class(colleague_name, time_obj, busy_range_list):
    Colleague.busy_range_list = []
    colleague = Colleague(colleague_name)
    colleague.append_to_busy_range_list(time_obj)
    assert colleague.name == colleague_name
    assert Colleague.busy_range_list == busy_range_list


# We are repeating ourselves with time_obj data, so we can use a parametrized fixture. We will have data as
# busy_from, busy_to, from_in_minutes, to_in_minutes, time_in_minutes inside data variable.

data = [('00:00', '01:00', 0, 60, [range(0, 61)]),
        ('23:59', '00:00', 1439, 0, [range(1439, 1440), range(0, 1)]),
        ('00:01', '00:00', 1, 0, [range(1, 1440), range(0, 1)])]


@pytest.fixture(params=data)
def time_obj(request):
    busy_from, busy_to, from_in_minutes, to_in_minutes, time_in_minutes = request.param
    return Time(busy_from, busy_to), from_in_minutes, to_in_minutes, time_in_minutes


def test_time_class_again(time_obj):
    time_instance, from_in_minutes, to_in_minutes, time_in_minutes = time_obj
    assert time_instance.from_in_minutes == from_in_minutes
    assert time_instance.to_in_minutes == to_in_minutes
    assert time_instance.time_in_minutes == time_in_minutes
