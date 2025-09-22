#!/usr/bin/env python3
"""
Test pour valider que les logs sont affichés dans le bon ordre
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import initialize_frequency_loader
from srt_parser import Subtitle
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def test_ordered_logs():
    """Test pour valider l'ordre des logs"""
    print("=== TEST DE L'ORDRE DES LOGS ===")
    
    # Initialiser le frequency loader
    frequency_loader = initialize_frequency_loader()
    print("✅ Frequency loader initialisé")
    
    # Créer l'engine
    engine = SubtitleFusionEngine()
    print("✅ Engine créé")
    
    # Créer des sous-titres de test avec des indices non-séquentiels
    target_subs = [
        Subtitle(index="1", start=0.0, end=2.0, text="[fracas]"),
        Subtitle(index="3", start=2.0, end=4.0, text="[musique inquiétante]"),
        Subtitle(index="5", start=4.0, end=6.0, text="Tu devrais le savoir."),
        Subtitle(index="7", start=6.0, end=8.0, text="C'est un test complexe."),
        Subtitle(index="9", start=8.0, end=10.0, text="[son mystérieux]"),
    ]
    
    native_subs = [
        Subtitle(index="1", start=0.0, end=2.0, text="[crash]"),
        Subtitle(index="3", start=2.0, end=4.0, text="[ominous music]"),
        Subtitle(index="5", start=4.0, end=6.0, text="You should know."),
        Subtitle(index="7", start=6.0, end=8.0, text="This is a complex test."),
        Subtitle(index="9", start=8.0, end=10.0, text="[mysterious sound]"),
    ]
    
    # Mots connus (simulation)
    known_words = {
        "tu", "devoir", "le", "savoir", "musique", "inquiétant", 
        "c'est", "un", "test", "complexe", "son", "mystérieux"
    }
    
    print("🔄 Test de fusion des sous-titres...")
    print("📝 Vérifiez que les logs sont dans l'ordre : 1, 3, 5, 7, 9")
    print("")
    
    # Test de fusion
    result = engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang="fr",
        enable_inline_translation=True,
        deepl_api=None,  # Pas de DeepL pour ce test
        native_lang="en",
        top_n=2000
    )
    
    print("")
    print("✅ Test terminé!")
    print(f"📊 Résultat: {len(result.get('hybrid', []))} sous-titres traités")
    print("🔍 Vérifiez que les logs sont dans l'ordre correct : 1, 3, 5, 7, 9")

if __name__ == "__main__":
    test_ordered_logs()
