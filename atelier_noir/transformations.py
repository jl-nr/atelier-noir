"""
Core image transformation functions for dark-themed effects.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageOps


def boost_contrast(image, factor=1.5):
    """
    Boost the contrast of an image.

    Args:
        image: PIL Image object
        factor: Contrast enhancement factor (default: 1.5)

    Returns:
        PIL Image with enhanced contrast
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def enhance_shadows(image, shadow_factor=0.7, highlight_factor=1.0):
    """
    Enhance shadows while preserving highlights.

    Args:
        image: PIL Image object
        shadow_factor: Factor to darken shadows (0.0-1.0, lower = darker)
        highlight_factor: Factor for highlights (default: 1.0 = no change)

    Returns:
        PIL Image with enhanced shadows
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert to numpy array
    img_array = np.array(image, dtype=np.float32)

    # Normalize to 0-1 range
    img_array = img_array / 255.0

    # Calculate luminance
    luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]

    # Create mask for shadows (low luminance areas)
    shadow_mask = np.clip(1.0 - luminance, 0, 1)

    # Apply shadow enhancement
    for channel in range(3):
        img_array[:, :, channel] = img_array[:, :, channel] * (1 - shadow_mask * (1 - shadow_factor))

    # Apply highlight preservation
    highlight_mask = np.clip(luminance - 0.5, 0, 1) * 2
    for channel in range(3):
        img_array[:, :, channel] = img_array[:, :, channel] * (1 - highlight_mask * (1 - highlight_factor))

    # Convert back to 0-255 range and to PIL Image
    img_array = np.clip(img_array * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(img_array)


def apply_monochrome(image, style='dark'):
    """
    Apply monochrome filter with dark theme.

    Args:
        image: PIL Image object
        style: Style of monochrome conversion ('dark', 'high_contrast', 'moody')

    Returns:
        PIL Image in grayscale with dark theme
    """
    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    if style == 'dark':
        # Darken the image
        enhancer = ImageEnhance.Brightness(gray)
        gray = enhancer.enhance(0.7)
        # Increase contrast
        enhancer = ImageEnhance.Contrast(gray)
        gray = enhancer.enhance(1.3)
    elif style == 'high_contrast':
        # High contrast monochrome
        enhancer = ImageEnhance.Contrast(gray)
        gray = enhancer.enhance(2.0)
        enhancer = ImageEnhance.Brightness(gray)
        gray = enhancer.enhance(0.8)
    elif style == 'moody':
        # Moody, darker monochrome
        enhancer = ImageEnhance.Brightness(gray)
        gray = enhancer.enhance(0.6)
        enhancer = ImageEnhance.Contrast(gray)
        gray = enhancer.enhance(1.5)

    # Convert back to RGB for consistency
    return gray.convert('RGB')


def apply_dark_theme(image, contrast_factor=1.5, shadow_factor=0.7, monochrome=False, monochrome_style='dark'):
    """
    Apply a complete dark theme transformation.

    Args:
        image: PIL Image object
        contrast_factor: Contrast enhancement factor
        shadow_factor: Shadow enhancement factor
        monochrome: Whether to apply monochrome filter
        monochrome_style: Style of monochrome conversion

    Returns:
        PIL Image with dark theme applied
    """
    result = image.copy()

    # Apply contrast boost
    result = boost_contrast(result, contrast_factor)

    # Enhance shadows
    result = enhance_shadows(result, shadow_factor)

    # Optionally apply monochrome
    if monochrome:
        result = apply_monochrome(result, monochrome_style)

    return result
