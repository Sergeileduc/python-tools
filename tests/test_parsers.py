import datetime

import pytest

from python_tools_sl.parsing import is_json_type, parse_bool, parse_date, parse_json_safe, slugify


def test_is_json_type_valid():
    assert is_json_type({"a": 1, "b": [1, 2, {"c": True}]})
    assert is_json_type("hello")
    assert is_json_type(123)
    assert is_json_type(None)
    assert is_json_type({})  # valide → True
    assert is_json_type([1, 2, 3])


def test_is_json_type_invalid():
    assert not is_json_type({1: "a"})  # clé non-str
    assert not is_json_type({"a": object()})  # objet non JSON
    assert not is_json_type(set([1, 2, 3]))  # set non JSON
    assert not is_json_type((1, 2))  # tuple non JSON


def test_parse_json_safe_valid():
    data = parse_json_safe('{"a":1,"b":2}')
    assert data == {"a": 1, "b": 2}


@pytest.mark.parametrize(
    "text, expected",
    [
        ('"hello"', "hello"),
        ("123", 123),
        ("true", True),
        ("false", False),
        ("null", None),
    ],
)
def test_parse_json_safe_primitives(text, expected):
    assert parse_json_safe(text) == expected


def test_parse_json_safe_invalid1():
    data = parse_json_safe('{"a":1,,}')
    assert data is None


def test_parse_json_safe_invalid2():
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
