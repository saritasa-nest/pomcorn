from pages import HelpPage, IndexPage, SearchPage
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import pytest


# You can implement your own logic to initialize a webdriver.
# An example of Chrome initialization is described below.
@pytest.fixture(scope="session")
def webdriver() -> WebDriver:
    """Initialize `Chrome` webdriver."""
    webdriver = selenium_webdriver.Chrome()
    webdriver.set_window_size(1920, 1080)
    return webdriver


@pytest.fixture
def index_page(webdriver: WebDriver) -> IndexPage:
    """Open index page of PyPI and return instance of it."""
    return IndexPage.open(webdriver)


@pytest.fixture
def help_page(webdriver: WebDriver) -> HelpPage:
    """Open help page of PyPI and return instance of it."""
    return HelpPage.open(webdriver)


@pytest.fixture
def results_page(webdriver: WebDriver) -> SearchPage:
    """Open search results page of PyPI and return instance of it."""
    return SearchPage.open(webdriver)
