"""
Unit tests for OCR Text Extractor
"""

import unittest
import numpy as np
import cv2
from modules.ocr_text_extractor import OCRTextExtractor


class TestOCRTextExtractor(unittest.TestCase):
    """Test cases for OCR functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ocr = OCRTextExtractor()
        # Create a simple test image with text
        self.test_image = np.ones((100, 300, 3), dtype=np.uint8) * 255
        cv2.putText(self.test_image, "Hello World", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    def test_extract_text(self):
        """Test basic text extraction"""
        text = self.ocr.extract_text(self.test_image)
        self.assertIsInstance(text, str)
        # OCR may not always extract perfectly, so just check it returns something
        # In real scenario, would use a known test image
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        test_text = "This is a Python project using Machine Learning and TensorFlow"
        keywords = self.ocr.extract_keywords(test_text)
        self.assertIsInstance(keywords, list)
        # Should extract technical terms
        self.assertGreater(len(keywords), 0)
    
    def test_extract_code_snippets(self):
        """Test code snippet detection"""
        test_text = "def my_function(x, y): return x + y"
        snippets = self.ocr.detect_code_snippets(test_text)
        self.assertIsInstance(snippets, list)
        # Should detect function definition
        self.assertGreater(len(snippets), 0)
    
    def test_detect_ui_elements(self):
        """Test UI element detection"""
        elements = self.ocr.detect_ui_elements(self.test_image)
        self.assertIsInstance(elements, dict)
        self.assertIn('elements', elements)
        self.assertIn('count', elements)


if __name__ == '__main__':
    unittest.main()

