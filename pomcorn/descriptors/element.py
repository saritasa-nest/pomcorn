from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from pomcorn import locators

if TYPE_CHECKING:
    from pomcorn import WebView, XPathElement


class Element:
    """Descriptor for init `PomcornElement` as attribute by locator.

    .. code-block:: python

        # Example
        from pomcorn import Page, Element

        class MainPage(Page):
            title_element = Element(locators.ClassLocator("page-title"))

    """

    cache_attribute_name = "cached_elements"

    def __init__(
        self,
        locator: locators.XPathLocator,
        is_relative_locator: bool = True,
    ) -> None:
        """Initialize descriptor.

        Args:
            locator: Instance of a class to locate the element in
                the browser.
            is_relative_locator: Whether add parent ``base_locator`` to the
                current descriptors's `base_locator` or not. If descriptor is
                used for ``Page``, the value of this argument will not be used.

        """
        self.is_relative_locator = is_relative_locator
        self.locator = locator

    def __set_name__(self, _owner: type, name: str) -> None:
        """Save attribute name for which descriptor is created."""
        self.attribute_name = name

    def __get__(
        self,
        instance: WebView | None,
        _type: type[WebView],
    ) -> XPathElement:
        """Get element with stored locator."""
        if not instance:
            raise AttributeError("This descriptor is for instances only!")
        return self.prepare_element(instance)

    def prepare_element(self, instance: WebView) -> XPathElement:
        """Init and cache element in instance.

        Initiate element only once, and then store it in an instance and
        return it each subsequent time. This is to avoid calling
        `wait_until_visible` multiple times in the init of component.

        If the instance doesn't already have an attribute to store cache, it
        will be set.

        If descriptor is used for ``Component`` and
        ``self.is_relative_locator=True``, element will be found by sum of
        ``base_locator`` of that component and passed locator of descriptor.

        If descriptor is used for instance of ``Page``, then ``base_locator``
        is not needed, since element will be searched across the entire page,
        not within some component.

        """
        if not getattr(instance, self.cache_attribute_name, None):
            setattr(instance, self.cache_attribute_name, {})

        cache = getattr(instance, self.cache_attribute_name, {})
        if cached_element := cache.get(self.attribute_name):
            return cached_element

        from pomcorn import Component

        if self.is_relative_locator and isinstance(instance, Component):
            self.locator = instance.base_locator // self.locator

        element = instance.init_element(locator=self.locator)
        cache[self.attribute_name] = element

        return element

    def __set__(self, *args, **kwargs) -> NoReturn:
        raise ValueError("You can't reset an element attribute value!")
