"""Define parameters that can be sent to the base station."""
import base64
from enum import Enum
import json
import logging

_LOGGER: logging.Logger = logging.getLogger(__name__)


class DeviceType(Enum):
    """
    List retrieved from com.oceanwing.battery.cam.binder.model.QueryDeviceData
    """

    BATTERY_DOORBELL = 7
    CAMERA = 1
    CAMERA2 = 9
    CAMERA2C = 8
    CAMERA_E = 4
    DOORBELL = 5
    FLOODLIGHT = 3
    INDOOR_CAMERA = 30
    INDOOR_PT_CAMERA = 31
    KEYPAD = 11
    LOCK_ADVANCED = 51
    LOCK_BASIC = 50
    LOCK_SIMPLE = 52
    MOTION_SENSOR = 10
    SENSOR = 2
    STATION = 0

    @property
    def is_doorbell(self):
        return self in [
            DeviceType.BATTERY_DOORBELL,
            DeviceType.DOORBELL,
        ]

    @property
    def is_camera(self):
        return self in [
            DeviceType.BATTERY_DOORBELL,
            DeviceType.DOORBELL,
            DeviceType.CAMERA,
            DeviceType.CAMERA2,
            DeviceType.CAMERA2C,
            DeviceType.CAMERA_E,
            DeviceType.FLOODLIGHT,
            DeviceType.INDOOR_CAMERA,
            DeviceType.INDOOR_PT_CAMERA,
        ]

    @property
    def is_station(self):
        return self in [DeviceType.DOORBELL, DeviceType.FLOODLIGHT, DeviceType.STATION]

    @property
    def is_sensor(self):
        return self in [DeviceType.MOTION_SENSOR, DeviceType.SENSOR]


class StringConverter:
    """
    Converts values to and from String.
    """

    @staticmethod
    def load(value):
        return str(value)

    @staticmethod
    def dump(value):
        return str(value)


class JsonConverter:
    """
    Converts values to and from JSON.
    """

    @staticmethod
    def load(value):
        return json.loads(value)

    @staticmethod
    def dump(value):
        return json.dumps(value)


class BoolConverter:
    """
    Converts boolean-like values.
    """

    @staticmethod
    def load(value):
        return bool(JsonConverter.load(value))

    @staticmethod
    def dump(value):
        return JsonConverter.dump(int(value))


class Base64Converter:
    """
    Wraps and unwraps base64 values then converts to and from JSON.
    """

    @staticmethod
    def load(value):
        decoded_value = base64.b64decode(value, validate=True).decode()
        return JsonConverter.load(decoded_value)

    @staticmethod
    def dump(value):
        encoded_value = JsonConverter.dump(value)
        return base64.b64encode(encoded_value.encode()).decode()


