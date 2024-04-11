===============================================================================
Descriptors
===============================================================================

**Descriptors** are a powerful feature that allows you to define custom
behavior for attribute access, assignment, and deletion. When an attribute is
accessed, assigned, or deleted, Python will call the corresponding descriptor
method if it is defined. You can read more about descriptors
`here <https://realpython.com/python-descriptors/>`_ or
`here <https://docs.python.org/3/howto/descriptor.html>`_.

``pomcorn`` provides two kinds of descriptors - for **Elements** and
**Components**, and a number of child classes from them.


*******************************************************************************
Descriptors usage
*******************************************************************************

.. code-block:: python

  from pomcorn import Page
  from pomcorn.descriptors import ElementById, GetComponent

  from demo.pages.common.navigation_bar import Navbar

  class PyPIPage(Page):

      # Descriptors have been added to simplify initialization of elements
      search_input = ElementById("search")
      # and components as page/components classes attributes
      navbar = GetComponent[Navbar]()


*******************************************************************************
Element descriptor interfaces
*******************************************************************************

.. _GetElement:

.. autoclass:: pomcorn.descriptors.GetElement
   :members:

.. automodule:: pomcorn.descriptors.elements
   :members:
   :special-members: __init__
   :exclude-members: GetElement

*******************************************************************************
Component descriptor interfaces
*******************************************************************************

.. _GetComponent:

.. autoclass:: pomcorn.descriptors.GetComponent
   :members:

.. automodule:: pomcorn.descriptors.components
   :members:
   :special-members: __init__
   :exclude-members: GetComponent
