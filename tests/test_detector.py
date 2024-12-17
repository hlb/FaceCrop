import unittest
import cv2
import numpy as np
import os
from src.detector import FaceDetector

class TestFaceDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.detector = FaceDetector()
        
        # Use Mona Lisa test image
        cls.fixture_image = os.path.join('tests', 'fixtures', 'images', 'Mona_Lisa.jpg')
        if not os.path.exists(cls.fixture_image):
            raise FileNotFoundError(f"Test fixture image not found: {cls.fixture_image}")
        cls.test_img = cv2.imread(cls.fixture_image)
        if cls.test_img is None:
            raise ValueError(f"Failed to load test image: {cls.fixture_image}")
        
    def test_detector_initialization(self):
        """Test if detector initializes correctly"""
        self.assertIsNotNone(self.detector.mp_face_detection)
        self.assertIsNotNone(self.detector.haar_cascade)
        self.assertIsNotNone(self.detector.profile_cascade)
        
    def test_detect_face_empty_image(self):
        """Test detection on empty image"""
        empty_img = np.zeros((100, 100, 3), dtype=np.uint8)
        result = self.detector.detect_face(empty_img)
        self.assertIsNone(result)
        
    def test_detect_face_with_face(self):
        """Test detection on image with face-like pattern"""
        result = self.detector.detect_face(self.test_img)
        
        # Should return a tuple of 4 values (x, y, w, h)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)
        
        # Coordinates should be within image bounds
        x, y, w, h = result
        self.assertTrue(0 <= x < self.test_img.shape[1])
        self.assertTrue(0 <= y < self.test_img.shape[0])
        self.assertTrue(w > 0 and h > 0)
        self.assertTrue(x + w <= self.test_img.shape[1])
        self.assertTrue(y + h <= self.test_img.shape[0])

if __name__ == '__main__':
    unittest.main()
