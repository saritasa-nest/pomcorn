import pytest

from pomcorn.locators.base_locators import XPathLocator


@pytest.mark.parametrize(
    argnames=["base_locator", "child_locator", "operator", "expected_xpath"],
    argvalues=[
        [XPathLocator("//div"), XPathLocator("/span"), "/", "//div/span"],
        [XPathLocator("//div"), XPathLocator("//span"), "//", "//div//span"],
        [XPathLocator("//ul/li"), XPathLocator("//a"), "/", "//ul/li/a"],
        [
            XPathLocator("(//li)[2]"),
            XPathLocator("//button"),
            "/",
            "(//li)[2]/button",
        ],
        [
            XPathLocator("(//li)[2]"),
            XPathLocator("/button"),
            "//",
            "(//li)[2]//button",
        ],
        [XPathLocator(""), XPathLocator("/span"), "/", "/span"],
        [XPathLocator("//div"), XPathLocator(""), "/", "//div"],
    ],
)
def test_combining_xpath_locators(
    base_locator: XPathLocator,
    child_locator: XPathLocator,
    operator: str,
    expected_xpath: str,
) -> None:
    """Test combining two XPathLocator instances with `/` or `//`."""
    result = (
        base_locator / child_locator
        if operator == "/"
        else base_locator // child_locator
    )
    assert str(result) == expected_xpath


@pytest.mark.parametrize(
    argnames=["base_locator", "raw_suffix", "operator", "expected_xpath"],
    argvalues=[
        [XPathLocator("//div"), "//span", "/", "//div/span"],
        [XPathLocator("//section"), "/a[@href]", "//", "//section//a[@href]"],
    ],
)
def test_combining_with_raw_string_suffix(
    base_locator: XPathLocator,
    raw_suffix: str,
    operator: str,
    expected_xpath: str,
) -> None:
    """Test combining an XPathLocator with a raw string."""
    result = (
        base_locator / raw_suffix
        if operator == "/"
        else base_locator // raw_suffix
    )
    assert str(result) == expected_xpath


def test_combining_empty_locators_raises_error() -> None:
    """Test that combining two empty XPathLocators raises ValueError."""
    first_locator = XPathLocator("")
    second_locator = XPathLocator("")
    with pytest.raises(ValueError, match="Both of locators have empty query"):
        _ = first_locator / second_locator
    with pytest.raises(ValueError, match="Both of locators have empty query"):
        _ = first_locator // second_locator
