"""
Test suite for subtitle fusion algorithm
"""

import unittest
import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from subtitle_fusion import SubtitleFusionEngine
from srt_parser import parse_srt, Subtitle

class TestFusionAlgorithm(unittest.TestCase):
    """Test cases for subtitle fusion algorithm"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = SubtitleFusionEngine()
    
    def test_proper_noun_detection(self):
        """Test proper noun detection"""
        known_words = {"i", "am", "running", "quickly"}
        
        # Test capitalized word at beginning of sentence (should be proper noun if not in frequency list)
        result = self.engine.is_proper_noun("John", "John is running", known_words)
        self.assertTrue(result)
        
        # Test capitalized word not at beginning (should be proper noun)
        result = self.engine.is_proper_noun("John", "I see John running", known_words)
        self.assertTrue(result)
        
        # Test lowercase word (should not be proper noun)
        result = self.engine.is_proper_noun("running", "I am running", known_words)
        self.assertFalse(result)
    
    def test_word_known_check(self):
        """Test word knowledge checking with contractions"""
        known_words = {"i", "do", "not", "understand"}
        
        # Test known word
        result = self.engine.is_word_known("understand", known_words, "en")
        self.assertTrue(result)
        
        # Test contraction where all parts are known
        result = self.engine.is_word_known("don't", known_words, "en")
        self.assertTrue(result)
        
        # Test unknown word
        result = self.engine.is_word_known("complicated", known_words, "en")
        self.assertFalse(result)
    
    def test_time_intersection(self):
        """Test time intersection detection"""
        # Test overlapping times
        result = self.engine._has_intersection("00:00:10,000", "00:00:15,000", 
                                             "00:00:12,000", "00:00:18,000")
        self.assertTrue(result)
        
        # Test non-overlapping times
        result = self.engine._has_intersection("00:00:10,000", "00:00:15,000", 
                                             "00:00:20,000", "00:00:25,000")
        self.assertFalse(result)
    
    def test_srt_time_conversion(self):
        """Test SRT time to milliseconds conversion"""
        result = self.engine._srt_time_to_ms("00:01:30,500")
        expected = 90500  # 1 minute 30 seconds 500 milliseconds
        self.assertEqual(result, expected)
    
    def test_fusion_with_simple_data(self):
        """Test fusion algorithm with simple test data"""
        # Create simple test subtitles
        target_subs = [
            Subtitle("1", "00:00:10,000", "00:00:15,000", "I understand this"),
            Subtitle("2", "00:00:16,000", "00:00:20,000", "This is complicated")
        ]

        native_subs = [
            Subtitle("1", "00:00:10,000", "00:00:15,000", "Je comprends ceci"),
            Subtitle("2", "00:00:16,000", "00:00:20,000", "C'est compliqué")
        ]

        known_words = {"i", "understand", "this", "is"}

        # Run async method using asyncio.run()
        result = asyncio.run(self.engine.fuse_subtitles(target_subs, native_subs, known_words, "en"))

        self.assertTrue(result['success'])
        self.assertEqual(len(result['hybrid']), 2)
        # First subtitle should be kept (all words known)
        self.assertEqual(result['hybrid'][0].text, "I understand this")
        # Second subtitle should be replaced (unknown word "complicated")
        self.assertEqual(result['hybrid'][1].text, "C'est compliqué")

if __name__ == '__main__':
    unittest.main()
