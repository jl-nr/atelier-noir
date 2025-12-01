"""
Atelier Noir - Dark-themed image transformations for stylized preprocessing.
"""

from .transformations import (
    boost_contrast,
    enhance_shadows,
    apply_monochrome,
    apply_dark_theme,
    add_vignette,
    add_film_grain,
    apply_cinematic_dark_theme,
    apply_noir_preset,
    apply_dramatic_preset,
)

__version__ = "0.1.0"
__all__ = [
    "boost_contrast",
    "enhance_shadows",
    "apply_monochrome",
    "apply_dark_theme",
    "add_vignette",
    "add_film_grain",
    "apply_cinematic_dark_theme",
    "apply_noir_preset",
    "apply_dramatic_preset",
]
