import pytest

from pomcorn import Component, ListComponent, Page, locators
from pomcorn.constants import AutomationPlatform


class FakeItem(Component[Page]):
    """Common test component for represent item class."""

    def wait_until_visible(self, **kwargs) -> None:
        """To not wait anything."""


def test_get_item_by_text_on_web(fake_page: Page) -> None:
    """Check `get_item_by_text` method on web.

    With `AUTOMATION_PLATFORM=AutomationPlatform.WEB` (default).

    """

    class WebList(ListComponent[FakeItem, Page]):
        """Test web list component`."""

        base_locator = locators.XPathLocator("html")  # required
        relative_item_locator = locators.XPathLocator("body")  # required

    list_cls = WebList(fake_page, wait_until_visible=False)

    # Ensure that locator is built using text inside element
    item = list_cls.get_item_by_text("sample text")
    expected_query = '//html//body[contains(., "sample text")]'
    assert item.base_locator.query == expected_query

    item = list_cls.get_item_by_text("sample text", exact=True)
    assert item.base_locator.query == '//html//body[./text()="sample text"]'


def test_get_item_by_text_on_android(
    monkeypatch: pytest.MonkeyPatch,
    fake_page: Page,
) -> None:
    """Check `get_item_by_text` method on android.

    With `AUTOMATION_PLATFORM=AutomationPlatform.ANDROID`.

    """
    monkeypatch.setattr(
        "pomcorn.config.AUTOMATION_PLATFORM",
        AutomationPlatform.ANDROID,
    )

    class AndroidList(ListComponent[FakeItem, Page]):
        """Test android list component`."""

        base_locator = locators.XPathLocator("html")  # required
        relative_item_locator = locators.XPathLocator("body")  # required

    list_cls = AndroidList(fake_page, wait_until_visible=False)

    # Ensure that locator is built using `@text` attribute
    item_locator = list_cls.get_item_by_text("sample text").base_locator
    expected_query = (
        "(//html//body)"
        '[self::node()[contains(@text, "sample text")] '
        '| .//*[contains(@text, "sample text")]]'
    )
    assert item_locator.query == expected_query

    item = list_cls.get_item_by_text("sample text", exact=True)
    expected_query = (
        "(//html//body)"
        '[self::node()[@text="sample text"] '
        '| .//*[@text="sample text"]]'
    )
    assert item.base_locator.query == expected_query
