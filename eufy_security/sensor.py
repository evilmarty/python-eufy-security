"""Define a Eufy sensor object."""
import logging
from typing import TYPE_CHECKING

from async_generator import asynccontextmanager

from .errors import EufySecurityP2PError
from .p2p.session import P2PSession
from .p2p.types import CommandType
from .types import DeviceType, ParamType
from .device import Device

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Sensor(Device):
    """Define the sensor object."""

    @staticmethod
    def from_info(api: "API", sensor_info: dict) -> "Sensor":
        sensor_type = DeviceType(sensor_info["device_type"])
        if sensor_type == DeviceType.MOTION_SENSOR:
            klass = MotionSensor
        else:
            klass = Sensor
        return klass(api, sensor_info)


class MotionSensor(Sensor): pass
