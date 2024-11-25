from demo.pages import IndexPage


def test_search(index_page: IndexPage):
    """Check that the search on the index page works correctly.

    Check that the search query matches the expected number of packages. Also
    check if a specific package is found and click on it to redirect to the
    details page.

    """
    # Search packages by `saritasa`
    search_page = index_page.search.find("saritasa")

    # Check that at least 4 packages are presented
    assert search_page.results.count >= 4

    # Get package by name
    package_name = "pomcorn"
    package = search_page.results.get_item_by_text(package_name)
    assert package.name == package_name

    package_details_page = package.open()
    assert package_name in package_details_page.header
