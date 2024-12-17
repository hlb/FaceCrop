import unittest
import os
import sys
import tempfile
import shutil
import numpy as np
import cv2
from unittest.mock import patch
from src.cli import main

class TestCLI(unittest.TestCase):
    def setUp(self):
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, 'output')
        
        # Use Mona Lisa image from fixtures
        self.fixture_image = os.path.join(os.path.dirname(__file__), 'fixtures', 'images', 'Mona_Lisa.jpg')
        if not os.path.exists(self.fixture_image):
            raise FileNotFoundError(f"Test fixture image not found: {self.fixture_image}")
        self.test_image = os.path.join(self.test_dir, 'Mona_Lisa.jpg')
        shutil.copy2(self.fixture_image, self.test_image)
        
    def tearDown(self):
        # Clean up test directory
        shutil.rmtree(self.test_dir)
        
    @patch('sys.argv')
    def test_single_file_processing(self, mock_argv):
        """Test processing a single file"""
        # Set the mock argv list directly
        sys.argv = ['face_crop.py', self.test_image]
        # We expect the program to exit normally
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        
    @patch('sys.argv')
    def test_single_file_with_output(self, mock_argv):
        """Test processing a single file with specified output"""
        output_path = os.path.join(self.test_dir, 'output.png')
        sys.argv = ['face_crop.py', self.test_image, '--output', output_path]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        
    @patch('sys.argv')
    def test_directory_processing(self, mock_argv):
        """Test processing a directory"""
        os.makedirs(self.output_dir)
        sys.argv = ['face_crop.py', self.test_dir, '--output', self.output_dir]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        
    @patch('sys.argv')
    def test_directory_without_output(self, mock_argv):
        """Test processing a directory without output directory"""
        sys.argv = ['face_crop.py', self.test_dir]
        with self.assertRaises(SystemExit) as cm:
            main()
        # Should exit with error code 1 since output directory is required for directory input
        self.assertEqual(cm.exception.code, 1)
        
    @patch('sys.argv')
    def test_circular_mask_option(self, mock_argv):
        """Test circular mask option"""
        sys.argv = ['face_crop.py', self.test_image, '--circular']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        
    @patch('sys.argv')
    def test_single_file_processing_failure(self, mock_argv):
        """Test processing a single file that fails"""
        # Create an empty file that's not a valid image
        invalid_image = os.path.join(self.test_dir, 'invalid.jpg')
        with open(invalid_image, 'w') as f:
            f.write('not an image')
            
        sys.argv = ['face_crop.py', invalid_image]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        
    @patch('sys.argv')
    def test_empty_directory_processing(self, mock_argv):
        """Test processing an empty directory"""
        empty_dir = os.path.join(self.test_dir, 'empty')
        os.makedirs(empty_dir)
        sys.argv = ['face_crop.py', empty_dir, '--output', self.output_dir]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        
    @patch('sys.argv')
    def test_directory_with_invalid_images(self, mock_argv):
        """Test processing a directory with invalid images"""
        input_dir = os.path.join(self.test_dir, 'invalid_images')
        os.makedirs(input_dir)
        
        # Create an invalid image file
        invalid_image = os.path.join(input_dir, 'invalid.jpg')
        with open(invalid_image, 'w') as f:
            f.write('not an image')
            
        sys.argv = ['face_crop.py', input_dir, '--output', self.output_dir]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        
    @patch('sys.argv')
    def test_directory_with_mixed_files(self, mock_argv):
        """Test processing a directory with both valid and invalid images"""
        input_dir = os.path.join(self.test_dir, 'mixed')
        os.makedirs(input_dir)
        
        # Copy valid image
        valid_image = os.path.join(input_dir, 'valid.jpg')
        shutil.copy2(self.fixture_image, valid_image)
        
        # Create an invalid image
        invalid_image = os.path.join(input_dir, 'invalid.jpg')
        with open(invalid_image, 'w') as f:
            f.write('not an image')
            
        # Create a non-image file
        text_file = os.path.join(input_dir, 'readme.txt')
        with open(text_file, 'w') as f:
            f.write('This is not an image')
            
        sys.argv = ['face_crop.py', input_dir, '--output', self.output_dir]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)  # Should succeed because at least one image processed
        
if __name__ == '__main__':
    unittest.main()
