import pytest
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from demo.pages import HelpPage, IndexPage, SearchPage


# You can implement your own logic to initialize a webdriver.
# An example of Chrome initialization is described below.
@pytest.fixture(scope="session")
def webdriver() -> WebDriver:
    """Initialize `Chrome` webdriver."""
    options = selenium_webdriver.ChromeOptions()

    # Set browser's language to English
    prefs = {"intl.accept_languages": "en,en_U"}
    options.add_experimental_option("prefs", prefs)

    webdriver = selenium_webdriver.Chrome(options)
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
