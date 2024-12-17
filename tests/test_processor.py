import unittest
import os
import cv2
import numpy as np
from PIL import Image
from src.processor import ImageProcessor
import tempfile
import shutil

class TestImageProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_dir = tempfile.mkdtemp()
        cls.output_path = os.path.join(cls.test_dir, 'output.jpg')
        cls.processor = ImageProcessor()
        
        # Use Mona Lisa test image
        cls.fixture_image = os.path.join('tests', 'fixtures', 'images', 'Mona_Lisa.jpg')
        if not os.path.exists(cls.fixture_image):
            raise FileNotFoundError(f"Test fixture image not found: {cls.fixture_image}")
        cls.test_image_path = os.path.join(cls.test_dir, 'test_image.jpg')
        shutil.copy2(cls.fixture_image, cls.test_image_path)
        
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
