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
        cls.mona_lisa_image = os.path.join(
            "tests", "fixtures", "images", "Mona_Lisa.jpg"
        )
        if not os.path.exists(cls.mona_lisa_image):
            raise FileNotFoundError(
                f"Test fixture image not found: {cls.mona_lisa_image}"
            )
        cls.mona_lisa_img = cv2.imread(cls.mona_lisa_image)
        if cls.mona_lisa_img is None:
            raise ValueError(f"Failed to load test image: {cls.mona_lisa_image}")

        # Use cat test image
        cls.cat_image = os.path.join("tests", "fixtures", "images", "cat.jpg")
        if not os.path.exists(cls.cat_image):
            raise FileNotFoundError(f"Test fixture image not found: {cls.cat_image}")
        cls.cat_img = cv2.imread(cls.cat_image)
        if cls.cat_img is None:
            raise ValueError(f"Failed to load test image: {cls.cat_image}")

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

    def test_detect_face_mona_lisa_normal(self):
        """Test detection on Mona Lisa image in normal mode"""
        result = self.detector.detect_face(self.mona_lisa_img, strict=False)

        # Should return a tuple of 4 values (x, y, w, h)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)

        # Coordinates should be within image bounds
        x, y, w, h = result
        self.assertTrue(0 <= x < self.mona_lisa_img.shape[1])
        self.assertTrue(0 <= y < self.mona_lisa_img.shape[0])
        self.assertTrue(w > 0 and h > 0)
        self.assertTrue(x + w <= self.mona_lisa_img.shape[1])
        self.assertTrue(y + h <= self.mona_lisa_img.shape[0])

    def test_detect_face_mona_lisa_strict(self):
        """Test detection on Mona Lisa image in strict mode"""
        result = self.detector.detect_face(self.mona_lisa_img, strict=True)

        # Should still detect Mona Lisa's face even in strict mode
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)

        x, y, w, h = result
        self.assertTrue(0 <= x < self.mona_lisa_img.shape[1])
        self.assertTrue(0 <= y < self.mona_lisa_img.shape[0])
        self.assertTrue(w > 0 and h > 0)
        self.assertTrue(x + w <= self.mona_lisa_img.shape[1])
        self.assertTrue(y + h <= self.mona_lisa_img.shape[0])

    def test_detect_face_cat_normal(self):
        """Test detection on cat image in normal mode"""
        result = self.detector.detect_face(self.cat_img, strict=False)

        # In normal mode, might detect cat face as human face
        if result:
            x, y, w, h = result
            self.assertTrue(0 <= x < self.cat_img.shape[1])
            self.assertTrue(0 <= y < self.cat_img.shape[0])
            self.assertTrue(w > 0 and h > 0)
            self.assertTrue(x + w <= self.cat_img.shape[1])
            self.assertTrue(y + h <= self.cat_img.shape[0])

    def test_detect_face_cat_strict(self):
        """Test detection on cat image in strict mode"""
        result = self.detector.detect_face(self.cat_img, strict=True)

        # Should not detect cat face as human face in strict mode
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
