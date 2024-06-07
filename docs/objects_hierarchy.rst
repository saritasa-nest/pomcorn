===============================================================================
Object Hierarchy
===============================================================================

Pomcorn includes next object hierarchy for Page Object Model (``POM``) page creation:


.. mermaid::

  classDiagram
    WebView <|-- Component
    WebView <|-- Page
    Component <|-- ListComponent
    Component .. Locator
    Page .. Component

    class WebView{
        -webdriver: Webdriver
    }
    class Page{
        +wait_until_loaded()
        +open()
    }
    class Component{
        -page: Page
        -base_locator: Locator
        + wait_until_visible()
    }
    class ListComponent{
        -item_locator: Locator
        +count()
        +all()
        +get_item_by_text()
    }
    class Locator{
      -query: String
    }

|

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
bar). Descendant of `WebView`. It has implemented logic of waiting until it becomes
visible/invisible. During initialization, it waits for the base locator
(see :ref:`Locators<Locators>`), which will be used to search for this component in its waiting
methods. Also, the base locator will be used to create the `body` attribute, which will represent
the component body to interact with it.

**ListComponent** - It's a class, descendant of **Component**, with implemented methods for work
with list-like components: ``all``, ``count`` and ``get_item_by_text``.

PomcornElement class
*******************************************************************************

A smallest part of page(component). It can be a button, link, or just some text. In general, you can
imagine that this is an html tag.


.. note::
    The class is rarely initiated in its pure form, so we added descriptors for easy definition of
    element-attributes (see :ref:`descriptors<Descriptors>`), and within **Page** and **Component**
    classes, an element can be defined using the :ref:`self.init_element<WebView>` method.
