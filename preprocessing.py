import argparse
from PIL import Image
from rembg import remove

def remove_background(input_path, output_path, remove_bg):
    if remove_bg:
        # Remove background if flag is set
        input_image = Image.open(input_path)
        output_image = remove(input_image)
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