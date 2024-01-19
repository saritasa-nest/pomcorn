Version history
===============================================================================

We follow `Semantic Versions <https://semver.org/>`_.

0.4.0
*******************************************************************************

- Add ``|`` (or) operator for XPathLocators
- Add ``Page.click_on_page`` method
- Add recommendation for use keyword when specifying the ``locator`` argument
  in ``init_element`` and ``init_elements`` methods whenever possible to be
  consistent with the method of the same name in ``ComponentWithBaseLocator``

0.3.1
*******************************************************************************

- Fix type hints after `update Selenium <https://github.com/SeleniumHQ/selenium/commit/10adfe88a2b2870e3e61546b9e2a9233c9f74657>`_

0.3.0
*******************************************************************************

Backwards incompatible changes
-------------------------------------------------------------------------------
- Update ``InputByLabelLocator`` from a single-level to a nested implementation

0.2.0
*******************************************************************************

Backwards incompatible changes
-------------------------------------------------------------------------------
- Replace ``is_loaded`` property to ``check_page_is_loaded`` method

0.1.0
*******************************************************************************

- Init release
