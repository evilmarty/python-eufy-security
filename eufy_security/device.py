import logging
from typing import TYPE_CHECKING

from async_generator import asynccontextmanager

from .errors import EufySecurityP2PError
from .p2p.session import P2PSession
from .types import DeviceType, ParamDict, ParamType

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Device:
    def __init__(self, api: "API", device_info: dict) -> None:
        self._api = api
        self.device_info = device_info

    @property
    def device_type(self) -> str:
        """Return the device type."""
        return DeviceType(self.device_info["device_type"])

    @property
    def status(self) -> str:
        """Return the device status."""
        return self.device_info["status"]

    @property
    def hardware_version(self) -> str:
        """Return the hardware version."""
        return self.device_info["main_hw_version"]

    @property
    def mac(self) -> str:
        """Return the MAC address."""
        return self.device_info["wifi_mac"]

    @property
    def model(self) -> str:
        """Return the device model."""
        return self.device_info["device_model"]

    @property
    def name(self) -> str:
        """Return the name."""
        return self.device_info["device_name"]

    @property
    def serial(self) -> str:
        """Return the device serial number."""
        return self.device_info["device_sn"]

    @property
    def software_version(self) -> str:
        """Return the station's software version."""
        return self.device_info["main_sw_version"]

    @property
    def station_serial(self) -> str:
        """Return the device's station serial number."""
        return self.device_info["station_sn"]

    @property
    def last_camera_image_url(self) -> str:
        """Return the URL to the latest camera thumbnail."""
        return self.device_info["cover_path"]

    @property
    def params(self) -> dict:
        """Return device parameters."""
        return ParamDict(self.device_info["params"])

    async def async_start_stream(self) -> str:
        """Start the camera stream and return the RTSP URL."""
        return await self._api.async_start_stream(self)

    async def async_stop_stream(self) -> None:
        """Stop the camera stream."""
        await self._api.async_stop_stream(self)

    async def async_update_param(self, param_type: any, value: any) -> None:
        await self.async_update_params({param_type: value})

    async def async_update_params(self, params: dict) -> None:
        """Set device parameters."""
        serialized_params = []
        for param_type, value in params.items():
            param_type = ParamType.lookup(param_type)
            value = param_type.dump(value)
            serialized_params.append(
                {"param_type": param_type.value, "param_value": value}
            )

        await self._api.async_device_update_params(self, serialized_params)

    async def async_update(self) -> None:
        """Get the latest values for the camera's properties."""
        await self._api.async_update_device_info()

    def update(self, device_info):
        """Update the device's device_info."""
        self.device_info = device_info

    @asynccontextmanager
    async def async_establish_session(self, session: P2PSession = None):
        if session and session.valid_for(self.station_serial):
            yield session
            return

        if self.station_serial in self._api.stations:
            async with self._api.stations[self.station_serial].connect() as session:
                yield session
                return
        else:
            raise EufySecurityP2PError(f"Could not find station for {self.name}")
