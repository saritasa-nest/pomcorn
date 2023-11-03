===============================================================================
Wait conditions
===============================================================================

**Wait conditions** in Selenium are mechanisms that allow to wait for certain conditions before
performing the next actions. They are used for synchronization between the test and the web
application to ensure that elements or pages are fully loaded and ready for interaction. This helps
to avoid errors related to elements not yet appearing on the page or not being fully loaded.

Pomcorn includes several custom waiting conditions that complement the built-in Selenium waiting
list. About Selenium wait conditions you can read
`here <https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html>`_.

Package wait conditions
-------------------------------------------------------------------------------

.. automodule:: pomcorn.waits_conditions
    :members:
