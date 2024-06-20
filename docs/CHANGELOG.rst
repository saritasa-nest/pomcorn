Version history
===============================================================================

We follow `Semantic Versions <https://semver.org/>`_.

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
