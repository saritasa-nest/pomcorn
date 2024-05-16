from typing import TypeAlias

from pomcorn import Component

from .base_page import PyPIPage

# In order not to specify generics every time, it's comfy to create your own
# type alias for `Component`.
PyPIComponent: TypeAlias = Component[PyPIPage]
