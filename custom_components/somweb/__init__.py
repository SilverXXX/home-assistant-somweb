"""SOMweb garage door integration."""
# import asyncio
# import logging
# from homeassistant import config_entries, core
import json
from datetime import timedelta
import logging
from homeassistant.helpers.entity_component import EntityComponent

from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the SOMWeb platform."""
    conf_array = config.get("cover")
    if conf_array is None:
        return True

    for config in conf_array:
        if config["platform"] == DOMAIN:
            hass.config_entries.async_forward_entry_setup(config, "cover")

    return True


async def async_setup_entry(hass, config):
    """Set up the SOMweb cover."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config, "cover")
    )

    return True


# async def async_unload_entry(hass, config_entry):
#     """Unload a config entry."""
#     unload_ok = await hass.config_entries.async_forward_entry_unload(
#         config_entry, "cover"
#     )
#     return unload_ok


# async def async_setup(hass, config):

#     component = hass.data[DOMAIN] = EntityComponent(_LOGGER, DOMAIN, hass, SCAN_INTERVAL)
#     await component.async_setup(config)


# async def async_setup_entry(
#     hass: core.HomeAssistant,
#     config_entry: config_entries.ConfigEntry,
#     # async_add_devices,
# ) -> bool:
#     """Set up entry."""

#     hass.data.setdefault(DOMAIN, {})

#     hass_data = dict(config_entry.data)

#     # Registers update listener to update config entry when options are updated.
#     unsub_options_update_listener = config_entry.add_update_listener(
#         options_update_listener
#     )

#     # Store a reference to the unsubscribe function to cleanup if an entry is unloaded.
#     hass_data["unsub_options_update_listener"] = unsub_options_update_listener
#     hass.data[DOMAIN][config_entry.entry_id] = hass_data

#     # Forward the setup to the sensor platform.
#     hass.async_create_task(
#         hass.config_entries.async_forward_entry_setup(config_entry, "cover")
#     )
#     return True


# async def options_update_listener(
#     hass: core.HomeAssistant, config_entry: config_entries.ConfigEntry
# ):
#     """Handle options update."""
#     await hass.config_entries.async_reload(config_entry.entry_id)


# async def async_unload_entry(
#     hass: core.HomeAssistant, entry: config_entries.ConfigEntry
# ) -> bool:
#     """Unload a config entry."""
#     unload_ok = all(
#         await asyncio.gather(
#             *[hass.config_entries.async_forward_entry_unload(entry, "cover")]
#         )
#     )

#     # Remove options_update_listener.
#     hass.data[DOMAIN][entry.entry_id]["unsub_options_update_listener"]()

#     # Remove config entry from domain.
#     if unload_ok:
#         hass.data[DOMAIN].pop(entry.entry_id)

#     return unload_ok


# async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
#     """Set up the component from yaml configuration."""
#     hass.data.setdefault(DOMAIN, {})
#     return True