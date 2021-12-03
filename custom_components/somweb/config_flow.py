import logging
from typing import Any, Dict, Optional
from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_ID, CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from .const import DOMAIN
from somweb import SomwebClient as Client

# from .cover import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ID): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


async def validate_input(user_input: Dict[str, str]) -> None:
    """Validates somweb connection."""
    udi = user_input[CONF_ID]
    username = user_input[CONF_USERNAME]
    password = user_input[CONF_PASSWORD]

    if udi == None or len(udi) == 0:
        raise InvalidSomwebId

    if username == None or len(username) == 0 or password == None or len(password) == 0:
        raise InvalidCredentials

    try:
        int(udi)
    except:
        raise InvalidSomwebId

    client = Client(udi, username, password)
    is_alive = False
    try:
        is_alive = await client.is_alive()
    except:
        pass

    if not is_alive:
        raise CannotConnect

    if not (await client.authenticate()).success:
        raise InvalidCredentials


@config_entries.HANDLERS.register(DOMAIN)
class SomwebConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Somweb config flow."""

    VERSION = 1
    DDD = config_entries.CONN_CLASS_LOCAL_POLL
    # CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_user(self, user_input: Optional[Dict[str, str]] = None):
        errors: Dict[str, str] = {}
        if user_input is not None:
            udi = None
            try:
                udi = user_input[CONF_ID]
                await validate_input(user_input)
            except CannotConnect:
                errors[CONF_ID] = "cannot_connect"
            except InvalidSomwebId:
                errors[CONF_ID] = "invalid_id"
            except InvalidCredentials:
                errors[CONF_USERNAME] = "invalid_credentials"
                errors[CONF_PASSWORD] = "invalid_credentials"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            await self.async_set_unique_id(udi)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"Somweb {udi}", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )


class InvalidCredentials(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidSomwebId(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid somweb id."""