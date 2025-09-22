#!/usr/bin/env python3
"""
Performance comparison test for different approaches to implement word ranking.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from frequency_loader import initialize_frequency_loader

class FrequencyLoaderWithRanking:
    """Enhanced frequency loader with ranking capabilities"""
    
    def __init__(self, frequency_lists_dir: Optional[Path] = None):
        # Initialize like the original
        if frequency_lists_dir is None:
            current_file = Path(__file__)
            self.frequency_lists_dir = current_file.parent / "src" / "frequency_lists"
        else:
            self.frequency_lists_dir = frequency_lists_dir
            
        self._language_files = {
            'en': 'en-10000.txt',
            'fr': 'fr-5000.txt', 
            'pt': 'pt-10000.txt'
        }
        
        # Cache for loaded frequency lists (sets)
        self._cache: Dict[str, set] = {}
        # Cache for word rankings (dictionaries)
        self._ranking_cache: Dict[str, Dict[str, int]] = {}
    
    def get_top_n_words(self, language: str, top_n: int = 2000) -> set:
        """Get the top N most frequent words (same as original)"""
        language = language.lower().strip()
        
        if language not in self._language_files:
            raise ValueError(f"Unsupported language: {language}")
        
        filename = self._language_files[language]
        file_path = self.frequency_lists_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Frequency list file not found: {file_path}")
        
        # Check cache first
        cache_key = f"{language}_{top_n}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Load and cache the frequency list
        words = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= top_n:
                    break
                word = line.strip().lower()
                if word:
                    words.append(word)
        
        # Convert to set for O(1) lookup
        word_set = set(words)
        self._cache[cache_key] = word_set
        return word_set
    
    def get_word_rank_approach1_list(self, word: str, language: str, top_n: int = 2000) -> Optional[int]:
        """
        Approach 1: Convert set to list and use index()
        Pros: Simple, minimal memory overhead
        Cons: O(n) lookup time
        """
        words_set = self.get_top_n_words(language, top_n)
        if word not in words_set:
            return None
        
        # Convert set to list (expensive but cached)
        cache_key = f"{language}_{top_n}_list"
        if cache_key not in self._ranking_cache:
            words_list = list(words_set)
            self._ranking_cache[cache_key] = {w: i+1 for i, w in enumerate(words_list)}
        
        return self._ranking_cache[cache_key].get(word)
    
    def get_word_rank_approach2_dict(self, word: str, language: str, top_n: int = 2000) -> Optional[int]:
        """
        Approach 2: Pre-build ranking dictionary
        Pros: O(1) lookup time
        Cons: Higher memory usage (2x storage)
        """
        cache_key = f"{language}_{top_n}_dict"
        if cache_key not in self._ranking_cache:
            # Load words in order
            filename = self._language_files[language]
            file_path = self.frequency_lists_dir / filename
            
            ranking_dict = {}
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= top_n:
                        break
                    word = line.strip().lower()
                    if word:
                        ranking_dict[word] = i + 1  # 1-indexed
            
            self._ranking_cache[cache_key] = ranking_dict
        
        return self._ranking_cache[cache_key].get(word)
    
    def get_word_rank_approach3_hybrid(self, word: str, language: str, top_n: int = 2000) -> Optional[int]:
        """
        Approach 3: Hybrid - use set for existence check, then dict for ranking
        Pros: O(1) for both existence and ranking
        Cons: Highest memory usage
        """
        # First check if word exists (fast)
        words_set = self.get_top_n_words(language, top_n)
        if word not in words_set:
            return None
        
        # Then get rank (also fast)
        return self.get_word_rank_approach2_dict(word, language, top_n)

def performance_test():
    """Compare performance of different approaches"""
    print("=== TEST DE PERFORMANCE COMPARATIF ===")
    
    loader = FrequencyLoaderWithRanking()
    
    # Test words
    test_words = [
        'le', 'être', 'avoir', 'que', 'dans',  # Known words
        'fracas', 'crescendo', 'démarre', 'déclic', 'verrouillage'  # Unknown words
    ]
    
    language = 'fr'
    top_n = 2000
    iterations = 1000
    
    print(f"Test avec {len(test_words)} mots, {iterations} itérations par approche")
    print(f"Langue: {language}, Top N: {top_n}")
    
    # Approach 1: List-based
    print(f"\n1. Approche List-based (Set -> List -> Index):")
    start_time = time.time()
    for _ in range(iterations):
        for word in test_words:
            rank = loader.get_word_rank_approach1_list(word, language, top_n)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"   Temps total: {total_time:.4f}s")
    print(f"   Temps par lookup: {(total_time * 1000) / (iterations * len(test_words)):.4f}ms")
    
    # Approach 2: Dict-based
    print(f"\n2. Approche Dict-based (Pre-built ranking dict):")
    start_time = time.time()
    for _ in range(iterations):
        for word in test_words:
            rank = loader.get_word_rank_approach2_dict(word, language, top_n)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"   Temps total: {total_time:.4f}s")
    print(f"   Temps par lookup: {(total_time * 1000) / (iterations * len(test_words)):.4f}ms")
    
    # Approach 3: Hybrid
    print(f"\n3. Approche Hybrid (Set + Dict):")
    start_time = time.time()
    for _ in range(iterations):
        for word in test_words:
            rank = loader.get_word_rank_approach3_hybrid(word, language, top_n)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"   Temps total: {total_time:.4f}s")
    print(f"   Temps par lookup: {(total_time * 1000) / (iterations * len(test_words)):.4f}ms")

def memory_usage_test():
    """Test memory usage of different approaches"""
    print(f"\n=== TEST D'UTILISATION MÉMOIRE ===")
    
    loader = FrequencyLoaderWithRanking()
    language = 'fr'
    top_n = 2000
    
    # Load all approaches to populate caches
    test_words = ['le', 'être', 'fracas', 'crescendo']
    
    print("Chargement des caches...")
    for word in test_words:
        _ = loader.get_word_rank_approach1_list(word, language, top_n)
        _ = loader.get_word_rank_approach2_dict(word, language, top_n)
        _ = loader.get_word_rank_approach3_hybrid(word, language, top_n)
    
    # Analyze cache sizes
    print(f"\nAnalyse des caches:")
    print(f"   Cache sets: {len(loader._cache)} entrées")
    print(f"   Cache rankings: {len(loader._ranking_cache)} entrées")
    
    for key, value in loader._ranking_cache.items():
        if isinstance(value, dict):
            print(f"   {key}: {len(value)} mots avec rangs")

def accuracy_test():
    """Test accuracy of different approaches"""
    print(f"\n=== TEST DE PRÉCISION ===")
    
    loader = FrequencyLoaderWithRanking()
    language = 'fr'
    top_n = 2000
    
    test_words = ['le', 'être', 'avoir', 'que', 'dans', 'fracas', 'crescendo']
    
    print("Comparaison des rangs retournés:")
    print(f"{'Mot':<12} {'Approche 1':<12} {'Approche 2':<12} {'Approche 3':<12}")
    print("-" * 50)
    
    for word in test_words:
        rank1 = loader.get_word_rank_approach1_list(word, language, top_n)
        rank2 = loader.get_word_rank_approach2_dict(word, language, top_n)
        rank3 = loader.get_word_rank_approach3_hybrid(word, language, top_n)
        
        rank1_str = str(rank1) if rank1 else "None"
        rank2_str = str(rank2) if rank2 else "None"
        rank3_str = str(rank3) if rank3 else "None"
        
        print(f"{word:<12} {rank1_str:<12} {rank2_str:<12} {rank3_str:<12}")
        
        # Verify consistency
        if rank1 != rank2 or rank2 != rank3:
            print(f"   ⚠️  Incohérence détectée pour '{word}'!")

if __name__ == "__main__":
    performance_test()
    memory_usage_test()
    accuracy_test()
