"""
Core image transformation functions for dark-themed effects.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter


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


def add_vignette(image, strength=0.6, softness=0.5):
    """
    Add a cinematic vignette effect around the edges.

    Args:
        image: PIL Image object
        strength: How dark the edges become (0-1, higher = darker)
        softness: How soft the transition is (0-1, higher = softer)

    Returns:
        PIL Image with vignette applied
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

    width, height = image.size
    center_x, center_y = width / 2, height / 2

    # Create radial gradient mask using numpy
    y, x = np.ogrid[0:height, 0:width]
    dist_from_center = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    max_dist = np.sqrt(center_x**2 + center_y**2)
    radial = dist_from_center / max_dist

    # Soften edges
    softness = np.clip(softness, 0.01, 1.0)
    radial = radial**(1.0 / softness)
    radial = np.clip(radial, 0.0, 1.0)

    # Strength controls how dark edges get
    strength = np.clip(strength, 0.0, 1.0)
    vignette_mask = 1.0 - radial * strength
    vignette_mask = vignette_mask[..., np.newaxis]  # shape (h, w, 1)

    img_array = np.array(image, dtype=np.float32) / 255.0
    img_array *= vignette_mask
    img_array = np.clip(img_array * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(img_array)


def add_film_grain(image, intensity=0.2, monochrome=True):
    """
    Overlay subtle film-style grain on the image.

    Args:
        image: PIL Image object
        intensity: Grain intensity (0-1, typical 0.1-0.4)
        monochrome: If True, use monochrome grain; otherwise colored

    Returns:
        PIL Image with grain applied
    """
    if intensity <= 0:
        return image

    if image.mode != "RGB":
        image = image.convert("RGB")

    width, height = image.size
    base = np.array(image, dtype=np.float32) / 255.0

    # Generate noise
    if monochrome:
        noise = np.random.normal(loc=0.0, scale=1.0, size=(height, width, 1))
        noise = np.repeat(noise, 3, axis=2)
    else:
        noise = np.random.normal(loc=0.0, scale=1.0, size=(height, width, 3))

    # Normalize noise to 0-1 and center around 0
    noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-8)
    noise = (noise - 0.5) * 2.0  # [-1, 1]

    grain = base + noise * intensity * 0.3
    grain = np.clip(grain, 0.0, 1.0)
    grain = (grain * 255.0).astype(np.uint8)
    return Image.fromarray(grain)


def apply_cinematic_dark_theme(
    image,
    contrast_factor=1.6,
    shadow_factor=0.65,
    monochrome=False,
    monochrome_style="moody",
    vignette=True,
    vignette_strength=0.6,
    vignette_softness=0.6,
    grain=True,
    grain_intensity=0.22,
):
    """
    Apply an opinionated, cinematic dark look in a single call.

    This stacks the classic Atelier Noir pipeline (contrast + shadows + optional
    monochrome) with a vignette and subtle film grain.

    Args mirror `apply_dark_theme` with extra vignette and grain controls.
    """
    result = apply_dark_theme(
        image,
        contrast_factor=contrast_factor,
        shadow_factor=shadow_factor,
        monochrome=monochrome,
        monochrome_style=monochrome_style,
    )

    if vignette:
        result = add_vignette(
            result, strength=vignette_strength, softness=vignette_softness
        )

    if grain:
        result = add_film_grain(result, intensity=grain_intensity, monochrome=True)

    return result
