"""
Batch processing pipeline for image transformations.
"""

import os
from pathlib import Path
from PIL import Image
from .transformations import apply_dark_theme


def process_batch(
    input_dir,
    output_dir,
    contrast_factor=1.5,
    shadow_factor=0.7,
    monochrome=False,
    monochrome_style='dark',
    extensions=None,
    overwrite=False
):
    """
    Process a batch of images with dark theme transformations.

    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save processed images
        contrast_factor: Contrast enhancement factor
        shadow_factor: Shadow enhancement factor
        monochrome: Whether to apply monochrome filter
        monochrome_style: Style of monochrome conversion
        extensions: List of file extensions to process (default: ['.jpg', '.jpeg', '.png', '.bmp'])
        overwrite: Whether to overwrite existing files

    Returns:
        dict with processing statistics
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all image files
    image_files = []
    for ext in extensions:
        image_files.extend(input_path.glob(f'*{ext}'))
        image_files.extend(input_path.glob(f'*{ext.upper()}'))

    stats = {
        'processed': 0,
        'skipped': 0,
        'errors': 0,
        'error_files': []
    }

    for img_path in image_files:
        output_file = output_path / img_path.name

        # Skip if file exists and overwrite is False
        if output_file.exists() and not overwrite:
            stats['skipped'] += 1
            continue

        try:
            # Load image
            image = Image.open(img_path)

            # Apply transformations
            processed = apply_dark_theme(
                image,
                contrast_factor=contrast_factor,
                shadow_factor=shadow_factor,
                monochrome=monochrome,
                monochrome_style=monochrome_style
            )

            # Save processed image
            processed.save(output_file)
            stats['processed'] += 1

        except Exception as e:
            stats['errors'] += 1
            stats['error_files'].append((str(img_path), str(e)))

    return stats
