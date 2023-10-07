"""
@brief   Extract all the slices of a z-stack in CZI format into a folder of PNG images.
@author  Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).
@date    5 Oct 2023.
"""
import os
import czifile
import PIL.Image
import argparse
import numpy as np


def hex_to_dec(hex_color):
    # Remove the "#" if present in the input string
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    # Extract individual components (RR, GG, BB, AA) from the hex string
    alpha = int(hex_color[0:2], 16)
    red = int(hex_color[2:4], 16)
    green = int(hex_color[4:6], 16)
    blue = int(hex_color[6:8], 16)

    return red, green, blue, alpha


def convert_czi_to_png(input_czi_path, output_dir):
    # Create the output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get z-stack image with shape (C, Z, H, W)
    czi_data = np.squeeze(czifile.imread(input_czi_path)[0][0], axis=-1)

    # Get metadata
    metadata = czifile.CziFile(input_czi_path).metadata(raw=False)

    # Loop through each slice and save it as a PNG image
    fname = os.path.splitext(os.path.basename(input_czi_path))[0]
    for c in range(czi_data.shape[0]):
        # Get the color of the channel
        red, green, blue, alpha = hex_to_dec(metadata['ImageDocument']['Metadata']['DisplaySetting']['Channels']['Channel'][c]['Color'])
        color_name = metadata['ImageDocument']['Metadata']['DisplaySetting']['Channels']['Channel'][c]['Name']

        # Loop over the z-stack
        max_intensity_proj = None
        for z in range(czi_data.shape[1]):
            # Construct the output PNG file path with slice number suffix
            output_png_path = os.path.join(output_dir, f"{fname}_color_{color_name}_slice_{z}.png")
            
            # Get image for the current color channel and stack depth
            im_gray = czi_data[c][z].astype(np.float32) / 255.
            im_rgb = np.stack([im_gray] * 3, axis=-1)
            im_rgb[:, :, 0] *= red 
            im_rgb[:, :, 1] *= green
            im_rgb[:, :, 2] *= blue 
            im_rgb = np.clip(np.round(im_rgb).astype(np.uint8), 0, 255)

            # Compute maximum intensity projection
            if max_intensity_proj is None:
                max_intensity_proj = im_rgb
            else:
                max_intensity_proj = np.maximum(max_intensity_proj, im_rgb)

            # Convert the slice data to a PNG image using Pillow
            im = PIL.Image.fromarray(im_rgb)
            im.save(output_png_path)

        # Save maximum intensity projection
        output_mip_path = os.path.join(output_dir, f"{fname}_color_{color_name}_mip.png")
        max_intensity_proj_im = PIL.Image.fromarray(max_intensity_proj)
        max_intensity_proj_im.save(output_mip_path)

def parse_cmdline():
    # Read command line arguments
    parser = argparse.ArgumentParser(description="Convert CZI images to PNG format with slice number suffixes.")
    parser.add_argument("--input", required=True, help="Path to the input directory containing CZI images.")
    parser.add_argument("--output", required=True, help="Path to the output directory for saving PNG images.")
    args = parser.parse_args()
    
    # Sanity check: make sure that output folder does not exist
    if os.path.exists(args.output) and os.path.isdir(args.output):  
        raise RuntimeError("[ERROR] The output directory already exists. Provide an output path that does not exist.")
    return args


def main():
    # Parse command line parameters
    args = parse_cmdline()    

    # Perform the conversion
    convert_czi_to_png(args.input, args.output)

    print("[INFO] Conversion complete. PNG images saved in the output folder.")


if __name__ == "__main__":
    main()
