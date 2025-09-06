"""
Test suite for subtitle fusion functionality
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from subtitle_fusion import SubtitleFusionEngine

class TestSubtitleFusion(unittest.TestCase):
    """Test cases for subtitle fusion engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = SubtitleFusionEngine()
    
    def test_engine_initialization(self):
        """Test that the engine initializes correctly"""
        self.assertIsNotNone(self.engine)
        self.assertIsInstance(self.engine.english_contractions, dict)
        self.assertIn("don't", self.engine.english_contractions)
    
    def test_contractions_mapping(self):
        """Test English contractions mapping"""
        contractions = self.engine.english_contractions
        self.assertEqual(contractions["don't"], ["do", "not"])
        self.assertEqual(contractions["you're"], ["you", "are"])
        self.assertEqual(contractions["can't"], ["can", "not"])

if __name__ == '__main__':
    unittest.main()
