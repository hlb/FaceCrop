import unittest
import os
import cv2
import numpy as np
from PIL import Image
from src.processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.processor = ImageProcessor()
        
        # Create test directory if it doesn't exist
        cls.test_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        os.makedirs(cls.test_dir, exist_ok=True)
        
        # Create a test image with a face-like pattern
        test_img = np.zeros((300, 300, 3), dtype=np.uint8)
        # Draw a flesh-colored ellipse for face
        cv2.ellipse(test_img, (150, 150), (60, 80), 0, 0, 360, (204, 172, 147), -1)
        # Draw darker ellipses for eyes
        cv2.ellipse(test_img, (120, 130), (10, 5), 0, 0, 360, (50, 50, 50), -1)
        cv2.ellipse(test_img, (180, 130), (10, 5), 0, 0, 360, (50, 50, 50), -1)
        
        # Save test image
        cls.test_image_path = os.path.join(cls.test_dir, 'test_face.png')
        cv2.imwrite(cls.test_image_path, test_img)
        
        # Output path for processed images
        cls.output_path = os.path.join(cls.test_dir, 'output.png')
        
    def tearDown(self):
        # Clean up output file after each test
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
            
    @classmethod
    def tearDownClass(cls):
        # Clean up test directory
        if os.path.exists(cls.test_dir):
            for file in os.listdir(cls.test_dir):
                os.remove(os.path.join(cls.test_dir, file))
            os.rmdir(cls.test_dir)
            
    def test_process_image_with_face(self):
        """Test processing an image containing a face"""
        result = self.processor.process_image(self.test_image_path, self.output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_path))
        
        # Check output image
        output_img = Image.open(self.output_path)
        self.assertEqual(output_img.mode, 'RGBA')  # Should be RGBA for transparency
        
    def test_process_image_with_circular_mask(self):
        """Test processing with circular mask option"""
        result = self.processor.process_image(self.test_image_path, self.output_path, circular_mask=True)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_path))
        
        # Check output image
        output_img = Image.open(self.output_path)
        self.assertEqual(output_img.mode, 'RGBA')
        
    def test_process_nonexistent_image(self):
        """Test processing a non-existent image"""
        result = self.processor.process_image('nonexistent.jpg', self.output_path)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.output_path))

if __name__ == '__main__':
    unittest.main()
