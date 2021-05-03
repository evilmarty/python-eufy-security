"""Define a Eufy station object."""
import logging
from typing import TYPE_CHECKING

from async_generator import asynccontextmanager

from .device import Device
from .errors import EufySecurityP2PError
from .p2p.session import P2PSession
from .p2p.types import CommandType
from .types import GuardMode

if TYPE_CHECKING:
    from .api import API  # pylint: disable=cyclic-import

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Station(Device):
    """Define a station object (e.g. Homebase)."""

    @staticmethod
    def from_info(api: "API", station_info: dict) -> "Station":
        return Station(api, station_info)

    @asynccontextmanager
    async def async_establish_session(self, session: P2PSession = None):
        if session and session.valid_for(self.serial):
            yield session
            return

        async with self.connect() as session:
            yield session
            return

    @asynccontextmanager
    async def connect(self, addr: str = None):
        dsk_key_resp = await self._api.request(
            "post", "app/equipment/get_dsk_keys", json={"station_sns": [self.serial]}
        )
        for item in dsk_key_resp.get("data")["dsk_keys"]:
            if item["station_sn"] == self.serial:
                p2p_session = P2PSession(
                    self.serial,
                    self.device_info["p2p_did"],
                    item["dsk_key"],
                    self.device_info["member"]["action_user_id"],
                )
                is_connected = await p2p_session.connect(addr)
                if is_connected:
                    try:
                        yield p2p_session
                    finally:
                        await p2p_session.close()
                    return
                else:
                    raise EufySecurityP2PError(f"Could not connect to {self.name}")
        else:
            raise EufySecurityP2PError(f"Could not find discovery key for {self.name}")

    @property
    def model(self) -> str:
        """Return the station's model."""
        return self.device_info["station_model"]

    @property
    def name(self) -> str:
        """Return the station name."""
        return self.device_info["station_name"]

    @property
    def serial(self) -> str:
        """Return the station serial number."""
        return self.device_info["station_sn"]

    @property
    def ip(self) -> str:
        """Return the station's ip."""
        return self.device_info["ip_addr"]

    async def set_guard_mode(self, mode: GuardMode, session: P2PSession = None) -> None:
        async with self.async_establish_session(session) as session:
            await session.async_send_command_with_int(
                0, CommandType.CMD_SET_ARMING, mode.value
            )
