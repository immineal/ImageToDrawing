import argparse
from PIL import Image
from rembg import remove

def remove_background(input_path, output_path):
    # Open the input image
    input_image = Image.open(input_path)
    
    # Remove the background
    output_image = remove(input_image)
    
    # Save the output image (use PNG to preserve transparency)
    output_image.save(output_path)
    print(f"Background removed! Saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove the background from an image.')
    parser.add_argument('input', help='Path to the input image (e.g., input.jpg)')
    parser.add_argument('output', help='Path to save the output image (e.g., output.png)')
    args = parser.parse_args()
    
    remove_background(args.input, args.output)