# Image to Line Art Converter

A web application that converts uploaded images into artistic line art SVG drawings using a combination of Python and Rust processing.

## Features

- Image preprocessing with background removal
- Configurable contrast settings 
- Adjustable path length for line art generation
- Outputs SVG vector graphics
- Web interface for easy usage

## Attribution

The Rust image processing code is adapted from [ImageToLines by RandomGamingDev](https://github.com/RandomGamingDev/ImageToLines).
Thank you for that.

## Requirements

- Python 3.x
- Rust/Cargo
- Required Python packages:
```sh
pip install -r requirements.txt
```

## Setup

1. Install dependencies:
```sh
pip install -r requirements.txt
cargo build
```

2. Ensure these directories exist:

   - nobg - For processed images without background
   - images/output - For generated SVG files

## Usage

1. Start the server:
```sh
python server.py
```

2. Access the web interface at `http://localhost:5000`

3. Upload an image and adjust parameters:
   - **Contrast**: Controls the threshold for line generation (default: 12)
   - **Path Length**: Minimum length for SVG path segments (default: 25)

4. The server will:
   - Crop and resize the image to 512x512
   - Remove the background
   - Process the image through the Rust engine
   - Generate an SVG line art drawing
   - Return a downloadable SVG file

## Project Structure

   - server.py - Flask web server handling image upload and processing
   - preprocessing.py - Image preparation and background removal
   - main.rs - Rust-based image processing core (adapted from ImageToLines)
   - postprocessing.py - SVG generation and optimization

## License

See LICENSE.md for details.