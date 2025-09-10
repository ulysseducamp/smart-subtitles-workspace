"""
Frequency List Loader for Smart Subtitles API

This module provides efficient in-memory loading and caching of word frequency lists
for different languages. The frequency lists are used by the fusion algorithm to
determine which words are "known" vs "unknown" for vocabulary-based subtitle selection.

Features:
- Lazy loading: Only load frequency lists when needed
- In-memory caching: O(1) word lookup performance
- Cross-platform file paths using pathlib
- Graceful error handling for missing files
- UTF-8 encoding support
- Word normalization (lowercase, strip whitespace)
"""

from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class FrequencyLoader:
    """
    Efficient frequency list loader with in-memory caching.
    
    Loads word frequency lists from static files and provides O(1) lookup
    performance for the fusion algorithm.
    """
    
    def __init__(self, frequency_lists_dir: Optional[Path] = None):
        """
        Initialize the frequency loader.
        
        Args:
            frequency_lists_dir: Path to directory containing frequency list files.
                                Defaults to src/frequency_lists/ relative to this file.
        """
        if frequency_lists_dir is None:
            # Default to src/frequency_lists/ relative to this file
            self.frequency_lists_dir = Path(__file__).parent / "frequency_lists"
        else:
            self.frequency_lists_dir = Path(frequency_lists_dir)
            
        
        # Language to filename mapping
        self._language_files = {
            'en': 'en-10000.txt',
            'fr': 'fr-5000.txt', 
            'pt': 'pt-10000.txt',
            'es': 'es-10000.txt'
        }
        
        logger.info(f"FrequencyLoader initialized with directory: {self.frequency_lists_dir}")
    
    
    
    def get_top_n_words(self, language: str, top_n: int) -> List[str]:
        """
        Get top N most frequent words for a language in frequency order.
        Simple and efficient: reads directly from file without caching the full list.
        
        Args:
            language: Language code
            top_n: Number of top words to return
            
        Returns:
            List of top N words in frequency order (most frequent first)
        """
        # Normalize language code
        language = language.lower().strip()
        
        if language not in self._language_files:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(self._language_files.keys())}")
        
        filename = self._language_files[language]
        file_path = self.frequency_lists_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Frequency list file not found: {file_path}")
        
        try:
            # Read only the top N words directly from file
            with open(file_path, 'r', encoding='utf-8') as f:
                words = []
                for i, line in enumerate(f):
                    if i >= top_n:  # Stop after reading top_n words
                        break
                    word = line.strip().lower()
                    if word:  # Skip empty lines
                        words.append(word)
            
            logger.info(f"Loaded top {len(words)} words for {language} from {filename}")
            return words
            
        except Exception as e:
            logger.error(f"Error loading top {top_n} words for {language}: {e}")
            raise
    
    
    def get_supported_languages(self) -> list[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of supported language codes
        """
        return list(self._language_files.keys())
    


# Global instance for easy access
_frequency_loader: Optional[FrequencyLoader] = None


def get_frequency_loader() -> FrequencyLoader:
    """
    Get the global frequency loader instance.
    
    Returns:
        Global FrequencyLoader instance
    """
    global _frequency_loader
    if _frequency_loader is None:
        _frequency_loader = FrequencyLoader()
    return _frequency_loader


def initialize_frequency_loader(frequency_lists_dir: Optional[Path] = None) -> FrequencyLoader:
    """
    Initialize the global frequency loader with optional custom directory.
    
    Args:
        frequency_lists_dir: Optional custom directory for frequency lists
        
    Returns:
        Initialized FrequencyLoader instance
    """
    global _frequency_loader
    _frequency_loader = FrequencyLoader(frequency_lists_dir)
    return _frequency_loader
