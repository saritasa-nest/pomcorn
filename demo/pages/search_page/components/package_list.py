from pages import PyPIPage

from pomcorn import ListComponent, locators

from .package import Package


class PackageList(ListComponent[Package, PyPIPage]):
    """Represent the list of search results on `SearchPage`."""

    # The `ListComponent` item should always be `ComponentWithBaseLocator`,
    # because all its methods depend on `base_locator`
    item_class = Package

    def __init__(
        self,
        page: PyPIPage,
        # We use the empty init to set the default value for `base_locator`
        base_locator: locators.XPathLocator = locators.PropertyLocator(
            prop="aria-label",
            value="Search results",
        ),
        wait_until_visible: bool = True,
    ):
        super().__init__(page, base_locator, wait_until_visible)

    # Set up `base_item_locator` and `item_class` is required
    @property
    def base_item_locator(self) -> locators.XPathLocator:
        """Get the base locator of result item."""
        return self.base_locator // locators.ClassLocator(
            class_name="package-snippet",
            container="a",
        )
