"""Define tests for device."""

import pytest

from eufy_security.device import Device, DeviceDict


def test_device_update_with_dict():
    device = Device(None, {"device_name": "device1"})
    assert device.name == "device1"
    device.update({"device_name": "device1updated"})
    assert device.name == "device1updated"


def test_device_dict_init():
    dd = DeviceDict(None)
    assert dd.item_class == Device
    assert dd.item_key == "device_sn"


def test_device_dict_update_when_new_items():
    dd = DeviceDict(None)
    assert "1" not in dd
    assert "2" not in dd

    dd.update([{"device_sn": "1", "status": 1}, {"device_sn": "2", "status": 1}])
    assert "1" in dd
    assert "2" in dd


def test_device_dict_update_when_existing_items():
    dd = DeviceDict(None)
    dd.update([{"device_sn": "1", "status": 1}, {"device_sn": "2", "status": 1}])
    assert dd["1"].status == 1
    assert dd["2"].status == 1

    dd.update([{"device_sn": "1", "status": 0,}])
    assert dd["1"].status == 0
    assert dd["2"].status == 1
