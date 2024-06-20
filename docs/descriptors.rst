===============================================================================
Descriptors
===============================================================================

``pomcorn`` now provides descriptor for **Elements**. This allows us to define
elements as class attributes of a page or component. Example of usage:

.. code-block:: python

  from pomcorn import Element, Page, locators
  from demo.pages.common.navigation_bar import Navbar

  class PyPIPage(Page):

      search_input = Element(locators.ClassLocator("search"))

The descriptor takes a locator to locate element on page or inside component
(then we need to pass ``is_relative_locator=true``) and creates a new instance
of element the first time ``search_input`` attribute is accessed and caches it
to return the cached value the next time.

The cache is intended to avoid calling ``wait_until_visible`` multiple times in
the initialization of the element.

*******************************************************************************
Element descriptor interfaces
*******************************************************************************

.. _Element:

.. autoclass:: pomcorn.descriptors.Element
   :members:

   :special-members: __init__
   :exclude-members: Element
