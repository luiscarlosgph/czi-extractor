"""
@brief   Extract all the slices of a z-stack in CZI format into a folder of 
         PNG images.
@author  Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).
@date    5 Oct 2023.
"""
import os
import czifile
import PIL.Image
import argparse
import numpy as np
import skimage.restoration


def hex_to_dec(hex_color: str):
    """
    @brief  Convert hex color to RGBA.
    
    @param[in]  hex_color  String containing #AARRGGBB.

    @returns  a tuple of red, green blue, alpha. All of them integers [0, 255].
    """
    # Remove the "#" if present in the input string
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    # Extract individual components (RR, GG, BB, AA) from the hex string
    alpha = int(hex_color[0:2], 16)
    red = int(hex_color[2:4], 16)
    green = int(hex_color[4:6], 16)
    blue = int(hex_color[6:8], 16)

    return red, green, blue, alpha


def save_mip(output_mip_path: str, z_stack: np.ndarray, red: int, green: int, 
             blue: int):
    """
    @brief  Save the maximum intensity projection (MIP) of the provided stack 
            to file.

    @param[in]  output_mip_path  Path where the MIP will be saved.
    @param[in]  z_stack          Image stack, shape (Z, H, W).
    @param[in]  red              The projection is a grayscale image, this
                                 is the red intensity equivalent to 255 in the
                                 grayscale MIP image. 
                                 Provided for visualization purposes.
    @param[in]  green            Green intensity corresponding to 255 in the
                                 grayscale MIP.
    @param[in]  blue             Blue intensity corresponding to 255 in the
                                 grayscale MIP.
    @returns nothing.
    """
    # Compute maximum intensity projection (MIP)
    mip_gray = np.max(z_stack, axis=0)

    # Convert MIP to the color provided for visualization purposes
    mip_rgb = np.stack([mip_gray.astype(np.float32) / 255.] * 3, axis=-1)
    mip_rgb[:, :, 0] *= red 
    mip_rgb[:, :, 1] *= green
    mip_rgb[:, :, 2] *= blue 
    mip_rgb = np.clip(np.round(mip_rgb).astype(np.uint8), 0, 255)

    # Save MIP image
    mip_im = PIL.Image.fromarray(mip_rgb)
    mip_im.save(output_mip_path)


def save_aip(output_aip_path: str, z_stack: np.ndarray, red: int, green: int, 
             blue: int):
    """
    @brief  Save the average intensity projection (AIP) of the provided stack 
            to file.

    @param[in]  output_aip_path  Path where the AIP will be saved.
    @param[in]  z_stack          Image stack, shape (Z, H, W).
    @param[in]  red              The projection is a grayscale image, this
                                 is the red intensity equivalent to 255 in the
                                 grayscale MIP image. 
                                 Provided for visualization purposes.
    @param[in]  green            Green intensity corresponding to 255 in the
                                 grayscale MIP.
    @param[in]  blue             Blue intensity corresponding to 255 in the
                                 grayscale MIP.
    @returns nothing.
    """
    # Compute average intensity projection (AIP)
    aip_gray = np.average(z_stack, axis=0)

    # Convert AIP to the color provided for visualization purposes 
    aip_rgb = np.stack([aip_gray.astype(np.float32) / 255.] * 3, axis=-1)
    aip_rgb[:, :, 0] *= red 
    aip_rgb[:, :, 1] *= green
    aip_rgb[:, :, 2] *= blue 
    aip_rgb = np.clip(np.round(aip_rgb).astype(np.uint8), 0, 255)
    aip_im = PIL.Image.fromarray(aip_rgb)
    aip_im.save(output_aip_path)


def convert_czi_to_png(input_czi_path: str, output_dir: str):
    """
    @brief  Function that extracts the slices of the stack and saves them as
            PNG images. It also saves the MIP and the AIP.

    @param[in]  input_czi_path  Path to the input file contaiing the stack.
    @param[in]  output_dir      Path to the output directory where the PNGs
                                will be saved.

    @returns  nothing.
    """
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
        
        # Save maximum intensity projection
        output_mip_path = os.path.join(output_dir, f"{fname}_color_{color_name}_mip.png")
        save_mip(output_mip_path, czi_data[c], red, green, blue)
        
        # Save average intensity projection
        output_aip_path = os.path.join(output_dir, f"{fname}_color_{color_name}_aip.png")
        save_aip(output_aip_path, czi_data[c], red, green, blue)

        # Loop over the z-stack saving the slices
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

            # Convert the slice data to a PNG image using Pillow
            im = PIL.Image.fromarray(im_rgb)
            im.save(output_png_path)


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
    print("[INFO] Converting all the stack slices to PNG...")
    convert_czi_to_png(args.input, args.output)
    print("[INFO] Conversion complete. PNG images saved in the output folder.")


if __name__ == "__main__":
    main()
