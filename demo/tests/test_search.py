from pages import IndexPage


def test_search(index_page: IndexPage):
    """Check that the search on the index page works correctly.

    Check that the search query matches the expected number of packages. Also
    check if a specific package is found and click on it to redirect to the
    details page.

    """
    # Search packages by `saritasa`
    search_page = index_page.search.find("saritasa")

    # TODO: Replace to 4 after upload `pomcorn`
    # Check that presented 3 packages
    assert search_page.results.count == 3

    # Get package by name
    # TODO: Replace to `pomcorn` after upload package
    package_name = "saritasa-invocations"
    package = search_page.results.get_item_by_text(package_name)
    assert package.name == package_name

    package_details_page = package.open()
    assert package_name in package_details_page.header
