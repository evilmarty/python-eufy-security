"""Define tests for device."""

import pytest

from eufy_security.device import Device, DeviceDict

def test_device_dict_init():
    dd = DeviceDict(None)
    assert dd.item_class == Device
    assert dd.item_key == "device_sn"

def test_device_dict_update_when_new_items():
    dd = DeviceDict(None)
    assert "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" not in dd

    dd.update([
        {
            "device_sn": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "params": [],
        }
    ])
    assert "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" in dd
