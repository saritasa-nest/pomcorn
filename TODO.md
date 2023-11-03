# TODO list

## GitHub

* Add PR/Issue templates

## In future

* Add arguments for `ButtonWithTextLocator` to choice `a` or `button` tag
* Provide ability to specify base locator and item locator as class attributes like:

```python
base_locator = locators.PropertyLocator(
    prop="aria-label",
    value="Search results",
)
relative_item_locator = locators.ClassLocator(
    class_name="package-snippet",
    container="a",
)
```

* Add short comparison with other POM implementations
