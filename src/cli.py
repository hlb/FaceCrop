import os
import argparse
import sys
from .processor import ImageProcessor

def main():
    parser = argparse.ArgumentParser(description="Crop faces from images")
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument(
        "--output", help="Output directory (required for directory input)"
    )
    parser.add_argument("--circular", action="store_true", help="Create circular mask")
    args = parser.parse_args()

    processor = ImageProcessor()

    # Check if input is a file or directory
    if os.path.isfile(args.input):
        # Single file processing
        output_path = (
            args.output
            if args.output
            else os.path.splitext(args.input)[0] + "_cropped.png"
        )
        if processor.process_image(args.input, output_path, args.circular):
            print(f"Successfully processed {args.input} -> {output_path}")
            sys.exit(0)
        else:
            print(f"Failed to process {args.input}")
            sys.exit(1)
    else:
        # Directory processing
        if not args.output:
            print("Error: Output directory is required when processing a directory")
            sys.exit(1)

        if not os.path.exists(args.output):
            os.makedirs(args.output)

        success_count = 0
        total_count = 0

        for filename in os.listdir(args.input):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                input_path = os.path.join(args.input, filename)
                output_filename = os.path.splitext(filename)[0] + "_cropped.png"
                output_path = os.path.join(args.output, output_filename)

                total_count += 1
                if processor.process_image(input_path, output_path, args.circular):
                    success_count += 1
                    print(f"Successfully processed {filename}")
                else:
                    print(f"Failed to process {filename}")

        if total_count == 0:
            print("No image files found in directory")
            sys.exit(1)
        elif success_count == 0:
            print("Failed to process any images")
            sys.exit(1)
        else:
            print(f"Successfully processed {success_count} out of {total_count} images")
            sys.exit(0)

if __name__ == "__main__":
    main()
