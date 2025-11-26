"""
Atelier Noir - Dark-themed image transformations for stylized preprocessing.
"""

from .transformations import (
    boost_contrast,
    enhance_shadows,
    apply_monochrome,
    apply_dark_theme,
)

__version__ = "0.1.0"
__all__ = [
    "boost_contrast",
    "enhance_shadows",
    "apply_monochrome",
    "apply_dark_theme",
]