class ParamType(Enum):
    """
    List retrieved from com.oceanwing.battery.cam.binder.model.CameraParams
    """

    @staticmethod
    def lookup(name_or_value):
        if isinstance(name_or_value, ParamType):
            return name_or_value
        if type(name_or_value) == str:
            return ParamType[name_or_value]
        else:
            return ParamType(name_or_value)

    def __new__(cls, value, converter=JsonConverter):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._converter_ = converter
        return obj

    def load(self, value):
        """Deserialize the value for the parameter."""
        return self._converter_.load(value)

    def dump(self, value):
        """Serialize the value for the parameter."""
        return self._converter_.dump(value)

    CHIME_STATE = 2015
    DETECT_EXPOSURE = 2023
    DETECT_MODE = 2004
    DETECT_MOTION_SENSITIVE = 2005
    DETECT_SCENARIO = 2028
    DETECT_SWITCH = 2027
    DETECT_ZONE = 2006
    DOORBELL_AUDIO_RECODE = 2042
    DOORBELL_BRIGHTNESS = 2032
    DOORBELL_DISTORTION = 2033
    DOORBELL_HDR = 2029
    DOORBELL_IR_MODE = 2030
    DOORBELL_LED_NIGHT_MODE = 2039
    DOORBELL_MOTION_ADVANCE_OPTION = 2041
    DOORBELL_MOTION_NOTIFICATION = 2035
    DOORBELL_NOTIFICATION_JUMP_MODE = 2038
    DOORBELL_NOTIFICATION_OPEN = 2036
    DOORBELL_RECORD_QUALITY = 2034
    DOORBELL_RING_RECORD = 2040
    DOORBELL_SNOOZE_START_TIME = 2037
    DOORBELL_VIDEO_QUALITY = 2031
    NIGHT_VISUAL = 2002
    OPEN_DEVICE = 2001
    RINGING_VOLUME = 2022
    SDCARD = 2010
    UN_DETECT_ZONE = 2007
    VOLUME = 2003

    # Inferred from source
    SNOOZE_MODE = 1271, Base64Converter
    WATERMARK_MODE = 1214  # 1 - hide, 2 - show
    DEVICE_UPGRADE_NOW = 1134
    CAMERA_UPGRADE_NOW = 1133
    SCHEDULE_MODE = 1257
    GUARD_MODE = 1224  # 0 - Away, 1 - Home, 63 - Disarmed, 2 - chedule
    DEVICE_STATUS = 1131, BoolConverter
    BATTERY_LEVEL = 1101
    CHARGING_STATUS = 2111
    SENSOR_OPEN = 1550, BoolConverter

    FLOODLIGHT_MANUAL_SWITCH = 1400, BoolConverter
    FLOODLIGHT_MANUAL_BRIGHTNESS = 1401  # The range is 22-100
    FLOODLIGHT_MOTION_BRIGHTNESS = 1412  # The range is 22-100
    FLOODLIGHT_SCHEDULE_BRIGHTNESS = 1413  # The range is 22-100
    FLOODLIGHT_MOTION_SENSITIVTY = 1272  # The range is 1-5

    CAMERA_SPEAKER_VOLUME = 1230
    CAMERA_RECORD_ENABLE_AUDIO = 1366  # Enable microphone
    CAMERA_RECORD_RETRIGGER_INTERVAL = 1250  # In seconds
    CAMERA_RECORD_CLIP_LENGTH = 1249  # In seconds

    CAMERA_IR_CUT = 1013
    CAMERA_PIR = 1011, BoolConverter
    CAMERA_WIFI_RSSI = 1142

    CAMERA_MOTION_ZONES = 1204, Base64Converter
    CAMERA_OFF = 99904, BoolConverter
    IS_HOMEKIT_SECURE_VIDEO = 1285
    CAMERA_NOTIFICATION_OPTIONS = 1710
    RTSP_AUTHENTICATION = 1287, Base64Converter
    DEVICE_LIST_1 = 1158, Base64Converter
    DEVICE_LIST_2 = 1157, Base64Converter
    DEV_MD_RECORD = 1273
    NIGHT_VISION_TYPE = 1277
    MOTION_SENSITIVITY = 1276
    ALARM_DELAY_HOME = 1166
    DOORBELL_CHIME_SWITCH = 1702, BoolConverter
    DOORBELL_MECHANICAL_CHIME_SWITCH = 1703, BoolConverter
    ALARM_DELAY_CUSTOM1 = 1168
    LIVEVIEW_LED_SWITCH = 1056, BoolConverter
    LEAVING_DELAY_HOME = 1171
    DOORBELL_SET_LED_ENABLE = 1716
    NAS_SWITCH = 1145, BoolConverter
    NAS_TEST = 1146
    CUSTOM3_ACTION = 1150
    DOORBELL_SET_RINGTONE_VOLUME = 1708
    CUSTOM2_ACTION = 1149
    LEAVING_DELAY_CUSTOM1 = 1173
    PIR_TEST_MODE = 1243
    OFF_ACTION = 1177
    PIR_SENSITIVITY = 1210
    DOORBELL_WDR_SWITCH = 1704
    LIGHT_CTRL_PIR_SWITCH = 1408, BoolConverter
    DOORBELL_SET_ELECTRONIC_RINGTONE_TIME = 1709
    DEV_SPEAKER_MUTE = 1241, BoolConverter
    AWAY_ACTION = 1239
    HOME_ACTION = 1225
    DEV_MIC_MUTE = 1240, BoolConverter
    DEV_LED_SWITCH = 1045, BoolConverter
    PIR_POWERMODE = 1246
    ALARM_DELAY_AWAY = 1167
    CUSTOM1_ACTION = 1148
    START_HOMEKIT = 1163
    EAS_SWITCH = 1015, BoolConverter
    BATTERY_TEMP = 1138
    ALARM_DELAY_CUSTOM2 = 1169
    LEAVING_DELAY_AWAY = 1172
    DEV_MIC_VOLUME = 1229
    LEAVING_DELAY_CUSTOM2 = 1174
    SENSOR_BAT_STATE = 1552
    SENSOR_CHANGE_TIME = 1551
    SENSOR_CHIRP_TONE = 1507
    SUB1G_RSSI = 1141
    SENSOR_CHIRP_VOLUME = 1508
    SENSOR_ALARM_ENABLE = 1506, BoolConverter
    KEYPAD_IS_PSW_SET = 1670
    UPGRADE_RESULT = 1043
    HUB_OSD = 1253
    WAN_MODE = 1265
    DELAY_CUS2 = 1160, Base64Converter
    HUB_NOTIFY_MODE = 1283
    HUB_LAN_IP = 1176, StringConverter
    TFCARD_STATUS = 1135
    LANGUAGE = 1200
    REPEATER_RSSI = 1266
    HUB_ALARM_TONE = 1281
    HUB_NOTIFY_ALARM = 1282
    DELAY_CUS1 = 1159, Base64Converter
    HUB_ALARM_AUTO_END = 1280, BoolConverter
    AI_SWITCH = 1236, BoolConverter
    CUSTOM_MODE = 1256, Base64Converter
    HUB_LOGIG = 1140

    SENSOR_OPEN_STATUS_ALERT = 1290, Base64Converter
    SENSOR_DAILY_STATUS_CHECK = 1291, Base64Converter

    # Set only params?
    PUSH_MSG_MODE = 1252  # 0 to ???


class GuardMode(Enum):
    AWAY = 0
    HOME = 1
    DISARMED = 63
    SCHEDULE = 2
    GEOFENCING = 47


class ParamDict(dict):
    def __init__(self, params):
        super().__init__()
        self.update(params)

    def __getitem__(self, key):
        return super().__getitem__(ParamType.lookup(key))

    def update(self, params):
        updateable_params = {}
        for param in list(params):
            param_type = param["param_type"]
            value = param["param_value"]
            try:
                param_type = ParamType(param_type)
                updateable_params[param_type] = param_type.load(value)
            except ValueError:
                _LOGGER.debug(
                    'Unable to process parameter "%s", value "%s"', param_type, value
                )
        super().update(updateable_params)
