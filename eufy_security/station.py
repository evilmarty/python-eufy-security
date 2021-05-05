"""Define a Eufy station object."""
import logging
from typing import TYPE_CHECKING

from async_generator import asynccontextmanager

from .device import Device
from .errors import EufySecurityP2PError
from .p2p.session import P2PSession
from .p2p.types import CommandType
from .types import GuardMode, ParamType

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

    @property
    def guard_mode(self):
        """Return the station's guard mode."""
        try:
            return GuardMode(self.params[ParamType.GUARD_MODE])
        except ValueError:
            return None

    @property
    def away_mode(self):
        """Return whether the station is in away mode."""
        return self.guard_mode == GuardMode.AWAY

    @property
    def home_mode(self):
        """Return whether the station is in home mode."""
        return self.guard_mode == GuardMode.HOME

    @property
    def disarmed_mode(self):
        """Return whether the station is in disarmed mode."""
        return self.guard_mode == GuardMode.DISARMED

    @property
    def schedule_mode(self):
        """Return whether the station is in schedule mode."""
        return self.guard_mode == GuardMode.SCHEDULE

    @property
    def geofencing_mode(self):
        """Return whether the station is in geofencing mode."""
        return self.guard_mode == GuardMode.GEOFENCING

    async def set_guard_mode(self, mode: GuardMode, session: P2PSession = None) -> None:
        """Set station guard mode."""
        async with self.async_establish_session(session) as session:
            await session.async_send_command_with_int(
                0, CommandType.CMD_SET_ARMING, mode.value
            )

    async def set_away_mode(self, session: P2PSession = None) -> None:
        """Set station guard mode to away."""
        await self.set_guard_mode(GuardMode.AWAY, session)

    async def set_home_mode(self, session: P2PSession = None) -> None:
        """Set station guard mode to home."""
        await self.set_guard_mode(GuardMode.HOME, session)

    async def set_disarmed_mode(self, session: P2PSession = None) -> None:
        """Set station guard mode to disarmed."""
        await self.set_guard_mode(GuardMode.DISARMED, session)

    async def set_schedule_mode(self, session: P2PSession = None) -> None:
        """set station guard mode to schedule."""
        await self.set_guard_mode(GuardMode.SCHEDULE, session)

    async def set_geofencing_mode(self, session: P2PSession = None) -> None:
        """set station guard mode to geofencing."""
        await self.set_guard_mode(GuardMode.GEOFENCING, session)
