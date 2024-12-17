#!/usr/bin/env python3
import os
import argparse
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image, ImageDraw

def create_circular_mask(size):
    """Create a circular mask for the image"""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return mask

def process_image(input_path, output_path, circular_mask=False):
    """Process a single image: detect face, crop upper body, and create transparent background"""
    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read image {input_path}")
        return False
    
    # Convert BGR to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width = img.shape[:2]
    
    # Detect face
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(rgb_img)
        
        if not results.detections:
            print(f"No face detected in {input_path}")
            return False
        
        # Get the first detected face
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        
        # Convert relative coordinates to absolute
        x = int(bbox.xmin * width)
        y = int(bbox.ymin * height)
        w = int(bbox.width * width)
        h = int(bbox.height * height)
        
        # Calculate the center of the face
        face_center_x = x + w // 2
        face_center_y = y + h // 2
        
        # Calculate square crop size (3x face height to include upper body)
        crop_size = int(max(w, h) * 3)
        
        # Ensure the crop size is large enough to include the head
        min_head_margin = int(h * 0.5)  # Add 50% margin above head
        
        # Calculate crop coordinates ensuring square shape and head visibility
        y1 = max(0, face_center_y - crop_size // 2)
        # If top margin is not enough, adjust y1
        if (y - y1) < min_head_margin:
            y1 = max(0, y - min_head_margin)
        
        # Calculate other coordinates maintaining square shape
        x1 = max(0, face_center_x - crop_size // 2)
        x2 = min(width, x1 + crop_size)
        y2 = min(height, y1 + crop_size)
        
        # Adjust x1 if x2 is out of bounds
        if x2 == width:
            x1 = max(0, width - crop_size)
        
        # Adjust y1 if y2 is out of bounds
        if y2 == height:
            y1 = max(0, height - crop_size)
        
        # Ensure square shape by taking the minimum dimension
        actual_size = min(x2 - x1, y2 - y1)
        x2 = x1 + actual_size
        y2 = y1 + actual_size
        
        # Crop image
        cropped = rgb_img[y1:y2, x1:x2]
        
        # Convert to PIL Image
        pil_img = Image.fromarray(cropped)
        
        # Create alpha channel (transparency)
        rgba = pil_img.convert('RGBA')
        
        if circular_mask:
            # Apply circular mask
            mask = create_circular_mask(rgba.size)
            rgba.putalpha(mask)
        
        # Save the result
        rgba.save(output_path, 'PNG', quality=100)
        return True

def main():
    parser = argparse.ArgumentParser(description='Crop faces from images with transparent background')
    parser.add_argument('--input', default='.', help='Input folder path (default: current directory)')
    parser.add_argument('--output', default='results', help='Output folder path (default: ./results)')
    parser.add_argument('--circular', action='store_true', help='Apply circular mask to the output')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Supported image formats
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp')
    
    # Process all images in input directory
    processed_count = 0
    total_count = 0
    
    for filename in os.listdir(args.input):
        if filename.lower().endswith(supported_formats):
            total_count += 1
            input_path = os.path.join(args.input, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(args.output, f"{base_name}_cropped.png")
            
            print(f"Processing: {filename}")
            if process_image(input_path, output_path, args.circular):
                processed_count += 1
    
    print(f"\nProcessing complete!")
    print(f"Successfully processed {processed_count} out of {total_count} images")
    print(f"Results saved in: {os.path.abspath(args.output)}")

if __name__ == '__main__':
    main()
