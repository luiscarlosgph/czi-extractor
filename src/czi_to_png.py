"""
@brief   Convert a folder of CZI images containing z-stacks into a folder of PNG images.
@author  Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).
@date    5 Oct 2023.
"""
import os
import czifile
import pillow
import argparse


def convert_czi_to_png(input_dir, output_dir):
    # Create the output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # List all files in the input folder
    czi_files = [f for f in os.listdir(input_dir) if f.endswith('.czi')]

    # Loop through each CZI file in the input folder
    for czi_file in czi_files:
        # Construct the full path of the input CZI file
        input_czi_path = os.path.join(input_dir, czi_file)

        # Open the CZI file
        with czifile.CziFile(input_czi_path) as czi:
            # Read the CZI data
            czi_data = czi.asarray()

        # Loop through each slice and save it as a PNG image
        for i, slice_data in enumerate(czi_data):
            # Construct the output PNG file path with slice number suffix
            output_png_path = os.path.join(output_dir, f"{os.path.splitext(czi_file)[0]}_slice_{i}.png")

            # Convert the slice data to a PNG image using Pillow
            img = pillow.Image.fromarray(slice_data)
            img.save(output_png_path)


def main():
    # Read command line arguments
    parser = argparse.ArgumentParser(description="Convert CZI images to PNG format with slice number suffixes.")
    parser.add_argument("--input-dir", required=True, help="Path to the input directory containing CZI images.")
    parser.add_argument("--output-dir", required=True, help="Path to the output directory for saving PNG images.")
    args = parser.parse_args()

    # Perform the conversion
    convert_czi_to_png(args.input_dir, args.output_dir)

    print("Conversion complete. PNG images saved in the output folder.")


if __name__ == "__main__":
    main()
