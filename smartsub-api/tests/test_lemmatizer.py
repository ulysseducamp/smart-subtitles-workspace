"""
Test suite for lemmatization functionality
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lemmatizer import lemmatize_single_line, batch_lemmatize

class TestLemmatizer(unittest.TestCase):
    """Test cases for lemmatization functions"""
    
    def test_lemmatize_single_line_english(self):
        """Test English lemmatization"""
        line = "I am running quickly"
        result = lemmatize_single_line(line, "en")
        
        # Should return list of lemmatized words
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        # Note: exact lemmatization may vary, but should be consistent
        print(f"Lemmatized: {result}")
    
    def test_lemmatize_single_line_french(self):
        """Test French lemmatization"""
        line = "Je suis en train de courir"
        result = lemmatize_single_line(line, "fr")
        
        # Should return list of lemmatized words
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 6)
        print(f"Lemmatized: {result}")
    
    def test_batch_lemmatize(self):
        """Test batch lemmatization"""
        lines = [
            "I am running",
            "You are walking",
            "He is sleeping"
        ]
        result = batch_lemmatize(lines, "en")
        
        # Should return list of lists
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], list)
        print(f"Batch lemmatized: {result}")
    
    def test_lemmatize_with_punctuation(self):
        """Test lemmatization with punctuation"""
        line = "I don't understand this!"
        result = lemmatize_single_line(line, "en")
        
        # Should handle punctuation gracefully
        self.assertIsInstance(result, list)
        print(f"Lemmatized with punctuation: {result}")
    
    def test_pt_br_mapping(self):
        """Test Portuguese Brazilian language mapping"""
        line = "respirando assustados"
        result = lemmatize_single_line(line, "pt-BR")
        
        # Should return list of lemmatized words without errors
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        print(f"Portuguese BR lemmatized: {result}")
    
    def test_pt_br_variants(self):
        """Test different pt-BR language code variants"""
        line = "música sinistra"
        
        # Test different variants
        variants = ["pt-BR", "pt-br", "pt_br"]
        for variant in variants:
            result = lemmatize_single_line(line, variant)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 2)
            print(f"Portuguese {variant} lemmatized: {result}")

if __name__ == '__main__':
    unittest.main()
