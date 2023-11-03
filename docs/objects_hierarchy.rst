===============================================================================
Object Hierarchy
===============================================================================

Pomcorn includes next object hierarchy for Page Object Model (``POM``) page creation:

.. image:: _static/images/class_diagram.png
    :alt: Class diagram

WebView class
*******************************************************************************

A common object that has utils to work with a webdriver, e.g. checking and locating elements,
moving to other pages.

Page class
*******************************************************************************

A top level object, basically the web page itself. Responsible for keeping elements and components.
Descendant of **WebView**.

Component classes
*******************************************************************************

**Component** is a group of elements that can be found on different pages (e.g. a list with search
bar). Descendant of `WebView`.

**ComponentWithBaseLocator** - It's a class, descendant of **Component**, with implemented
additional logic of waiting until it becomes visible/invisible. During initialization, it waits for
the base locator (see :ref:`Locators<Locators>`), which will be used to search for this component in
its waiting methods. Also, the base locator will be used to create the `body` attribute, which will
represent the component body to interact with it.


.. note::
    Using **ComponentWithBaseLocator** is more preferable, because unlike **Component**, this
    component implements methods of waiting until it becomes visible/invisible, including in
    ``__init__`` method. This will allow you to make your test more stable because the component
    will wait until it becomes visible before returning its instance.

**ListComponent** - It's a class, descendant of **Component**, with implemented methods for work
with list-like components: ``all``, ``count`` and ``get_item_by_text``.

Element class
*******************************************************************************

A smallest part of page(component). It can be a button, link, or just some text. In general, you can
imagine that this is an html tag.
