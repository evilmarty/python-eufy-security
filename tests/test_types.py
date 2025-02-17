"""Define tests for types."""

from datetime import datetime, timezone
import json

import pytest

from eufy_security.types import ParamDict, ParamType

from .common import load_fixture


def test_param_type_lookup_by_instance():
    assert ParamType.lookup(ParamType.CHIME_STATE) == ParamType.CHIME_STATE


def test_param_type_lookup_by_name():
    assert ParamType.lookup("CHIME_STATE") == ParamType.CHIME_STATE


def test_param_type_lookup_by_value():
    assert ParamType.lookup(2015) == ParamType.CHIME_STATE


def test_param_type_load_with_string_converter():
    assert ParamType.HUB_LAN_IP.load("foobar") == "foobar"


def test_param_type_dump_with_string_converter():
    assert ParamType.HUB_LAN_IP.dump(123) == "123"


def test_param_type_load_with_json_converter():
    assert ParamType.CHIME_STATE.load("123") == 123


def test_param_type_dump_with_json_converter():
    assert ParamType.CHIME_STATE.dump(123) == "123"


def test_param_type_load_with_bool_converter_for_true():
    assert ParamType.SENSOR_STATUS.load("1") == True


def test_param_type_load_with_bool_converter_for_false():
    assert ParamType.SENSOR_STATUS.load("0") == False


def test_param_type_dump_with_bool_converter_for_true():
    assert ParamType.SENSOR_STATUS.dump(True) == "1"


def test_param_type_dump_with_bool_converter_for_false():
    assert ParamType.SENSOR_STATUS.dump(False) == "0"


def test_param_type_load_with_base64_converter():
    assert ParamType.SNOOZE_MODE.load("eyJhIjogMX0=") == {"a": 1}


def test_param_type_dump_with_base64_converter():
    assert ParamType.SNOOZE_MODE.dump({"a": 1}) == "eyJhIjogMX0="


def test_param_type_load_with_datetime_converter():
    dt = datetime(2021, 5, 10, 21, 42, 5, tzinfo=timezone.utc)
    assert ParamType.SENSOR_CHANGE_TIME.load("1620682925") == dt


def test_param_type_dump_with_datetime_converter():
    dt = datetime(2021, 5, 10, 21, 42, 5, tzinfo=timezone.utc)
    assert ParamType.SENSOR_CHANGE_TIME.dump(dt) == "1620682925"


def test_param_dict_initializes():
    data = json.loads(load_fixture("devices_list_response.json"))["data"][0]["params"]
    params = ParamDict(data)
    assert len(params) == 25


def test_param_dict_getitem_by_param_type():
    data = json.loads(load_fixture("devices_list_response.json"))["data"][0]["params"]
    params = ParamDict(data)
    assert params[ParamType.DETECT_SWITCH] == True


def test_param_dict_getitem_by_str():
    data = json.loads(load_fixture("devices_list_response.json"))["data"][0]["params"]
    params = ParamDict(data)
    assert params["DETECT_SWITCH"] == True


def test_param_dict_getitem_by_int():
    data = json.loads(load_fixture("devices_list_response.json"))["data"][0]["params"]
    params = ParamDict(data)
    assert params[2027] == True


def test_param_dict_update():
    data = json.loads(load_fixture("devices_list_response.json"))["data"][0]["params"]
    params = ParamDict(data)
    assert params[ParamType.DETECT_SWITCH] == True

    params.update(
        [
            {
                "param_id": 0,
                "device_sn": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "param_type": 2027,
                "param_value": "0",
                "create_time": 1572460903,
                "update_time": 0,
                "status": 1,
            }
        ]
    )
    assert params[ParamType.DETECT_SWITCH] == False
