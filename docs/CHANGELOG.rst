Version history
===============================================================================

We follow `Semantic Versions <https://semver.org/>`_.

0.8.6 (13.03.25)
*******************************************************************************
- Replace isort, black, flake with Ruff
- Replace error message handling via try-except block in wait methods with built-in
  selenium's message attribute of the `wait.until` method.

Backwards incompatible changes in 0.8.6
-------------------------------------------------------------------------------
- Remove custom errors. Custom errors were used only in `wait.until` that wrapped try-except block.
  Since the error message can be set directly in `wait.until`, these errors have been removed.

0.8.5 (10.02.25)
*******************************************************************************
- Add ability to get related xpath locators by index for ``XPathLocator``

0.8.4 (30.01.25)
*******************************************************************************
- Add escaping single and double quotes in the: ``ElementWithTextLocator``,
  ``InputInLabelLocator``, ``InputByLabelLocator``, ``TextAreaByLabelLocator``.
- Add escaping single and double quotes in the ``get_item_by_text`` method of
  the ``ListComponent``

0.8.3 (20.12.24)
*******************************************************************************
- Rename ``__parameters__`` in ``ListComponent`` to ``__generic__parameters``
  to avoid problems with Python build-in functions

0.8.2 (19.12.24)
*******************************************************************************
- Add ability to specify ``TypeAlias`` as ``_item class`` and use
  ``ListComponent`` as a parameterized type

0.8.1 (25.11.24)
*******************************************************************************
- Improve getting ``item class`` from first ``ListComponent`` generic variable.
  There were several cases where this didn't work correctly (for multiple generic variables
  and inheritance). Examples of such cases are presented in `this PR <https://github.com/saritasa-nest/pomcorn/pull/98#issuecomment-2485811259>`_.\

**Warning**: The ``item_class`` class attribute was removed.

0.8.0 (05.07.24)
*******************************************************************************
- Add ability to not specify ``item_class`` in ``ListComponent``. Instead, it
  will be automatically filled with value passed in ``Generic[ListItemType]``.

**Warning**: The ``item_class`` specification is still available, but it is
deprecated and will be removed soon.

0.7.5
*******************************************************************************
- Remove redundant call of ``scroll_to`` in ``PomcornElement.click()``.
  This is redundant, as webdriver by default scrolls to element before click (`docs <https://www.w3.org/TR/webdriver2/#element-click>`_).

0.7.4
*******************************************************************************
- Improve ``Page.click_on_page()`` method to click the page coordinates instead
  of offset relative to  current mouse position

0.7.3
*******************************************************************************
- Add ability to not specify ``app_root`` in ``Page.open_from_url()`` as in ``Page.open()``

0.7.2
*******************************************************************************
- Improve ``Page.click_on_page()`` method to click on <html> tag
- Improve ``Page.open_from_url()`` to support kwargs
- Fix ``\`` related problems in ``Page._get_full_relative_url()``

0.7.1
*******************************************************************************

- Add ability to `Element` to specify simple and relative locators using the
  `locator` or `relative_locator` arguments, as in `Component.init_element <https://github.com/saritasa-nest/pomcorn/blob/main/pomcorn/component.py>`_.
- Fix some possible xpath errors depending on empty locators queries and
  brackets.

0.7.0
*******************************************************************************

- Update diagrams with `mermaid <https://mermaid.js.org/intro/>`__
- Add invocation **inv docs.serve** to run docs on localhost
- Add auto-scroll to element before click
- Add page class name to ``PageDidNotLoadedError``
- Add method ``contains()`` to ``XPathLocator`` for search by contained text

Backwards incompatible changes in 0.7.0
-------------------------------------------------------------------------------
- Remove simple ``Component`` class
- Rename ``ComponentWithBaseLocator`` to ``Component``

- Rename ``Element`` class to ``PomcornElement``
- Add descriptor ``Element`` to simplify adding element-attributes to **Pages**
  and **Components**

0.6.0
*******************************************************************************

Backwards incompatible changes in 0.6.0
-------------------------------------------------------------------------------
- Updating the ``Page.click_on_page`` method: now it clicks on (1, 1) page
  coordinates, because clicking on the html tag was done in the center of the
  page, which led to unexpected situations
- ``InputByLabelLocator`` is split into ``InputByLabelLocator`` (for non-nested
  case) and ``InputInLabelLocator`` (for nested case)

0.5.0
*******************************************************************************

- Add ability to specify ``base_locator`` for ``ComponentWithBaseLocator`` as a
  class attribute, so as not to override `__init__` (Issue: `#34 <https://github.com/saritasa-nest/pomcorn/issues/34>`_)
- Add ability to specify ``base_item_locator`` via ``item_locator`` and
  ``relative_item_locator`` attributes for ``ListComponent`` to avoid
  overriding ``property`` each time and simplify creation of nested items
  locators

0.4.0
*******************************************************************************

- Add ``|`` (or) operator for XPathLocators
- Add ``Page.click_on_page`` method
- Add recommendation for use keyword when specifying the ``locator`` argument
  in ``init_element`` and ``init_elements`` methods whenever possible to be
  consistent with the method of the same name in ``ComponentWithBaseLocator``
- Improve ``WebView.scroll_to()``

0.3.1
*******************************************************************************

- Fix type hints after `update Selenium <https://github.com/SeleniumHQ/selenium/commit/10adfe88a2b2870e3e61546b9e2a9233c9f74657>`_

0.3.0
*******************************************************************************

Backwards incompatible changes in 0.3.0
-------------------------------------------------------------------------------
- Update ``InputByLabelLocator`` from a single-level to a nested implementation

0.2.0
*******************************************************************************

Backwards incompatible changes in 0.2.0
-------------------------------------------------------------------------------
- Replace ``is_loaded`` property to ``check_page_is_loaded`` method

0.1.0
*******************************************************************************

- Init release
