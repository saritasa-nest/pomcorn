# Demo Autotests Project

This is a demo autotest project implemented with `pomcorn` package for `PyPI` web site.
To start tests in this project you need to prepare a python virtual environment and install
according driver for Chrome browser.

You can get a demo project from
[package repository](https://github.com/saritasa-nest/pomcorn/tree/main/demo).

## Setup

### Environment

The simplest way to configure a proper Python version and virtual environment
is using [uv](https://docs.astral.sh/uv/).

Install dependencies and activate your `virtualenv`

```bash
uv sync --only-group demo
source .venv/bin/activate
```

[Install Chrome webdriver](https://saritasa-nest.github.io/pomcorn/latest/installation/#chrome-driver).

## Running Autotests

To run tests, use invoke command `pytest`:

```bash
inv pytest.run
```

## About the project

This project is a mini autotesting system for the [PyPI](https://pypi.org/) website.
It implements the basic structure of pages and tests according to **Page Object Model** pattern.

The project structure looks like this
(`__init__.py` files were skipped to simplify the structure):

```bash
│ demo/
├── pages/
│   ├── base/
│   │   ├── base_components.py
│   │   └── base_page.py
│   ├── common/
│   │   ├── navigation_bar.py
│   │   └── search.py
│   ├── search_page/
│   │   ├── components/
│   │   │   ├── package_list.py
│   │   │   └── package.py
│   │   └── search_page.py
│   ├── help_page.py
│   ├── index_page.py
│   └── package_details_page.py
├── tests
│   ├── test_logo.py
│   └── test_search.py
└── conftest.py
```

### Pages

This folder contains the page and component classes required to represent PyPI web pages.
These classes contain web page interaction logic to make tests free of that implementation.

#### Base Folder

Basic classes for PyPI pages and components are implemented here.

##### Base Components

:::demo.pages.base.base_components

##### Base Page

!!! note
    The `check_page_is_loaded` method and the `APP_ROOT` attribute require special attention
    here.

:::demo.pages.base.base_page

#### Common

This folder contains components common to multiple pages.

##### Navigation Bar

This class represents navigation bar on the top side of all PyPI pages.

![PyPI navigation bar](_static/images/pypi_navbar.png)

:::demo.pages.common.navigation_bar

##### Search component

This class represents a search field that can be placed on multiple pages.

| Search field examples |
| --- |
| [Index page](https://pypi.org/) |
| ![Search field on PyPI index page](_static/images/pypi_search_index.png) |
| [Navbar](https://pypi.org/search/) |
| ![Search field on PyPI navigation bar](_static/images/pypi_search_navbar.png) |

:::demo.pages.common.search

#### Search Page Folder

##### Search Page Components

Because a number of additional components needed to be created to implement the search page,
a separate folder was created for this page. This is where the page itself and its dependent
components are stored.

###### Package List

This class represents a list of found packages on the PyPI search page.

![PyPI Package List](_static/images/pypi_package_list.png)

:::demo.pages.search_page.components.package_list

###### Package

This class represents one found package listed on the PyPI search page.

![PyPI Package](_static/images/pypi_package.png)

:::demo.pages.search_page.components.package

###### Search Page

This class represents the PyPI [search page](https://pypi.org/search/).

![PyPI Search Page](_static/images/pypi_search_results.png)

:::demo.pages.search_page.search_page

#### Help Page

This class represents the PyPI [help page](https://pypi.org/help/). The `title` property is
implemented here to show how you can use page properties to implement the `check_page_is_loaded`
method.

![Help page title](_static/images/pypi_help_title.png)

:::demo.pages.help_page

#### Index Page

This class represents the PyPI [start page](https://pypi.org/). This page shows the use
of the class [Search component](#search-component).

![Search field on PyPI index page](_static/images/pypi_search_index.png)

:::demo.pages.index_page

#### Package Details Page

This class represents the PyPI
[package details page](https://pypi.org/project/pomcorn/).

![Package details page](_static/images/pypi_package_details.png)

:::demo.pages.package_details_page

!!! note
    You don't have to implement the `check_page_is_loaded` page method if this property is set on
    the base page and is appropriate for the current page.

### Tests

This folder contains autotests that use pages prepared in [fixtures](#conftest) to reproduce
some scenarios of user interaction with the site.

#### Test Logo

:::demo.tests.test_logo

### Conftest

Here are the implemented base [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html#fixtures)
for implemented PyPI pages. This is useful practice to avoid duplicating page opening calls in
each test.
Also, the [webdriver](https://www.selenium.dev/selenium/docs/api/py/api.html#webdriver-chrome)
fixture with a given window size (1920×1080) is implemented here.

:::demo.conftest
