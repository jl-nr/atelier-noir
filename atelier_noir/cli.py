#!/usr/bin/env python3
"""
Command-line interface for Atelier Noir.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image
from .transformations import (
    boost_contrast,
    enhance_shadows,
    apply_monochrome,
    apply_dark_theme,
    apply_cinematic_dark_theme,
    apply_noir_preset,
)
from .pipeline import process_batch


def main():
    parser = argparse.ArgumentParser(
        description='Atelier Noir - Dark-themed image transformations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Apply dark theme to a single image
  atelier-noir input.jpg -o output.jpg

  # Apply monochrome dark theme
  atelier-noir input.jpg -o output.jpg --monochrome

  # Process a batch of images
  atelier-noir --batch input_dir/ output_dir/

  # Custom contrast and shadow settings
  atelier-noir input.jpg -o output.jpg --contrast 2.0 --shadows 0.5

  # Cinematic dark look with vignette and grain
  atelier-noir input.jpg -o output.jpg --cinematic

  # Noir preset (strong contrast, moody monochrome)
  atelier-noir input.jpg -o output.jpg --noir
        """
    )

    # Input/output arguments
    parser.add_argument(
        'input',
        help='Input image file or directory (for batch mode)',
        type=str
    )

    parser.add_argument(
        '-o', '--output',
        help='Output image file or directory (required for batch mode)',
        type=str,
        default=None
    )

    # Batch processing
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process a batch of images from input directory'
    )

    # Transformation parameters
    parser.add_argument(
        '--contrast',
        type=float,
        default=1.5,
        help='Contrast enhancement factor (default: 1.5)'
    )

    parser.add_argument(
        '--shadows',
        type=float,
        default=0.7,
        help='Shadow enhancement factor, lower = darker (default: 0.7)'
    )

    parser.add_argument(
        '--monochrome',
        action='store_true',
        help='Apply monochrome filter'
    )

    parser.add_argument(
        '--monochrome-style',
        choices=['dark', 'high_contrast', 'moody'],
        default='dark',
        help='Monochrome style (default: dark)'
    )

    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing output files (batch mode only)'
    )

    # Look presets
    parser.add_argument(
        '--cinematic',
        action='store_true',
        help='Use cinematic dark theme (contrast + shadows + vignette + grain)'
    )
    parser.add_argument(
        '--no-vignette',
        action='store_true',
        help='Disable vignette (only meaningful with --cinematic)'
    )
    parser.add_argument(
        '--no-grain',
        action='store_true',
        help='Disable film grain (only meaningful with --cinematic)'
    )
    parser.add_argument(
        '--noir',
        action='store_true',
        help='Use noir preset (strong contrast, moody monochrome)'
    )

    args = parser.parse_args()

    # Batch processing mode
    if args.batch:
        if not args.output:
            print("Error: --output is required for batch processing", file=sys.stderr)
            sys.exit(1)

        print(f"Processing batch from {args.input} to {args.output}...")
        stats = process_batch(
            input_dir=args.input,
            output_dir=args.output,
            contrast_factor=args.contrast,
            shadow_factor=args.shadows,
            monochrome=args.monochrome,
            monochrome_style=args.monochrome_style,
            cinematic=args.cinematic,
            noir=args.noir,
            vignette=None if not args.cinematic else (False if args.no_vignette else True),
            grain=None if not args.cinematic else (False if args.no_grain else True),
            overwrite=args.overwrite
        )

        print(f"\nBatch processing complete:")
        print(f"  Processed: {stats['processed']}")
        print(f"  Skipped: {stats['skipped']}")
        print(f"  Errors: {stats['errors']}")

        if stats['error_files']:
            print("\nErrors:")
            for file, error in stats['error_files']:
                print(f"  {file}: {error}")

        sys.exit(0 if stats['errors'] == 0 else 1)

    # Single image processing mode
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        # Load image
        image = Image.open(input_path)

        # Apply transformations
        if args.noir:
            processed = apply_noir_preset(image)
        elif args.cinematic:
            processed = apply_cinematic_dark_theme(
                image,
                contrast_factor=args.contrast,
                shadow_factor=args.shadows,
                monochrome=args.monochrome,
                monochrome_style=args.monochrome_style,
                vignette=not args.no_vignette,
                grain=not args.no_grain,
            )
        else:
            processed = apply_dark_theme(
                image,
                contrast_factor=args.contrast,
                shadow_factor=args.shadows,
                monochrome=args.monochrome,
                monochrome_style=args.monochrome_style
            )

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            # Generate output filename
            stem = input_path.stem
            suffix = input_path.suffix
            output_path = input_path.parent / f"{stem}_dark{suffix}"

        # Save processed image
        processed.save(output_path)
        print(f"Processed image saved to: {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
