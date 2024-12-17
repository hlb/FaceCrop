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
        cls.output_path = os.path.join(cls.test_dir, "output.jpg")
        cls.processor = ImageProcessor()

        # Use Mona Lisa test image
        cls.mona_lisa_image = os.path.join(
            "tests", "fixtures", "images", "Mona_Lisa.jpg"
        )
        if not os.path.exists(cls.mona_lisa_image):
            raise FileNotFoundError(
                f"Test fixture image not found: {cls.mona_lisa_image}"
            )
        cls.mona_lisa_path = os.path.join(cls.test_dir, "mona_lisa.jpg")
        shutil.copy2(cls.mona_lisa_image, cls.mona_lisa_path)

        # Use cat test image
        cls.cat_image = os.path.join("tests", "fixtures", "images", "cat.jpg")
        if not os.path.exists(cls.cat_image):
            raise FileNotFoundError(f"Test fixture image not found: {cls.cat_image}")
        cls.cat_path = os.path.join(cls.test_dir, "cat.jpg")
        shutil.copy2(cls.cat_image, cls.cat_path)

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

    def test_process_mona_lisa_normal(self):
        """Test processing Mona Lisa image in normal mode"""
        result = self.processor.process_image(self.mona_lisa_path, self.output_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_path))

        # Check output image
        output_img = Image.open(self.output_path)
        self.assertEqual(output_img.mode, "RGBA")  # Should be RGBA for transparency

    def test_process_mona_lisa_strict(self):
        """Test processing Mona Lisa image in strict mode"""
        result = self.processor.process_image(
            self.mona_lisa_path, self.output_path, strict=True
        )
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_path))

        # Check output image
        output_img = Image.open(self.output_path)
        self.assertEqual(output_img.mode, "RGBA")

    def test_process_cat_normal(self):
        """Test processing cat image in normal mode"""
        result = self.processor.process_image(self.cat_path, self.output_path)
        # May or may not detect a face in normal mode, but shouldn't crash
        if result:
            self.assertTrue(os.path.exists(self.output_path))
            output_img = Image.open(self.output_path)
            self.assertEqual(output_img.mode, "RGBA")

    def test_process_cat_strict(self):
        """Test processing cat image in strict mode"""
        result = self.processor.process_image(
            self.cat_path, self.output_path, strict=True
        )
        # Should not detect a face in strict mode
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.output_path))

    def test_process_image_with_circular_mask(self):
        """Test processing with circular mask option"""
        result = self.processor.process_image(
            self.mona_lisa_path, self.output_path, circular_mask=True
        )
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_path))

        # Check output image
        output_img = Image.open(self.output_path)
        self.assertEqual(output_img.mode, "RGBA")

    def test_process_nonexistent_image(self):
        """Test processing a non-existent image"""
        result = self.processor.process_image("nonexistent.jpg", self.output_path)
        self.assertFalse(result)
        self.assertFalse(os.path.exists(self.output_path))


if __name__ == "__main__":
    unittest.main()
