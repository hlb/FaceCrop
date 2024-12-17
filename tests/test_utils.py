import unittest
import numpy as np
from PIL import Image
from src.utils import create_circular_mask

class TestUtils(unittest.TestCase):
    def test_create_circular_mask(self):
        # Test with square dimensions
        size = (100, 100)
        mask = create_circular_mask(size)
        
        # Check if mask is the correct size
        self.assertEqual(mask.size, size)
        
        # Check if mask is in L mode (grayscale)
        self.assertEqual(mask.mode, "L")
        
        # Convert to numpy array for easier testing
        mask_array = np.array(mask)
        
        # Check if center is white (255)
        center_x, center_y = size[0] // 2, size[1] // 2
        self.assertEqual(mask_array[center_y, center_x], 255)
        
        # Check if corners are black (0)
        self.assertEqual(mask_array[0, 0], 0)  # Top-left
        self.assertEqual(mask_array[0, -1], 0)  # Top-right
        self.assertEqual(mask_array[-1, 0], 0)  # Bottom-left
        self.assertEqual(mask_array[-1, -1], 0)  # Bottom-right
        
    def test_create_circular_mask_rectangular(self):
        # Test with rectangular dimensions
        size = (150, 100)
        mask = create_circular_mask(size)
        
        # Check if mask is the correct size
        self.assertEqual(mask.size, size)
        
        # Check if mask is in L mode (grayscale)
        self.assertEqual(mask.mode, "L")

if __name__ == '__main__':
    unittest.main()
