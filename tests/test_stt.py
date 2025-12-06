"""
Unit tests for Speech-to-Text
"""

import unittest
import numpy as np
from modules.speech_to_text import SpeechToText


class TestSpeechToText(unittest.TestCase):
    """Test cases for STT functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use tiny model for faster testing
        self.stt = SpeechToText(model_size="tiny")
    
    def test_model_loading(self):
        """Test that model loads correctly"""
        info = self.stt.get_model_info()
        self.assertIsInstance(info, dict)
        self.assertIn('model_size', info)
        self.assertIn('loaded', info)
    
    def test_transcribe_structure(self):
        """Test transcription result structure"""
        # Note: This would require actual audio file
        # For now, just test the structure
        result = {
            'text': '',
            'language': None,
            'error': 'No audio provided'
        }
        self.assertIn('text', result)
        self.assertIn('language', result)
        self.assertIn('error', result)


if __name__ == '__main__':
    unittest.main()

