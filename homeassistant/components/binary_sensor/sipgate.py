"""
Support for Sipgate.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/sipgate/
"""
import logging

from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD)
from homeassistant.components.binary_sensor import (
    BinarySensorDevice, PLATFORM_SCHEMA)

DOMAIN = 'sipgate'
DEFAULT_DEVICE_CLASS = 'connectivity'
ICON = 'mdi:phone-android'
NAME_PREFIX = 'sipgate_device_'

REQUIREMENTS = ['sipgate==0.0.1']
_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Sipgate platform."""

    _LOGGER.info('setup')
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    from sipgate import Client
    client = Client(username, password)
    devices = []
    phones = client.devices()
    for phone in phones:
        device = SipgateDevice(client, phone)
        devices.append(device)

    add_devices(devices, True)

class SipgateDevice(BinarySensorDevice):
    """Represents a Sipgate device, i.e. a phone"""
    def __init__(self, client, phone):
        self._id = phone.id
        self._client = client
        self._name = NAME_PREFIX + self._id
        self.update_from_phone(phone)

    def update_from_phone(self, phone):
        """Refresh the device properties with values from the API object"""
        self._alias = phone.alias
        self._online = bool(phone.online)
        _LOGGER.info('Online state is now %s', self._online)

    def update(self):
        """Updates the entity"""
        _LOGGER.info('Updating Sipgate device %s', self._id)
        phone = self._client.device_by_id(self._id)
        _LOGGER.info('Result was %s, %s, %s', phone.alias, phone.online, phone.id)
        self.update_from_phone(phone)


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_id(self):
        """Returns the device id"""
        return self._id

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return DEFAULT_DEVICE_CLASS

    @property
    def is_on(self):
        """Return true if sensor is on."""
        _LOGGER.info('is_on')
        return self._online

    @property
    def device_state_attributes(self):
        """Return the state attributes of the ICMP checo request."""
        _LOGGER.info('device_state_attributes')
        return {
            'online': self._online,
            'friendly_name': self._alias}
