import logging
from typing import TYPE_CHECKING

from async_generator import asynccontextmanager

from .errors import EufySecurityP2PError
from .p2p.session import P2PSession
from .types import DeviceType, ParamType

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
    def params(self) -> dict:
        """Return device parameters."""
        params = {}
        for param in self.device_info["params"]:
            param_type = param["param_type"]
            value = param["param_value"]
            try:
                param_type = ParamType(param_type)
                params[param_type] = param_type.read_value(value)
            except ValueError:
                _LOGGER.debug(
                    'Unable to process parameter "%s", value "%s"', param_type, value
                )
        return params

    @property
    def battery_level(self) -> int:
        """Return the device's battery level."""
        return self.params.get(ParamType.BATTERY_LEVEL, None)

    async def async_set_params(self, params: dict) -> None:
        """Set device parameters."""
        serialized_params = []
        for param_type, value in params.items():
            if isinstance(param_type, ParamType):
                value = param_type.write_value(value)
                param_type = param_type.value
            serialized_params.append({"param_type": param_type, "param_value": value})
        await self._api.request(
            "post",
            "app/upload_devs_params",
            json={
                "device_sn": self.serial,
                "station_sn": self.station_serial,
                "params": serialized_params,
            },
        )
        await self.async_update()

    async def async_update(self) -> None:
        """Get the latest values for the camera's properties."""
        await self._api.async_update_device_info()

    def update(self, device_info):
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
