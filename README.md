# Atelier Noir

A neat and small Python tool for applying dark-themed transformations to images: contrast boosting, shadow enhancement, monochrome filters, and a simple batch pipeline. Perfect for stylized preprocessing.

## Features

- **Contrast Boosting**: Enhance image contrast for dramatic effects
- **Shadow Enhancement**: Deepen shadows while preserving highlights
- **Monochrome Filters**: Multiple dark-themed monochrome styles
- **CLI and Library**: Use as a command-line tool or import as a Python library
- **Batch Processing**: Process entire directories of images
- **Cinematic Look**: Optional vignette and film grain preset for a moody, filmic dark theme
- **Dramatic Preset**: Bold, high-contrast preset with deep shadows for striking effects
- **Noir Preset**: One-shot strong-contrast, moody monochrome preset

## Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Usage Instructions

### Command Line Interface

#### Single Image Processing

```bash
# Basic dark theme transformation
atelier-noir input.jpg -o output.jpg

# Apply monochrome dark theme
atelier-noir input.jpg -o output.jpg --monochrome

# Custom contrast and shadow settings
atelier-noir input.jpg -o output.jpg --contrast 2.0 --shadows 0.5

# Different monochrome styles
atelier-noir input.jpg -o output.jpg --monochrome --monochrome-style moody

# Cinematic preset with vignette + grain
atelier-noir input.jpg -o output.jpg --cinematic

# Cinematic without grain
atelier-noir input.jpg -o output.jpg --cinematic --no-grain

# Dramatic preset (very high contrast, deep shadows)
atelier-noir input.jpg -o output.jpg --dramatic

# Noir preset (high contrast, moody monochrome)
atelier-noir input.jpg -o output.jpg --noir
```

#### Batch Processing

```bash
# Process all images in a directory
atelier-noir --batch input_dir/ output_dir/

# Batch with custom settings
atelier-noir --batch input_dir/ output_dir/ --contrast 1.8 --shadows 0.6 --monochrome

# Batch with cinematic preset
atelier-noir --batch input_dir/ output_dir/ --cinematic

# Batch with dramatic preset
atelier-noir --batch input_dir/ output_dir/ --dramatic

# Overwrite existing files
atelier-noir --batch input_dir/ output_dir/ --overwrite
```

### Python Library

```python
from atelier_noir import (
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
from PIL import Image

# Load an image
image = Image.open('input.jpg')

# Apply individual transformations
contrasted = boost_contrast(image, factor=1.5)
shadowed = enhance_shadows(contrasted, shadow_factor=0.7)
monochrome = apply_monochrome(shadowed, style='dark')

# Or apply complete dark theme
dark_image = apply_dark_theme(
    image,
    contrast_factor=1.5,
    shadow_factor=0.7,
    monochrome=True,
    monochrome_style='dark'
)

dark_image.save('output.jpg')

# Apply cinematic dark theme in one go
cinematic = apply_cinematic_dark_theme(
    image,
    contrast_factor=1.6,
    shadow_factor=0.65,
    monochrome=True,
    monochrome_style='moody',
)
cinematic.save('cinematic.jpg')

# Apply noir preset in one line
noir = apply_noir_preset(image)
noir.save('noir.jpg')

# Apply dramatic preset for bold, striking look
dramatic = apply_dramatic_preset(image)
dramatic.save('dramatic.jpg')
```

#### Batch Processing (Library)

```python
from atelier_noir.pipeline import process_batch

stats = process_batch(
    input_dir='input_images/',
    output_dir='output_images/',
    contrast_factor=1.5,
    shadow_factor=0.7,
    monochrome=True,
    monochrome_style='dark',
    overwrite=False
)

print(f"Processed: {stats['processed']}")
print(f"Skipped: {stats['skipped']}")
print(f"Errors: {stats['errors']}")
```

## Parameters

Following parameters are supported:

- `--contrast`: Contrast enhancement factor (default: 1.5)
- `--shadows`: Shadow enhancement factor, lower = darker shadows (default: 0.7)
- `--monochrome`: Apply monochrome filter
- `--monochrome-style`: Style of monochrome conversion
  - `dark`: Darkened with increased contrast (default)
  - `high_contrast`: High contrast monochrome
  - `moody`: Moody, darker monochrome
 - `--cinematic`: Enable cinematic preset (contrast + shadows + vignette + grain)
 - `--no-vignette`: Disable vignette when `--cinematic` is used
 - `--no-grain`: Disable film grain when `--cinematic` is used
 - `--dramatic`: Enable dramatic preset (very high contrast, deep shadows)
 - `--noir`: Enable noir preset (strong contrast, moody monochrome)

## Examples

### High Contrast Dark Theme
```bash
atelier-noir photo.jpg -o dark_photo.jpg --contrast 2.0 --shadows 0.6
```

### Moody Monochrome
```bash
atelier-noir photo.jpg -o moody_photo.jpg --monochrome --monochrome-style moody
```

### Batch Processing with Custom Settings
```bash
atelier-noir --batch photos/ dark_photos/ --contrast 1.8 --shadows 0.65 --monochrome --monochrome-style high_contrast
```

## License

Apache (check [LICENSE](LICENSE) file)
