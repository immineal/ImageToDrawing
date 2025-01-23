# Image to Line Art Converter

A web application that converts uploaded images into artistic line art SVG drawings and G-code output using a combination of Python and Rust processing.

## Features

- Image preprocessing with background removal 
- Configurable contrast settings for line detection
- Adjustable path length for line art optimization
- Outputs both SVG vector graphics and G-code
- Web interface with live preview
- Custom G-code tool on/off commands
- Batch processing support

## Attribution

The core functionality is built upon:
- [ImageToLines by RandomGamingDev](https://github.com/RandomGamingDev/ImageToLines) - Rust image processing
- [svg2gcode by sameer](https://github.com/sameer/svg2gcode) - G-code generation

## Requirements

- Python 3.x
- Rust/Cargo

## Setup

Install dependencies:
```sh
pip install -r requirements.txt
cargo build --release
```

## Usage

1. Start the server:
```sh
python server.py
```

2. Access the web interface at http://localhost:5000

3. Upload an image and configure settings:

   - Contrast Threshold: Controls line detection sensitivity (lower is more sensitive) (0-50)
   - Minimum Path Length: Filters short path segments (0-150)
   - Remove Background: Toggle background removal
   - Tool On Command (default: M3)
   - Tool Off Command (default: M5)
   - Press the Button to Process the Image! (**First time running might take a few minutes to build the gcode generator and download the model for removing the background**)

## License

See LICENSE.md for details.
