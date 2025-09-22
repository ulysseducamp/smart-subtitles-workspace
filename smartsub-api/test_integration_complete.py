#!/usr/bin/env python3
"""
Test d'intégration complet pour valider que les logs sont parfaitement ordonnés
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import initialize_frequency_loader
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def test_integration_complete():
    """Test d'intégration complet avec des sous-titres réels"""
    print("=== TEST D'INTÉGRATION COMPLET ===")
    
    # Initialiser le frequency loader
    frequency_loader = initialize_frequency_loader()
    print("✅ Frequency loader initialisé")
    
    # Créer l'engine
    engine = SubtitleFusionEngine()
    print("✅ Engine créé")
    
    # Créer des sous-titres de test
    from srt_parser import Subtitle
    
    target_subs = [
        Subtitle(index="1", start=0.0, end=2.0, text="[fracas]"),
        Subtitle(index="2", start=2.0, end=4.0, text="[musique inquiétante]"),
        Subtitle(index="3", start=4.0, end=6.0, text="Tu devrais le savoir."),
        Subtitle(index="4", start=6.0, end=8.0, text="C'est un test complexe."),
        Subtitle(index="5", start=8.0, end=10.0, text="[son mystérieux]"),
    ]
    
    native_subs = [
        Subtitle(index="1", start=0.0, end=2.0, text="[crash]"),
        Subtitle(index="2", start=2.0, end=4.0, text="[ominous music]"),
        Subtitle(index="3", start=4.0, end=6.0, text="You should know."),
        Subtitle(index="4", start=6.0, end=8.0, text="This is a complex test."),
        Subtitle(index="5", start=8.0, end=10.0, text="[mysterious sound]"),
    ]
    
    # Mots connus (simulation)
    known_words = {
        "tu", "devoir", "le", "savoir", "musique", "inquiétant", 
        "c'est", "un", "test", "complexe", "son", "mystérieux"
    }
    
    print("🔄 Test de fusion des sous-titres...")
    print("📝 Vérifiez que les logs sont parfaitement ordonnés et atomiques")
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
    print(f"📊 Résultat: {len(result.get('output_srt', []))} sous-titres traités")
    print("🔍 Vérifiez que les logs sont bien structurés et non mélangés")

if __name__ == "__main__":
    test_integration_complete()
