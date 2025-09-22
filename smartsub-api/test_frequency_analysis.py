#!/usr/bin/env python3
"""
Test script to analyze current frequency loader behavior and performance
for implementing word ranking functionality.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from frequency_loader import initialize_frequency_loader

def test_current_behavior():
    """Test current frequency loader behavior"""
    print("=== ANALYSE DU COMPORTEMENT ACTUEL ===")
    
    # Initialize frequency loader
    frequency_loader = initialize_frequency_loader()
    
    # Test with French words
    print("\n1. Test avec des mots français (top 2000):")
    french_words = frequency_loader.get_top_n_words('fr', 2000)
    print(f"   Nombre de mots chargés: {len(french_words)}")
    
    # Test some known words
    test_words = ['le', 'être', 'avoir', 'que', 'dans', 'ce', 'il', 'qui', 'pas', 'pour']
    print(f"\n2. Test de présence de mots connus:")
    for word in test_words:
        is_present = word in french_words
        print(f"   '{word}': {'✅ présent' if is_present else '❌ absent'}")
    
    # Test some unknown words
    unknown_words = ['fracas', 'crescendo', 'démarre', 'déclic', 'verrouillage']
    print(f"\n3. Test de présence de mots inconnus:")
    for word in unknown_words:
        is_present = word in french_words
        print(f"   '{word}': {'✅ présent' if is_present else '❌ absent'}")
    
    # Performance test
    print(f"\n4. Test de performance (1000 lookups):")
    start_time = time.time()
    for i in range(1000):
        test_word = 'le' if i % 2 == 0 else 'fracas'
        _ = test_word in french_words
    end_time = time.time()
    print(f"   1000 lookups en {end_time - start_time:.4f} secondes")
    print(f"   Performance: {(end_time - start_time) * 1000:.2f} ms pour 1000 lookups")

def analyze_frequency_file_structure():
    """Analyze the structure of frequency files"""
    print("\n=== ANALYSE DE LA STRUCTURE DES FICHIERS ===")
    
    frequency_lists_dir = Path("src/frequency_lists")
    fr_file = frequency_lists_dir / "fr-5000.txt"
    
    if fr_file.exists():
        print(f"\n1. Analyse du fichier {fr_file.name}:")
        with open(fr_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"   Nombre total de lignes: {len(lines)}")
        print(f"   Premiers 10 mots:")
        for i, line in enumerate(lines[:10], 1):
            word = line.strip()
            print(f"     {i}. '{word}'")
        
        print(f"   Derniers 10 mots:")
        for i, line in enumerate(lines[-10:], len(lines)-9):
            word = line.strip()
            print(f"     {i}. '{word}'")
    else:
        print(f"❌ Fichier {fr_file} non trouvé")

def test_ranking_requirements():
    """Test what we need for ranking functionality"""
    print("\n=== ANALYSE DES BESOINS POUR LE RANKING ===")
    
    frequency_loader = initialize_frequency_loader()
    french_words = frequency_loader.get_top_n_words('fr', 2000)
    
    # Convert set to list to get ranking
    words_list = list(french_words)
    print(f"1. Conversion Set -> List:")
    print(f"   Nombre de mots: {len(words_list)}")
    print(f"   Type: {type(words_list)}")
    
    # Test ranking lookup
    print(f"\n2. Test de recherche de rang:")
    test_words = ['le', 'être', 'avoir', 'fracas', 'crescendo']
    
    for word in test_words:
        if word in words_list:
            rank = words_list.index(word) + 1  # 1-indexed
            print(f"   '{word}': rang {rank}/{len(words_list)}")
        else:
            print(f"   '{word}': absent (hors des {len(words_list)} premiers)")
    
    # Performance test for ranking
    print(f"\n3. Test de performance pour le ranking:")
    start_time = time.time()
    for i in range(100):
        test_word = 'le' if i % 2 == 0 else 'fracas'
        if test_word in words_list:
            rank = words_list.index(test_word) + 1
    end_time = time.time()
    print(f"   100 ranking lookups en {end_time - start_time:.4f} secondes")
    print(f"   Performance: {(end_time - start_time) * 10:.2f} ms pour 100 lookups")

if __name__ == "__main__":
    test_current_behavior()
    analyze_frequency_file_structure()
    test_ranking_requirements()
