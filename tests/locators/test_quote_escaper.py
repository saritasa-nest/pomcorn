from pomcorn.locators.base_locators import XPathLocator


def test_empty_string():
    """Test that an empty string returned as wrapped empty string."""
    assert XPathLocator._escape_quotes("") == '""'


def test_no_quotes():
    """Test that a string without quotes returned as wrapped passed text."""
    assert XPathLocator._escape_quotes("Hello World") == '"Hello World"'


def test_single_quote():
    """Test escaping a string with a single quote."""
    assert (
        XPathLocator._escape_quotes("He's tall")
        == 'concat("He", "\'", "s tall")'
    )


def test_double_quote():
    """Test escaping a string with a double quote."""
    assert (
        XPathLocator._escape_quotes('She said "Hello"')
        == 'concat("She said ", \'"\', "Hello", \'"\')'
    )


def test_both_single_and_double_quotes():
    """Test escaping a string with both single and double quotes."""
    assert (
        XPathLocator._escape_quotes("He's 6'2\" tall")
        == 'concat("He", "\'", "s 6", "\'", "2", \'"\', " tall")'
    )


def test_string_starts_with_quote():
    """Test escaping a string that starts with a quote."""
    assert XPathLocator._escape_quotes('"Start') == 'concat(\'"\', "Start")'


def test_string_ends_with_quote():
    """Test escaping a string that ends with a quote."""
    assert XPathLocator._escape_quotes('End"') == 'concat("End", \'"\')'


def test_string_with_only_quotes():
    """Test escaping a string that contains only quotes."""
    assert XPathLocator._escape_quotes('""') == "concat('\"', '\"')"
    assert XPathLocator._escape_quotes("''") == 'concat("\'", "\'")'
