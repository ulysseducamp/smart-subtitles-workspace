#!/usr/bin/env python3
"""
Test de la fonction helper _log_subtitle_details
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from subtitle_fusion import SubtitleFusionEngine
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def test_helper_function():
    """Test de la fonction helper _log_subtitle_details"""
    print("=== TEST DE LA FONCTION HELPER ===")
    
    # Créer l'engine
    engine = SubtitleFusionEngine()
    
    # Test avec différents cas
    test_cases = [
        {
            'subtitle_index': '1',
            'original_text': '[fracas]',
            'proper_nouns': [],
            'words_ranks': 'fracas → inconnu (hors des 2000 premiers)',
            'unknown_words': ['fracas'],
            'decision': 'inline translation for single unknown word (COLLECTED FOR BATCH)',
            'reason': '1 unknown word detected, collecting original word \'[fracas]\' (lemmatized: \'fracas\') for batch translation',
            'final_text': '[fracas]'
        },
        {
            'subtitle_index': '2',
            'original_text': '[musique inquiétante]',
            'proper_nouns': [],
            'words_ranks': 'musique → rang 1138/2000 (connu), inquiétant → rang 1996/2000 (connu)',
            'unknown_words': [],
            'decision': 'kept in target language',
            'reason': 'all words are known or proper nouns',
            'final_text': '[musique inquiétante]'
        },
        {
            'subtitle_index': '3',
            'original_text': 'Tu devrais le savoir.',
            'proper_nouns': [],
            'words_ranks': 'tu → rang 111/2000 (connu), devoir → rang 40/2000 (connu), le → rang 4/2000 (connu), savoir → rang 68/2000 (connu)',
            'unknown_words': [],
            'decision': 'kept in target language',
            'reason': 'all words are known or proper nouns',
            'final_text': 'Tu devrais le savoir.'
        }
    ]
    
    print("🔄 Test de la fonction helper avec différents cas...")
    print("📝 Vérifiez que les logs sont bien formatés et atomiques")
    print("")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"--- Test Case {i} ---")
        engine._log_subtitle_details(**test_case)
        print("")
    
    print("✅ Test terminé - Vérifiez que les logs sont bien structurés!")

if __name__ == "__main__":
    test_helper_function()
