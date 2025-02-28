import pytest

from pomcorn.locators.base_locators import XPathLocator

TEST_QUERY = "//span[text()='Users']"


@pytest.mark.parametrize(
    argnames=("index", "result"),
    argvalues=[
        (-2, f"({TEST_QUERY})[last()-1]"),
        (-1, f"({TEST_QUERY})[last()]"),
        (0, f"({TEST_QUERY})[1]"),
        (1, f"({TEST_QUERY})[2]"),
    ],
)
def test_getting_related_xpath_locators_by_index(index: int, result: str):
    """Check that getting related xpath locators by index works correct."""
    locator = XPathLocator(TEST_QUERY)
    assert locator[index].query == result
