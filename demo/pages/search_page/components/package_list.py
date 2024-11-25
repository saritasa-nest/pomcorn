from demo.pages import PyPIPage
from pomcorn import ListComponent, locators

from .package import Package


class PackageList(ListComponent[Package, PyPIPage]):
    """Represent the list of search results on `SearchPage`."""

    # By default `ListComponent` have `item_class` attribute with stored first
    # Generic variable (Package in current case). This attribute is responsible
    # for the class that will be used for list items.

    base_locator = locators.PropertyLocator(
        prop="aria-label",
        value="Search results",
    )

    # Set up ``relative_item_locator`` or ``item_locator`` is required.
    # Use ``relative_item_locator`` - if you want locator nested within
    # ``base_locator``, ``item_locator`` - otherwise."
    # You also may override ``base_item_locator`` property.
    relative_item_locator = locators.ClassLocator(
        class_name="package-snippet",
        container="a",
    )
