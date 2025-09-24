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
from typing import Set, Optional, Dict
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
            current_file = Path(__file__)
            self.frequency_lists_dir = current_file.parent / "frequency_lists"
        else:
            self.frequency_lists_dir = frequency_lists_dir
            
        
        # Language to filename mapping
        self._language_files = {
            'en': 'en-10000.txt',
            'fr': 'fr-5000.txt', 
            'pt': 'pt-10000.txt'
        }
        
        # Cache for loaded frequency lists
        self._cache: dict[str, Set[str]] = {}
        
        # Cache for word rankings (word -> rank mapping)
        self._ranking_cache: dict[str, Dict[str, int]] = {}
        
        logger.info(f"FrequencyLoader initialized with directory: {self.frequency_lists_dir}")
    
    def get_top_n_words(self, language: str, top_n: int = 2000) -> Set[str]:
        """
        Get the top N most frequent words for a language.
        
        Args:
            language: Language code (e.g., 'en', 'fr', 'pt')
            top_n: Number of top words to return (default: 2000)
            
        Returns:
            Set of the top N most frequent words
            
        Raises:
            ValueError: If language is not supported
            FileNotFoundError: If frequency list file doesn't exist
        """
        # Normalize language code
        language = language.lower().strip()
        
        if language not in self._language_files:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(self._language_files.keys())}")
        
        filename = self._language_files[language]
        file_path = self.frequency_lists_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Frequency list file not found: {file_path}")
        
        # Check cache first
        cache_key = f"{language}_{top_n}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Load and cache the frequency list
        try:
            words = []
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= top_n:  # Stop after reading top_n words
                        break
                    word = line.strip().lower()
                    if word:  # Skip empty lines
                        words.append(word)
            
            logger.info(f"Loaded top {len(words)} words for {language} from {filename}")
            
            # Convert to set for O(1) lookup
            word_set = set(words)
            self._cache[cache_key] = word_set
            return word_set
            
        except Exception as e:
            logger.error(f"Error loading frequency list for {language}: {e}")
            raise
    
    
    def get_word_rank(self, word: str, language: str, top_n: int = 2000) -> Optional[int]:
        """
        Get the rank (1-indexed) of a word in the frequency list.

        Args:
            word: The word to look up
            language: Language code (e.g., 'en', 'fr', 'pt')
            top_n: Number of top words to consider (default: 2000)

        Returns:
            The rank (1-indexed) of the word, or None if not in the top_n words

        Raises:
            ValueError: If language is not supported
            FileNotFoundError: If frequency list file doesn't exist
        """
        # Normalize inputs
        original_word = word
        word = word.lower().strip()
        language = language.lower().strip()

        if language not in self._language_files:
            raise ValueError(f"Unsupported language: {language}. Supported: {list(self._language_files.keys())}")

        # Check cache first
        cache_key = f"{language}_{top_n}"
        if cache_key not in self._ranking_cache:
            logger.info(f"RANK_DIAGNOSTIC: Cache miss pour {cache_key}, construction en cours...")
            self._build_ranking_cache(language, top_n)

        rank = self._ranking_cache[cache_key].get(word)

        # DIAGNOSTIC LOG: Tracer les recherches de rang suspectes
        if original_word in ['as', 'de', 'para', 'que', 'a', 'o', 'e', 'da', 'do', 'em', 'um', 'uma']:
            cache_size = len(self._ranking_cache[cache_key])
            if rank:
                logger.info(f"RANK_DIAGNOSTIC: mot_suspect='{original_word}' → normalisé='{word}' → rang={rank}/{top_n} (cache_size={cache_size})")
            else:
                # Vérifier si le mot existe dans le cache avec une recherche exhaustive
                found_variants = [k for k in self._ranking_cache[cache_key].keys() if original_word.lower() in k]
                logger.warning(f"RANK_DIAGNOSTIC: mot_suspect='{original_word}' → normalisé='{word}' → NOT_FOUND (cache_size={cache_size}, variants_trouvés={found_variants[:5]})")

        return rank
    
    def _build_ranking_cache(self, language: str, top_n: int) -> None:
        """
        Build the ranking cache for a language and top_n combination.
        
        Args:
            language: Language code
            top_n: Number of top words to consider
        """
        filename = self._language_files[language]
        file_path = self.frequency_lists_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Frequency list file not found: {file_path}")
        
        # Build ranking dictionary from file order
        ranking_dict = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= top_n:  # Stop after reading top_n words
                    break
                word = line.strip().lower()
                if word:  # Skip empty lines
                    ranking_dict[word] = i + 1  # 1-indexed ranking
        
        # Cache the ranking dictionary
        cache_key = f"{language}_{top_n}"
        self._ranking_cache[cache_key] = ranking_dict
        
        logger.info(f"Built ranking cache for {language} with {len(ranking_dict)} words (top {top_n})")
    
    def get_supported_languages(self) -> list[str]:
        """
        Get list of supported language codes.
        
        Returns:
            List of supported language codes
        """
        return list(self._language_files.keys())
    


# Global instance for easy access
_frequency_loader: Optional[FrequencyLoader] = None


def initialize_frequency_loader(frequency_lists_dir: Optional[Path] = None) -> FrequencyLoader:
    """
    Initialize the global frequency loader instance.
    
    Args:
        frequency_lists_dir: Path to directory containing frequency list files.
                            Defaults to src/frequency_lists/ relative to this file.
    
    Returns:
        The initialized FrequencyLoader instance
    """
    global _frequency_loader
    _frequency_loader = FrequencyLoader(frequency_lists_dir)
    return _frequency_loader


def get_frequency_loader() -> FrequencyLoader:
    """
    Get the global frequency loader instance.
    
    Returns:
        The global FrequencyLoader instance
        
    Raises:
        RuntimeError: If the frequency loader hasn't been initialized
    """
    if _frequency_loader is None:
        raise RuntimeError("Frequency loader not initialized. Call initialize_frequency_loader() first.")
    return _frequency_loader