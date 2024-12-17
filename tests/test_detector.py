import unittest
import cv2
import numpy as np
from src.detector import FaceDetector

class TestFaceDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = FaceDetector()
        
        # Create a simple test image with a face-like pattern
        cls.test_img = np.zeros((300, 300, 3), dtype=np.uint8)
        # Draw a flesh-colored ellipse for face
        cv2.ellipse(cls.test_img, (150, 150), (60, 80), 0, 0, 360, (204, 172, 147), -1)
        # Draw darker ellipses for eyes
        cv2.ellipse(cls.test_img, (120, 130), (10, 5), 0, 0, 360, (50, 50, 50), -1)
        cv2.ellipse(cls.test_img, (180, 130), (10, 5), 0, 0, 360, (50, 50, 50), -1)
        
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
