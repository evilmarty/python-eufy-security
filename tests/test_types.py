"""Define tests for types."""

import pytest

from eufy_security.types import ParamType


def test_param_type_load_with_json_converter():
    assert ParamType.CHIME_STATE.load("123") == 123


def test_param_type_dump_with_json_converter():
    assert ParamType.CHIME_STATE.dump(123) == "123"


def test_param_type_load_with_bool_converter_for_true():
    assert ParamType.SENSOR_OPEN.load("1") == True


def test_param_type_load_with_bool_converter_for_false():
    assert ParamType.SENSOR_OPEN.load("0") == False


def test_param_type_dump_with_bool_converter_for_true():
    assert ParamType.SENSOR_OPEN.dump(True) == "1"


def test_param_type_dump_with_bool_converter_for_false():
    assert ParamType.SENSOR_OPEN.dump(False) == "0"


def test_param_type_load_with_base64_converter():
    assert ParamType.SNOOZE_MODE.load("eyJhIjogMX0=") == {"a": 1}


def test_param_type_dump_with_base64_converter():
    assert ParamType.SNOOZE_MODE.dump({"a": 1}) == "eyJhIjogMX0="
