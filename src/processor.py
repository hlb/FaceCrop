import cv2
from PIL import Image
from .detector import FaceDetector
from .utils import create_circular_mask


class ImageProcessor:
    def __init__(self):
        self.detector = FaceDetector()

    def process_image(self, input_path, output_path, circular_mask=False, strict=False):
        """Process a single image: detect face, crop upper body, and create transparent background"""
        # Read image
        img = cv2.imread(input_path)
        if img is None:
            print(f"Error: Could not read image {input_path}")
            return False

        # Keep original for final crop
        original = img.copy()
        height, width = img.shape[:2]

        # Detect face
        face_bbox = self.detector.detect_face(img, strict=strict)
        if not face_bbox:
            print(f"No face detected in {input_path}")
            return False

        x, y, w, h = face_bbox

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
