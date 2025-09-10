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
from typing import Dict, Set, Optional
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
            
        # Cache for loaded frequency sets
        self._frequency_sets: Dict[str, Set[str]] = {}
        
        # Language to filename mapping
        self._language_files = {
            'en': 'en-10000.txt',
            'fr': 'fr-5000.txt', 
            'pt': 'pt-10000.txt',
            'es': 'es-10000.txt'
        }
        
        logger.info(f"FrequencyLoader initialized with directory: {self.frequency_lists_dir}")
    
    def get_frequency_set(self, language: str) -> Set[str]:
        """
        Get frequency set for a language, loading it if not already cached.
        
        Args:
            language: Language code (en, fr, pt, es)
            
        Returns:
            Set of words in the frequency list (normalized to lowercase)
            
        Raises:
            FileNotFoundError: If frequency list file doesn't exist
            ValueError: If language is not supported
        """
        # Normalize language code
        language = language.lower().strip()
        
        if language not in self._language_files:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(self._language_files.keys())}")
        
        # Return cached set if available
        if language in self._frequency_sets:
            return self._frequency_sets[language]
        
        # Load and cache the frequency set
        self._load_language(language)
        return self._frequency_sets[language]
    
    def _load_language(self, language: str) -> None:
        """
        Load frequency list for a language from file.
        
        Args:
            language: Language code
            
        Raises:
            FileNotFoundError: If frequency list file doesn't exist
        """
        filename = self._language_files[language]
        file_path = self.frequency_lists_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Frequency list file not found: {file_path}")
        
        try:
            # Read file with UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as f:
                words = set()
                for line in f:
                    word = line.strip().lower()
                    if word:  # Skip empty lines
                        words.add(word)
            
            # Cache the loaded set
            self._frequency_sets[language] = words
            
            logger.info(f"Loaded frequency list for {language}: {len(words)} words from {filename}")
            
        except Exception as e:
            logger.error(f"Error loading frequency list for {language}: {e}")
            raise
    
    def is_word_known(self, word: str, language: str) -> bool:
        """
        Check if a word is in the frequency list for a language.
        
        Args:
            word: Word to check (will be normalized)
            language: Language code
            
        Returns:
            True if word is in frequency list, False otherwise
        """
        try:
            frequency_set = self.get_frequency_set(language)
            normalized_word = word.strip().lower()
            return normalized_word in frequency_set
        except (FileNotFoundError, ValueError):
            # If language not supported or file missing, assume word is unknown
            logger.warning(f"Cannot check word '{word}' for language '{language}' - assuming unknown")
            return False
    
    def get_supported_languages(self) -> list[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of supported language codes
        """
        return list(self._language_files.keys())
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get statistics about cached frequency sets.
        
        Returns:
            Dictionary mapping language codes to number of cached words
        """
        return {lang: len(words) for lang, words in self._frequency_sets.items()}


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
