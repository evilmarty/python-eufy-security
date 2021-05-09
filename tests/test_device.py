"""Define tests for device."""

import pytest

from eufy_security.device import Device, DeviceDict


def test_device_dict_init():
    dd = DeviceDict(None)
    assert dd.item_class == Device
    assert dd.item_key == "device_sn"


def test_device_dict_update_when_new_items():
    dd = DeviceDict(None)
    assert "abc123" not in dd

    dd.update([{"device_sn": "abc123", "params": [],}])
    assert "abc123" in dd


def test_device_dict_update_when_existing_items():
    device = Device(None, {"device_sn": "abc123", "status": 1,})
    dd = DeviceDict(None)
    dd[device.serial] = device
    assert "abc123" in dd

    dd.update([{"device_sn": "abc123", "status": 0,}])
    assert device.status == 0
