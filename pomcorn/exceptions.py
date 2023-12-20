class ElementIsNotClickableError(TimeoutError):
    """Raised when element is not clickable when it should be."""


class UrlDoesNotContainError(TimeoutError):
    """Raised when url does not contain needed substring when it should."""


class UrlDoesContainError(TimeoutError):
    """Raised when url does contain needed substring when it shouldn't."""


class UrlDidNotChangedError(TimeoutError):
    """Raised when url didn't changed when it should."""


class ElementIsNotVisibleError(TimeoutError):
    """Raised when element is not visible when it should be."""


class ElementIsNotInvisibleError(TimeoutError):
    """Raised when element is not invisible when it should be."""


class TextIsNotInElementError(TimeoutError):
    """Raised when element doesn't have required when it should have."""


class AttributeDoesNotContainError(TimeoutError):
    """Raised when attribute doesn't contain needed value when it should."""


class FailedFormSubmissionError(Exception):
    """Raised when there an error on form submission."""


class PageDidNotLoadedError(Exception):
    """Raised when page load timeout has expired."""
