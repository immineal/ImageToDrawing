from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import os
import hashlib
import subprocess

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = './images'
NOBG_FOLDER = './images/nobg'
OUTPUT_FOLDER = './output'

# Ensure required directories exist
for folder in [UPLOAD_FOLDER, NOBG_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def crop_to_square(image):
    width, height = image.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    return image.crop((left, top, right, bottom))

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image uploaded'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        # Get parameters
        contrast = request.form.get('contrast', '12')
        path_length = request.form.get('pathLength', '25')
        
        # Generate unique filename based on file content
        file_content = file.read()
        unique_id = hashlib.sha256(file_content).hexdigest()
        file.seek(0)  # Reset file pointer to beginning after reading
        filename = secure_filename(f"{unique_id}.jpg")
        
        # Save and process original image
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        nobg_path = os.path.join(NOBG_FOLDER, f"{unique_id}_nobg.png")
        
        # Open, crop to square, resize, and save image
        image = Image.open(file.stream)
        image = crop_to_square(image)
        image = image.resize((512, 512), Image.Resampling.LANCZOS)
        image.save(image_path, "JPEG", quality=95)
        
        # Run preprocessing
        subprocess.run([
            'python3', 'preprocessing.py',
            image_path,
            nobg_path
        ], check=True)
        
        # Update img_name.txt
        with open('img_name.txt', 'w') as f:
            f.write(f"./images/nobg/{unique_id}_nobg.png")
        
        # Update pixel_drawing_settings.txt
        with open('pixel_drawing_settings.txt', 'w') as f:
            f.write(contrast)
        
        # Run cargo
        subprocess.run(['cargo', 'run'], check=True)
        
        # Run postprocessing
        output_path = os.path.join(OUTPUT_FOLDER, f"{unique_id}.svg")
        subprocess.run([
            'python3', 'postprocessing.py',
            'output.jpeg',
            output_path,
            '--min-length', path_length
        ], check=True)
        
        return jsonify({
            'success': True,
            'message': 'Image processed successfully',
            'output_file': f"{unique_id}.svg"  # Just return filename, not full path
        })
        
    except subprocess.CalledProcessError as e:
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/output/<filename>')
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)