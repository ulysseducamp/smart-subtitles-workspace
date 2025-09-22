#!/usr/bin/env python3
"""
Test for Step 3.1: Word ranking functionality in FrequencyLoader
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from frequency_loader import initialize_frequency_loader

def test_word_ranking_basic():
    """Test basic word ranking functionality"""
    print("=== TEST ÉTAPE 3.1 : FONCTIONNALITÉ DE RANKING ===")
    
    # Initialize frequency loader
    frequency_loader = initialize_frequency_loader()
    
    # Test known words (should have ranks)
    known_words = ['le', 'être', 'avoir', 'que', 'dans']
    print(f"\n1. Test des mots connus:")
    
    for word in known_words:
        rank = frequency_loader.get_word_rank(word, 'fr', 2000)
        print(f"   '{word}': rang {rank}")
        
        # Validate that rank is not None
        assert rank is not None, f"Word '{word}' should have a rank"
        assert isinstance(rank, int), f"Rank should be an integer, got {type(rank)}"
        assert rank >= 1, f"Rank should be >= 1, got {rank}"
    
    # Test unknown words (should return None)
    unknown_words = ['fracas', 'crescendo', 'démarre', 'déclic', 'verrouillage']
    print(f"\n2. Test des mots inconnus:")
    
    for word in unknown_words:
        rank = frequency_loader.get_word_rank(word, 'fr', 2000)
        print(f"   '{word}': {rank}")
        
        # Validate that rank is None
        assert rank is None, f"Word '{word}' should not have a rank (should be None)"
    
    print(f"\n✅ Tests de base réussis!")

def test_word_ranking_accuracy():
    """Test accuracy of word rankings against file order"""
    print(f"\n=== TEST DE PRÉCISION DES RANGS ===")
    
    frequency_loader = initialize_frequency_loader()
    
    # Read first 10 words from file to validate rankings
    filename = "src/frequency_lists/fr-5000.txt"
    file_words = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            word = line.strip().lower()
            if word:
                file_words.append(word)
    
    print(f"Validation des rangs avec les premiers 10 mots du fichier:")
    
    for i, word in enumerate(file_words, 1):
        rank = frequency_loader.get_word_rank(word, 'fr', 2000)
        expected_rank = i
        actual_rank = rank
        
        print(f"   {i}. '{word}': rang attendu={expected_rank}, rang obtenu={actual_rank}")
        
        # Validate accuracy
        assert actual_rank == expected_rank, f"Rank mismatch for '{word}': expected {expected_rank}, got {actual_rank}"
    
    print(f"\n✅ Tests de précision réussis!")

def test_word_ranking_performance():
    """Test performance of word ranking"""
    print(f"\n=== TEST DE PERFORMANCE ===")
    
    frequency_loader = initialize_frequency_loader()
    
    # Test words
    test_words = ['le', 'être', 'avoir', 'que', 'dans', 'fracas', 'crescendo']
    iterations = 1000
    
    print(f"Test de performance avec {iterations} lookups...")
    
    start_time = time.time()
    for _ in range(iterations):
        for word in test_words:
            rank = frequency_loader.get_word_rank(word, 'fr', 2000)
    end_time = time.time()
    
    total_time = end_time - start_time
    per_lookup = (total_time * 1000) / (iterations * len(test_words))
    
    print(f"   Temps total: {total_time:.4f}s")
    print(f"   Temps par lookup: {per_lookup:.4f}ms")
    print(f"   Performance: {'✅ Excellente' if per_lookup < 0.1 else '⚠️ Acceptable' if per_lookup < 1.0 else '❌ Lente'}")
    
    # Validate performance (should be very fast)
    assert per_lookup < 1.0, f"Performance too slow: {per_lookup:.4f}ms per lookup"

def test_word_ranking_cache():
    """Test that ranking cache works correctly"""
    print(f"\n=== TEST DU CACHE ===")
    
    frequency_loader = initialize_frequency_loader()
    
    # First call should build cache
    print("Premier appel (construction du cache)...")
    start_time = time.time()
    rank1 = frequency_loader.get_word_rank('le', 'fr', 2000)
    first_call_time = time.time() - start_time
    
    # Second call should use cache
    print("Deuxième appel (utilisation du cache)...")
    start_time = time.time()
    rank2 = frequency_loader.get_word_rank('le', 'fr', 2000)
    second_call_time = time.time() - start_time
    
    print(f"   Premier appel: {first_call_time:.4f}s")
    print(f"   Deuxième appel: {second_call_time:.4f}s")
    print(f"   Amélioration: {first_call_time / second_call_time:.1f}x plus rapide")
    
    # Validate cache works
    assert rank1 == rank2, "Cache should return same result"
    assert second_call_time < first_call_time, "Second call should be faster (cache hit)"
    
    print(f"\n✅ Tests du cache réussis!")

def test_word_ranking_edge_cases():
    """Test edge cases"""
    print(f"\n=== TEST DES CAS LIMITES ===")
    
    frequency_loader = initialize_frequency_loader()
    
    # Test case sensitivity
    print("1. Test de la casse:")
    rank_lower = frequency_loader.get_word_rank('le', 'fr', 2000)
    rank_upper = frequency_loader.get_word_rank('LE', 'fr', 2000)
    rank_mixed = frequency_loader.get_word_rank('Le', 'fr', 2000)
    
    print(f"   'le': {rank_lower}")
    print(f"   'LE': {rank_upper}")
    print(f"   'Le': {rank_mixed}")
    
    assert rank_lower == rank_upper == rank_mixed, "Case should not matter"
    
    # Test whitespace
    print("2. Test des espaces:")
    rank_normal = frequency_loader.get_word_rank('le', 'fr', 2000)
    rank_spaces = frequency_loader.get_word_rank('  le  ', 'fr', 2000)
    
    print(f"   'le': {rank_normal}")
    print(f"   '  le  ': {rank_spaces}")
    
    assert rank_normal == rank_spaces, "Whitespace should be stripped"
    
    # Test different top_n values
    print("3. Test de différentes valeurs top_n:")
    rank_2000 = frequency_loader.get_word_rank('le', 'fr', 2000)
    rank_1000 = frequency_loader.get_word_rank('le', 'fr', 1000)
    rank_500 = frequency_loader.get_word_rank('le', 'fr', 500)
    
    print(f"   top_n=2000: {rank_2000}")
    print(f"   top_n=1000: {rank_1000}")
    print(f"   top_n=500: {rank_500}")
    
    assert rank_2000 == rank_1000 == rank_500, "Rank should be same regardless of top_n (if word is in all ranges)"
    
    print(f"\n✅ Tests des cas limites réussis!")

def main():
    """Run all tests for Step 3.1"""
    print("🧪 TESTS ÉTAPE 3.1 : FONCTIONNALITÉ DE RANKING DES MOTS")
    print("=" * 70)
    
    try:
        test_word_ranking_basic()
        test_word_ranking_accuracy()
        test_word_ranking_performance()
        test_word_ranking_cache()
        test_word_ranking_edge_cases()
        
        print(f"\n🎉 TOUS LES TESTS ÉTAPE 3.1 RÉUSSIS!")
        print("=" * 70)
        print("✅ La méthode get_word_rank() fonctionne correctement")
        print("✅ Les rangs sont précis (ordre du fichier préservé)")
        print("✅ Les performances sont excellentes (O(1))")
        print("✅ Le cache fonctionne correctement")
        print("✅ Les cas limites sont gérés")
        print("\n🚀 Prêt pour l'Étape 3.2!")
        
    except Exception as e:
        print(f"\n❌ ÉCHEC DES TESTS ÉTAPE 3.1")
        print(f"Erreur: {e}")
        raise

if __name__ == "__main__":
    main()
