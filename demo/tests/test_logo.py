from pages import HelpPage


def test_logo(help_page: HelpPage):
    """Check that click on site logo redirect to index page."""
    old_url = help_page.current_url
    index_page = help_page.click_on_logo()
    index_page.wait_until_url_changes(old_url)

    assert help_page.current_url.endswith("pypi.org/")
