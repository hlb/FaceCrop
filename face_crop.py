#!/usr/bin/env python3
import os
import argparse
import cv2
import mediapipe as mp
from PIL import Image, ImageDraw


def create_circular_mask(size):
    """Create a circular mask for the image"""
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    return mask


def process_image(input_path, output_path, circular_mask=False):
    """Process a single image: detect face, crop upper body, and create transparent background"""
    # Initialize face detectors
    mp_face_detection = mp.solutions.face_detection
    haar_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    profile_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_profileface.xml"
    )

    # Read image
    img = cv2.imread(input_path)
    if img is None:
        print(f"Error: Could not read image {input_path}")
        return False

    # Keep original for final crop
    original = img.copy()
    height, width = img.shape[:2]

    # Convert BGR to RGB for MediaPipe
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Basic preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_eq = cv2.equalizeHist(gray)

    # Try MediaPipe detection first with very low confidence threshold
    face_detected = False
    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.05, model_selection=1
    ) as face_detection:
        results = face_detection.process(rgb_img)
        if results.detections:
            detection = max(results.detections, key=lambda x: x.score[0])
            if detection.score[0] > 0.1:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * width)
                y = int(bbox.ymin * height)
                w = int(bbox.width * width)
                h = int(bbox.height * height)
                face_detected = True

    # If MediaPipe fails, try Haar Cascade
    if not face_detected:
        for scale in [1.02, 1.05, 1.08]:
            faces = haar_cascade.detectMultiScale(
                gray_eq,
                scaleFactor=scale,
                minNeighbors=3,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )
            if len(faces) > 0:
                faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
                x, y, w, h = faces[0]
                face_detected = True
                break

    # If frontal detection fails, try profile face detection
    if not face_detected:
        for is_flipped in [False, True]:
            current_img = cv2.flip(gray_eq, 1) if is_flipped else gray_eq
            faces = profile_cascade.detectMultiScale(
                current_img,
                scaleFactor=1.05,
                minNeighbors=2,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )
            if len(faces) > 0:
                x, y, w, h = faces[0]
                if is_flipped:
                    x = width - x - w
                face_detected = True
                break

    if not face_detected:
        print(f"No face detected in {input_path}")
        return False

    # Calculate crop dimensions
    face_center_x = x + w // 2
    face_center_y = y + h // 2
    crop_size = int(max(w, h) * 3)
    min_head_margin = int(h * 0.5)

    # Calculate initial crop coordinates
    y1 = max(0, face_center_y - crop_size // 2)
    if (y - y1) < min_head_margin:
        y1 = max(0, y - min_head_margin)

    x1 = max(0, face_center_x - crop_size // 2)
    x2 = min(width, x1 + crop_size)
    y2 = min(height, y1 + crop_size)

    # Adjust coordinates to maintain square shape
    if x2 == width:
        x1 = max(0, width - crop_size)
    if y2 == height:
        y1 = max(0, height - crop_size)

    actual_size = min(x2 - x1, y2 - y1)
    x2 = x1 + actual_size
    y2 = y1 + actual_size

    # Create final image
    cropped = cv2.cvtColor(original[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cropped)
    rgba = pil_img.convert("RGBA")

    if circular_mask:
        mask = create_circular_mask(rgba.size)
        rgba.putalpha(mask)

    rgba.save(output_path, "PNG")
    return True


def main():
    parser = argparse.ArgumentParser(description="Crop faces from images")
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument(
        "--output", help="Output directory (required for directory input)"
    )
    parser.add_argument("--circular", action="store_true", help="Create circular mask")
    args = parser.parse_args()

    # Check if input is a file or directory
    if os.path.isfile(args.input):
        # Single file processing
        output_path = (
            args.output
            if args.output
            else os.path.splitext(args.input)[0] + "_cropped.png"
        )
        if process_image(args.input, output_path, args.circular):
            print(f"Successfully processed {args.input} -> {output_path}")
        else:
            print(f"Failed to process {args.input}")
    else:
        # Directory processing
        if not args.output:
            print("Error: Output directory is required when processing a directory")
            return

        if not os.path.exists(args.output):
            os.makedirs(args.output)

        success_count = 0
        total_count = 0

        for filename in os.listdir(args.input):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                input_path = os.path.join(args.input, filename)
                output_filename = os.path.splitext(filename)[0] + "_cropped.png"
                output_path = os.path.join(args.output, output_filename)

                total_count += 1
                if process_image(input_path, output_path, args.circular):
                    success_count += 1
                    print(f"Successfully processed {filename}")
                else:
                    print(f"Failed to process {filename}")

        print(
            f"\nProcessing complete: {success_count}/{total_count} images successfully processed"
        )


if __name__ == "__main__":
    main()
