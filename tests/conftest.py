import pytest

from pomcorn import Page


@pytest.fixture
def fake_page() -> Page:
    """Prepare fake page object for run tests without browser."""
    return Page(webdriver=None, app_root="None")  # type: ignore
