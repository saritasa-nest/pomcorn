import os

from .constants import AutomationPlatform


def _get_automation_platform() -> AutomationPlatform:
    """Get automation platform from environment variable.

    Returns:
        Automation platform. AutomationPlatform.WEB by default.

    Raises:
        ValueError: If the environment variable has an invalid value.

    """
    value = os.getenv("POMCORN_AUTOMATION_PLATFORM")

    if value is None:
        return AutomationPlatform.WEB

    try:
        return AutomationPlatform(value)
    except ValueError as error:
        raise ValueError(
            f"Invalid POMCORN_AUTOMATION_PLATFORM={value!r}. "
            f"Expected one of: {[p.value for p in AutomationPlatform]}",
        ) from error


# Initially pomcorn was used for web automation testing. Now we started
# adapting it for Android testing as well. In Android apps, elements don't
# contain text inside them. Instead, they use the @text attribute.
# This variable defines which platform is automated in project.
# Also can be set by specifying `POMCORN_AUTOMATION_PLATFORM` env variable.
AUTOMATION_PLATFORM: AutomationPlatform = _get_automation_platform()
