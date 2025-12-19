===============================================================================
Project Configuration
===============================================================================

There are several ways to configure Pomcorn to suit your project's needs.

*******************************************************************************
Environment Variables
*******************************************************************************

Pomcorn can be configured using environment variables. The following variables
are available:

* ``POMCORN_AUTOMATION_PLATFORM``: Sets the default automation platform
  (e.g., ``web``, ``android``). See available platforms in ``AutomationPlatform``
  enumeration. By default everywhere is used ``web``. Value of this variable
  affects to:
  - how locators are prepared in ``ListComponent.get_item_by_text``
