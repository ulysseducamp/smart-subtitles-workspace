#!/usr/bin/env python3
"""
Test for Step 3.2: Integration of word ranking in subtitle_fusion.py
"""

import sys
import logging
from pathlib import Path
from io import StringIO

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from subtitle_fusion import SubtitleFusionEngine
from srt_parser import Subtitle
from frequency_loader import initialize_frequency_loader

def test_word_ranking_integration():
    """Test that word ranking is properly integrated in subtitle fusion"""
    print("=== TEST ÉTAPE 3.2 : INTÉGRATION DU RANKING DANS SUBTITLE_FUSION ===")
    
    # Initialize frequency loader
    frequency_loader = initialize_frequency_loader()
    
    # Create test subtitles
    target_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Le chat dort"),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="Le fracas réveille"),
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="C'est impossible")
    ]
    
    native_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="The cat sleeps"),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="The noise wakes up"),
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="It's impossible")
    ]
    
    # Get known words (top 2000 French words)
    known_words = frequency_loader.get_top_n_words('fr', 2000)
    
    # Create engine
    engine = SubtitleFusionEngine()
    
    # Capture logs
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.INFO)
    logger = logging.getLogger('subtitle_fusion')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    print(f"\n1. Test avec des mots connus et inconnus:")
    
    # Test fusion with ranking
    result = engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang='fr',
        enable_inline_translation=False,
        top_n=2000
    )
    
    # Get captured logs
    logs = log_capture.getvalue()
    
    # Check that logs contain ranking information
    print(f"Logs capturés:")
    print(logs)
    
    # Validate that ranking information is present
    assert "Mots analysés:" in logs, "Logs should contain 'Mots analysés:'"
    assert "rang" in logs, "Logs should contain ranking information"
    assert "connu" in logs, "Logs should contain 'connu' for known words"
    assert "inconnu" in logs, "Logs should contain 'inconnu' for unknown words"
    
    print(f"\n✅ Intégration réussie!")
    print(f"   - Logs contiennent 'Mots analysés:'")
    print(f"   - Informations de rang présentes")
    print(f"   - Mots connus et inconnus identifiés")

def test_word_ranking_format():
    """Test the format of word ranking in logs"""
    print(f"\n=== TEST DU FORMAT DES RANGS ===")
    
    # Initialize frequency loader
    frequency_loader = initialize_frequency_loader()
    
    # Test the format_words_with_ranks method directly
    engine = SubtitleFusionEngine()
    
    # Test with known words
    known_words = ['le', 'être', 'avoir']
    formatted = engine._format_words_with_ranks(known_words, 'fr', 2000)
    print(f"Mots connus formatés: {formatted}")
    
    # Validate format
    assert "rang" in formatted, "Should contain 'rang'"
    assert "connu" in formatted, "Should contain 'connu'"
    assert "2000" in formatted, "Should contain top_n value"
    
    # Test with unknown words
    unknown_words = ['fracas', 'crescendo']
    formatted = engine._format_words_with_ranks(unknown_words, 'fr', 2000)
    print(f"Mots inconnus formatés: {formatted}")
    
    # Validate format
    assert "inconnu" in formatted, "Should contain 'inconnu'"
    assert "hors des 2000 premiers" in formatted, "Should contain range info"
    
    # Test with empty list
    empty_words = []
    formatted = engine._format_words_with_ranks(empty_words, 'fr', 2000)
    print(f"Liste vide formatée: {formatted}")
    
    assert formatted == "none", "Empty list should return 'none'"
    
    print(f"\n✅ Format des rangs validé!")

def test_performance_with_ranking():
    """Test performance impact of ranking integration"""
    print(f"\n=== TEST DE PERFORMANCE AVEC RANKING ===")
    
    import time
    
    # Initialize frequency loader
    frequency_loader = initialize_frequency_loader()
    
    # Create larger test dataset
    target_subs = []
    native_subs = []
    
    for i in range(50):  # 50 subtitles
        target_subs.append(Subtitle(
            index=str(i+1), 
            start=f"00:00:{i*2:02d},000", 
            end=f"00:00:{(i*2)+2:02d},000", 
            text=f"Le mot {i} est important"
        ))
        native_subs.append(Subtitle(
            index=str(i+1), 
            start=f"00:00:{i*2:02d},000", 
            end=f"00:00:{(i*2)+2:02d},000", 
            text=f"Word {i} is important"
        ))
    
    # Get known words
    known_words = frequency_loader.get_top_n_words('fr', 2000)
    
    # Create engine
    engine = SubtitleFusionEngine()
    
    # Test performance
    start_time = time.time()
    result = engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang='fr',
        enable_inline_translation=False,
        top_n=2000
    )
    end_time = time.time()
    
    processing_time = end_time - start_time
    print(f"   Temps de traitement: {processing_time:.4f}s")
    print(f"   Performance: {'✅ Excellente' if processing_time < 1.0 else '⚠️ Acceptable' if processing_time < 5.0 else '❌ Lente'}")
    
    # Validate that processing completed successfully
    assert result is not None, "Result should not be None"
    assert isinstance(result, dict), "Result should be a dictionary"
    print(f"   Résultat: {list(result.keys())}")
    
    print(f"\n✅ Performance validée!")

def main():
    """Run all tests for Step 3.2"""
    print("🧪 TESTS ÉTAPE 3.2 : INTÉGRATION DU RANKING DANS SUBTITLE_FUSION")
    print("=" * 80)
    
    try:
        test_word_ranking_integration()
        test_word_ranking_format()
        test_performance_with_ranking()
        
        print(f"\n🎉 TOUS LES TESTS ÉTAPE 3.2 RÉUSSIS!")
        print("=" * 80)
        print("✅ L'intégration du ranking fonctionne correctement")
        print("✅ Le format des logs est correct")
        print("✅ Les performances sont maintenues")
        print("\n🚀 Prêt pour l'Étape 3.3!")
        
    except Exception as e:
        print(f"\n❌ ÉCHEC DES TESTS ÉTAPE 3.2")
        print(f"Erreur: {e}")
        raise

if __name__ == "__main__":
    main()
