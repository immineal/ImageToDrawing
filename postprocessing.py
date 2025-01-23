#!/usr/bin/env python3
import cv2
import numpy as np
from skimage.morphology import skeletonize
from skimage.util import img_as_ubyte
import svgwrite
import argparse
from pathlib import Path

def detect_and_export_centerlines(image_path, output_path, min_length=25, threshold=127, smoothness=1.0):
    # Read and process image
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Convert to binary
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
    skeleton = skeletonize(binary / 255)
    skeleton_image = img_as_ubyte(skeleton)
    
    # Find contours
    contours, _ = cv2.findContours(skeleton_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create SVG
    dwg = svgwrite.Drawing(output_path, size=image.shape[::-1])
    dwg.viewbox(0, 0, image.shape[1], image.shape[0])
    group = dwg.g(stroke='black', stroke_width=1, fill='none')

    # Process contours
    for contour in contours:
        if cv2.arcLength(contour, False) < min_length:
            continue
        
        # Simplify contour with approximation
        epsilon = smoothness
        approx = cv2.approxPolyDP(contour, epsilon, closed=False)
        points = approx.reshape(-1, 2)
        
        if len(points) < 2:
            continue

        # Calculate tangents for each point
        tangents = []
        for i in range(len(points)):
            if i == 0:
                tangent = points[1] - points[0] if len(points) > 1 else np.array([0.0, 0.0])
            elif i == len(points)-1:
                tangent = points[-1] - points[-2]
            else:
                prev_dir = points[i] - points[i-1]
                next_dir = points[i+1] - points[i]
                tangent = (prev_dir + next_dir) / 2.0
            tangents.append(tangent)

        # Build SVG path with cubic Bezier curves
        path_data = f"M {points[0][0]:.2f},{points[0][1]:.2f}"
        for i in range(len(points)-1):
            current = points[i]
            next_p = points[i+1]
            distance = np.linalg.norm(next_p - current)
            if distance == 0:
                continue
            
            # Calculate control points using tangents
            k = distance * 0.25  # Adjust this factor to control curve tightness
            cp1 = current + tangents[i] * k
            cp2 = next_p - tangents[i+1] * k
            
            path_data += f" C {cp1[0]:.2f},{cp1[1]:.2f} {cp2[0]:.2f},{cp2[1]:.2f} {next_p[0]:.2f},{next_p[1]:.2f}"
        
        group.add(dwg.path(d=path_data))
    
    dwg.add(group)
    dwg.save(pretty=True)

def main():
    parser = argparse.ArgumentParser(description='Convert image lines to SVG centerlines')
    parser.add_argument('input', type=Path, help='Input image path')
    parser.add_argument('output', type=Path, help='Output SVG path')
    parser.add_argument('--min-length', type=float, default=25, help='Minimum path length (default: 25)')
    parser.add_argument('--threshold', type=int, default=127, help='Binary threshold (0-255, default: 127)')
    parser.add_argument('--smoothness', type=float, default=0.2, 
                        help='Smoothing factor for contour approximation (higher = smoother, default: 0.4)')
    
    args = parser.parse_args()
    
    try:
        detect_and_export_centerlines(args.input, args.output, args.min_length, args.threshold, args.smoothness)
        print(f"Successfully saved SVG to: {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()