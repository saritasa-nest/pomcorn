===============================================================================
Locators
===============================================================================

**Locators** are special mechanisms used to find elements on a web page. They allow to locate
specific elements such as buttons, input fields, or links to interact with them.

The Selenium webdriver methods use tuples ``(By, query)`` to find elements, where ``By`` is one of
the `supported locator <https://www.selenium.dev/documentation/webdriver/elements/locators/#traditional-locators>`_
strategies and ``query`` is the query for that strategy.
About Selenium supported locator strategies you can read
`here <https://www.selenium.dev/documentation/webdriver/elements/locators/>`_.

Pomcorn implements its own classes for defining web page elements - **Locators**.
`XPath <https://www.selenium.dev/documentation/webdriver/elements/locators/#xpath>`_ was chosen as the
only strategy because it eliminated the need to specify the type of strategy and also made it easier
to create `relative locators <https://www.selenium.dev/documentation/webdriver/elements/locators/#relative-locators>`_.

.. note::
  `Others <https://playwright.dev/python/docs/locators#locate-by-css-or-xpath>`_ prefer NOT to use
  XPath because the DOM can change frequently and tests will crash. Therefore, to make the tests
  more stable, we have implemented a number of locators that follow the same logic as the other
  strategies (search by css, by tag name, by classes, by properties, etc.), but based on XPath.

*******************************************************************************
Interfaces
*******************************************************************************

.. mermaid::

  classDiagram
    Locator <|-- XPathLocator
    XPathLocator <|-- TInitLocator
    XPathLocator <|-- TLocator
    XPathLocator <|-- ElementWithTextLocator
    XPathLocator <|-- InputByLabelLocator
    XPathLocator <|-- PropertyLocator
    XPathLocator <|-- TagNameLocator
    XPathLocator <|-- TextAreaByLabelLocator

    PropertyLocator <|-- ClassLocator
    PropertyLocator <|-- DataTestIdLocator
    PropertyLocator <|-- IdLocator
    PropertyLocator <|-- NameLocator
    ElementWithTextLocator <|-- ButtonWithTextLocator

| * you can zoom it

.. _Locator:

.. autoclass:: pomcorn.locators.Locator
   :members:

.. _XPathLocator:

.. autoclass:: pomcorn.locators.XPathLocator
   :members:
   :special-members: __init__

.. automodule:: pomcorn.locators.xpath_locators
   :members:
   :special-members: __init__
