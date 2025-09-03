"""
Vocabulary analysis and proper noun detection
Core logic from your TypeScript decision engine
"""

class VocabularyAnalyzer:
    def __init__(self, frequency_list: list, top_n: int):
        self.known_words = set(frequency_list[:top_n])
    
    def analyze_subtitle_text(self, text: str, language: str) -> dict:
        """Analyze subtitle text for vocabulary decisions"""
        # TODO: Port your sophisticated proper noun detection
        return {
            "known_words": [],
            "unknown_words": [],
            "proper_nouns": [],
            "decision": "placeholder"  # target, native, or inline
        }
    
    def is_proper_noun(self, word: str) -> bool:
        """Detect proper nouns using your frequency-based logic"""
        # TODO: Port from TypeScript proper noun detection
        return False
    
    def should_use_inline_translation(self, unknown_words: list) -> bool:
        """Determine if single word should get inline translation"""
        return len(unknown_words) == 1
