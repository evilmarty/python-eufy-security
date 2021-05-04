"""Define a Eufy camera object."""
import logging
from typing import TYPE_CHECKING

from .device import Device
from .p2p.session import P2PSession
from .p2p.types import CommandType
from .types import DeviceType, ParamType

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Camera(Device):
    """Define the camera object."""

    @staticmethod
    def from_info(api: "API", camera_info: dict) -> "Camera":
        camera_type = DeviceType(camera_info["device_type"])
        if camera_type == DeviceType.FLOODLIGHT:
            klass = FloodlightCamera
        elif camera_type == DeviceType.DOORBELL:
            klass = DoorbellCamera
        else:
            klass = Camera
        return klass(api, camera_info)

    @property
    def last_camera_image_url(self) -> str:
        """Return the URL to the latest camera thumbnail."""
        return self.device_info["cover_path"]

    @property
    def motion_detection_enabled(self):
        """Return the status of motion detection."""
        return bool(self.params[ParamType.DETECT_SWITCH])

    async def async_start_detection(self):
        """Start camera detection."""
        await self.async_set_params({ParamType.DETECT_SWITCH: 1})

    async def async_start_stream(self) -> str:
        """Start the camera stream and return the RTSP URL."""
        start_resp = await self._api.request(
            "post",
            "web/equipment/start_stream",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "proto": 2,
            },
        )

        return start_resp["data"]["url"]

    async def async_stop_detection(self):
        """Stop camera detection."""
        await self.async_set_params({ParamType.DETECT_SWITCH: 0})

    async def async_stop_stream(self) -> None:
        """Stop the camera stream."""
        await self._api.request(
            "post",
            "web/equipment/stop_stream",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "proto": 2,
            },
        )


class DoorbellCamera(Camera):
    async def enable_osd(self, enable: bool, session: P2PSession = None) -> None:
        async with self.async_establish_session(session) as session:
            await session.async_send_command_with_int_string(
                0, CommandType.CMD_SET_DEVS_OSD, 1 if enable else 0
            )


class FloodlightCamera(Camera):
    async def enable_osd(self, enable: bool, session: P2PSession = None) -> None:
        async with self.async_establish_session(session) as session:
            # 0 - disables the timestamp
            # 1 - enables timestamp but removes logo
            # 2 - enables all OSD items
            await session.async_send_command_with_int_string(
                0, CommandType.CMD_SET_DEVS_OSD, 2 if enable else 1
            )

    async def enable_manual_light(
        self, enable: bool, session: P2PSession = None
    ) -> None:
        async with self.async_establish_session(session) as session:
            await session.async_send_command_with_int_string(
                0, CommandType.CMD_SET_FLOODLIGHT_MANUAL_SWITCH, 1 if enable else 0
            )
