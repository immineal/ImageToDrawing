import argparse
from PIL import Image
from rembg import remove
import os

def remove_background(input_path, output_path, remove_bg):
    # Convert PNG to JPG if it is a PNG
    if input_path.lower().endswith('.png'):
        input_image = Image.open(input_path)
        rgb_image = input_image.convert('RGB')
        input_path = input_path.replace('.png', '.jpg')
        rgb_image.save(input_path)
        print(f"Converted PNG to JPG: {input_path}")

    if remove_bg:
        # Remove background if flag is set
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        
        # Always composite onto white background and convert to RGB
        if output_image.mode == 'RGBA':
            # Create a white background image
            background = Image.new('RGB', output_image.size, (255, 255, 255))
            # Paste the RGBA image using the alpha channel as mask
            background.paste(output_image, mask=output_image.split()[3])
            output_image = background
        else:
            # Ensure the image is in RGB mode
            output_image = output_image.convert('RGB')
        
        output_image.save(output_path)
        print(f"Background removed! Saved to {output_path}")
    else:
        # Just copy the image if flag not set
        Image.open(input_path).save(output_path)
        print(f"Copied original image to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process image with optional background removal')
    parser.add_argument('input', help='Path to input image')
    parser.add_argument('output', help='Path to output image')
    parser.add_argument('--remove-bg', action='store_true', 
                      help='Enable background removal (default: copy image)')
    args = parser.parse_args()
    
    remove_background(args.input, args.output, args.remove_bg)