from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn, overload

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

    @overload
    def __init__(
        self,
        locator: locators.XPathLocator | None = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        *,
        relative_locator: locators.XPathLocator | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        locator: locators.XPathLocator | None = None,
        *,
        relative_locator: locators.XPathLocator | None = None,
    ) -> None:
        """Initialize descriptor.

        Use `relative_locator` if you need to include `base_locator` of
        instance, otherwise use `locator`.

        If descriptor is used for instance of ``Page``, then
        ``relative_locator`` is not needed, since element will be searched
        across the entire page, not within some component.

        """
        self.locator = locator
        self.relative_locator = relative_locator

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

        """
        if not getattr(instance, self.cache_attribute_name, None):
            setattr(instance, self.cache_attribute_name, {})

        cache = getattr(instance, self.cache_attribute_name, {})
        if cached_element := cache.get(self.attribute_name):
            return cached_element

        element = instance.init_element(
            locator=self._prepare_locator(instance),
        )
        cache[self.attribute_name] = element

        return element

    def _prepare_locator(self, instance: WebView) -> locators.XPathLocator:
        """Prepare a locator by arguments.

        Check that only one locator argument is passed, or none.
        If only `relative_locator` was passed, `base_locator` of instance will
        be added to specified in descriptor arguments. If only `locator` was
        passed, it will return only specified one.

        Raises:
            ValueError: If both arguments were passed or neither or
                ``relative_locator`` used not in ``Component``.

        """
        if self.relative_locator and self.locator:
            raise ValueError(
                "You need to pass only one of the arguments: "
                "`locator` or `relative_locator`.",
            )

        if not self.relative_locator:
            if not self.locator:
                raise ValueError(
                    "You need to pass one of the arguments: "
                    "`locator` or `relative_locator`.",
                )
            return self.locator

        from pomcorn import Component

        if self.relative_locator and isinstance(instance, Component):
            return instance.base_locator // self.relative_locator

        raise ValueError(
            f"`relative_locator` should be used only if descriptor used in "
            f"component. `{instance}` is not a component.",
        )

    def __set__(self, *args, **kwargs) -> NoReturn:
        raise ValueError("You can't reset an element attribute value!")
