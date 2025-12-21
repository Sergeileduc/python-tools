import datetime

import pytest

from python_tools_sl.parsing import parse_bool, parse_date, parse_json_safe, slugify


def test_parse_json_safe_valid():
    data = parse_json_safe('{"a":1,"b":2}')
    assert data == {"a": 1, "b": 2}


def test_parse_json_safe_invalid():
    data = parse_json_safe("not a json")
    assert data is None


def test_parse_date_formats():
    assert parse_date("2025-12-17") == datetime.datetime(2025, 12, 17)
    assert parse_date("17/12/2025") == datetime.datetime(2025, 12, 17)
    assert parse_date("20251217") == datetime.datetime(2025, 12, 17)


def test_parse_date_timestamp():
    ts = int(datetime.datetime(2025, 12, 17).timestamp())
    assert parse_date(str(ts)).date() == datetime.date(2025, 12, 17)


def test_parse_date_invalid():
    with pytest.raises(ValueError):
        parse_date("17-12-25")


def test_parse_bool_true_values():
    for val in ["true", "True", "YES", "1", "on"]:
        assert parse_bool(val) is True


def test_parse_bool_false_values():
    for val in ["false", "no", "0", "off", "random"]:
        assert parse_bool(val) is False


def test_slugify_basic():
    assert slugify("Hello World!") == "hello-world"


def test_slugify_strip_dashes():
    assert slugify("  ---Hello--- ") == "hello"
