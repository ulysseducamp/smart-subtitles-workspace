#!/usr/bin/env python3
"""
Debug script to understand the ranking inconsistency issue.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from frequency_loader import initialize_frequency_loader

def debug_ranking_issue():
    """Debug the ranking inconsistency"""
    print("=== DEBUG DU PROBLÈME DE RANKING ===")
    
    frequency_loader = initialize_frequency_loader()
    
    # Load French words
    french_words = frequency_loader.get_top_n_words('fr', 2000)
    print(f"Nombre de mots chargés: {len(french_words)}")
    
    # Convert to list
    words_list = list(french_words)
    print(f"Nombre de mots dans la liste: {len(words_list)}")
    
    # Test specific words
    test_words = ['le', 'être', 'avoir', 'que', 'dans']
    
    print(f"\nAnalyse détaillée:")
    for word in test_words:
        print(f"\nMot: '{word}'")
        print(f"  Dans le set: {word in french_words}")
        
        if word in french_words:
            # Method 1: index in list
            list_index = words_list.index(word)
            print(f"  Index dans la liste: {list_index}")
            print(f"  Rang (1-indexed): {list_index + 1}")
            
            # Method 2: check original file order
            filename = "src/frequency_lists/fr-5000.txt"
            with open(filename, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if line.strip().lower() == word:
                        print(f"  Rang dans le fichier original: {i}")
                        break
                else:
                    print(f"  Mot non trouvé dans le fichier original!")
    
    # Check if set order is different from file order
    print(f"\n=== VÉRIFICATION DE L'ORDRE ===")
    print("Premiers 10 mots du fichier original:")
    with open("src/frequency_lists/fr-5000.txt", 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if i > 10:
                break
            word = line.strip().lower()
            print(f"  {i}. '{word}'")
    
    print(f"\nPremiers 10 mots du set (ordre arbitraire):")
    for i, word in enumerate(list(french_words)[:10], 1):
        print(f"  {i}. '{word}'")

if __name__ == "__main__":
    debug_ranking_issue()
