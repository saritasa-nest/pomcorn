import pytest

from pomcorn.locators.base_locators import XPathLocator

TEST_QUERY = "//span[text()='Users']"


@pytest.mark.parametrize(
    argnames=["value", "expected_query"],
    argvalues=[
        # Getting by index
        [-2, f"({TEST_QUERY})[last() - 1]"],
        [-1, f"({TEST_QUERY})[last()]"],
        [0, f"({TEST_QUERY})[1]"],
        [1, f"({TEST_QUERY})[2]"],
        # Set xpath expressions
        ["@type='black'", f"({TEST_QUERY})[@type='black']"],
        # Set related locator
        [XPathLocator("//custom-xpath"), f"({TEST_QUERY})[//custom-xpath]"],
    ],
)
def test_xpath_square_brackets_logic(
    value: int | str | XPathLocator,
    expected_query: str,
):
    """Check that square bracket works correct.

    Make sure we can specify an index, xpath expression or locator in square
    brackets or locator object.

    """
    locator = XPathLocator(TEST_QUERY)
    assert locator[value].query == expected_query
