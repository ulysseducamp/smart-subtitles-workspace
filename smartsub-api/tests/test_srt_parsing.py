"""
Test suite for SRT parsing functionality
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from srt_parser import parse_srt, generate_srt, normalize_words, Subtitle

class TestSRTParsing(unittest.TestCase):
    """Test cases for SRT parsing functions"""
    
    def test_parse_srt_basic(self):
        """Test basic SRT parsing"""
        srt_content = """1
00:00:06,000 --> 00:00:08,800
A NETFLIX ORIGINAL SERIES

2
00:00:11,320 --> 00:00:13,120
[distant roar of traffic]"""
        
        subtitles = parse_srt(srt_content)
        
        self.assertEqual(len(subtitles), 2)
        self.assertEqual(subtitles[0].index, "1")
        self.assertEqual(subtitles[0].start, "00:00:06,000")
        self.assertEqual(subtitles[0].end, "00:00:08,800")
        self.assertEqual(subtitles[0].text, "A NETFLIX ORIGINAL SERIES")
        
        self.assertEqual(subtitles[1].index, "2")
        self.assertEqual(subtitles[1].text, "[distant roar of traffic]")
    
    def test_generate_srt(self):
        """Test SRT generation"""
        subtitles = [
            Subtitle("1", "00:00:06,000", "00:00:08,800", "A NETFLIX ORIGINAL SERIES"),
            Subtitle("2", "00:00:11,320", "00:00:13,120", "[distant roar of traffic]")
        ]
        
        result = generate_srt(subtitles)
        
        self.assertIn("1\n00:00:06,000 --> 00:00:08,800\nA NETFLIX ORIGINAL SERIES", result)
        self.assertIn("2\n00:00:11,320 --> 00:00:13,120\n[distant roar of traffic]", result)
    
    def test_round_trip(self):
        """Test parse -> generate -> parse round trip"""
        original_srt = """1
00:00:06,000 --> 00:00:08,800
A NETFLIX ORIGINAL SERIES

2
00:00:11,320 --> 00:00:13,120
[distant roar of traffic]"""
        
        # Parse
        subtitles = parse_srt(original_srt)
        
        # Generate
        generated_srt = generate_srt(subtitles)
        
        # Parse again
        subtitles2 = parse_srt(generated_srt)
        
        # Should be identical
        self.assertEqual(len(subtitles), len(subtitles2))
        self.assertEqual(subtitles[0].text, subtitles2[0].text)
        self.assertEqual(subtitles[1].text, subtitles2[1].text)
    
    def test_normalize_words(self):
        """Test word normalization"""
        text = "I don't understand this complicated situation!"
        words = normalize_words(text)
        
        expected = ["i", "don't", "understand", "this", "complicated", "situation"]
        self.assertEqual(words, expected)
    
    def test_normalize_words_with_html(self):
        """Test word normalization with HTML tags"""
        text = "<i>I don't</i> understand this <b>complicated</b> situation!"
        words = normalize_words(text)
        
        expected = ["i", "don't", "understand", "this", "complicated", "situation"]
        self.assertEqual(words, expected)

if __name__ == '__main__':
    unittest.main()
