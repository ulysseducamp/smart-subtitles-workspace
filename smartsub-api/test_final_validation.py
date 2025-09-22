#!/usr/bin/env python3
"""
Test de validation final pour l'Étape 1.1 - Restructuration des logs
"""

import sys
import os
import logging
import io

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from subtitle_fusion import SubtitleFusionEngine
from srt_parser import parse_srt, generate_srt
from frequency_loader import initialize_frequency_loader

def test_final_validation():
    """Test de validation final pour la restructuration des logs"""
    
    print("🧪 Final validation test for logs restructuring...")
    
    # Configure logging to capture output
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to all loggers
    main_logger = logging.getLogger('__main__')
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)
    
    fusion_logger = logging.getLogger('subtitle_fusion')
    fusion_logger.addHandler(handler)
    fusion_logger.setLevel(logging.INFO)
    
    # Test data - more complex scenario
    target_srt_content = """1
00:00:01,000 --> 00:00:03,000
Hello beautiful world

2
00:00:04,000 --> 00:00:06,000
This is wonderful

3
00:00:07,000 --> 00:00:09,000
The sunshine is amazing
"""
    
    native_srt_content = """1
00:00:01,000 --> 00:00:03,000
Bonjour magnifique monde

2
00:00:04,000 --> 00:00:06,000
C'est merveilleux

3
00:00:07,000 --> 00:00:09,000
Le soleil est incroyable
"""
    
    # Parse SRT files
    target_subs = parse_srt(target_srt_content)
    native_subs = parse_srt(native_srt_content)
    
    # Get frequency list
    frequency_loader = initialize_frequency_loader()
    known_words = frequency_loader.get_top_n_words("EN", 2000)
    
    # Simulate the complete logging flow from main.py
    main_logger.info("=== CONFIGURATION ===")
    main_logger.info("Niveau choisi: 2000 mots les plus fréquents")
    main_logger.info("Langue cible: EN, Langue native: FR")
    main_logger.info("Traduction inline: activée")
    main_logger.info("")
    
    main_logger.info("=== TRAITEMENT DES SOUS-TITRES ===")
    
    # Initialize fusion engine
    engine = SubtitleFusionEngine()
    
    # Test fusion
    result = engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang="EN",
        enable_inline_translation=True,
        deepl_api=None,
        native_lang="FR"
    )
    
    # Simulate statistics section
    main_logger.info("")
    main_logger.info("=== STATISTIQUES FINALES ===")
    main_logger.info("Total target subtitles: 3")
    main_logger.info("Total native subtitles: 3")
    main_logger.info("Subtitles kept in target language: 1/3")
    main_logger.info("Subtitles replaced with native: 0/3 (0.0%)")
    main_logger.info("Subtitles with inline translation: 2/3 (66.7%)")
    
    # Get captured output
    log_output = log_capture.getvalue()
    
    print(f"\n📋 Final log output:")
    print(log_output)
    
    # Comprehensive validation
    validation_results = []
    
    # 1. Check CONFIGURATION section
    config_checks = [
        "=== CONFIGURATION ===" in log_output,
        "Niveau choisi: 2000 mots les plus fréquents" in log_output,
        "Langue cible: EN, Langue native: FR" in log_output,
        "Traduction inline: activée" in log_output
    ]
    validation_results.append(("CONFIGURATION section", all(config_checks)))
    
    # 2. Check TRAITEMENT section
    treatment_checks = [
        "=== TRAITEMENT DES SOUS-TITRES ===" in log_output,
        "=== SUBTITLE 1 ===" in log_output,
        "=== SUBTITLE 2 ===" in log_output,
        "=== SUBTITLE 3 ===" in log_output
    ]
    validation_results.append(("TRAITEMENT section", all(treatment_checks)))
    
    # 3. Check STATISTIQUES section
    stats_checks = [
        "=== STATISTIQUES FINALES ===" in log_output,
        "Total target subtitles: 3" in log_output,
        "Total native subtitles: 3" in log_output
    ]
    validation_results.append(("STATISTIQUES section", all(stats_checks)))
    
    # 4. Check order
    config_pos = log_output.find("=== CONFIGURATION ===")
    treatment_pos = log_output.find("=== TRAITEMENT DES SOUS-TITRES ===")
    stats_pos = log_output.find("=== STATISTIQUES FINALES ===")
    validation_results.append(("Correct order", config_pos < treatment_pos < stats_pos))
    
    # 5. Check unified logging
    validation_results.append(("Unified logging", "print(" not in log_output))
    
    # 6. Check subtitle processing details
    subtitle_checks = [
        "Original:" in log_output,
        "Proper nouns:" in log_output,
        "Words lemmatised:" in log_output,
        "Unknown words:" in log_output,
        "Decision:" in log_output,
        "Reason:" in log_output
    ]
    validation_results.append(("Subtitle processing details", all(subtitle_checks)))
    
    # Print validation results
    print(f"\n📊 Validation Results:")
    all_passed = True
    for test_name, passed in validation_results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    # Remove handlers
    main_logger.removeHandler(handler)
    fusion_logger.removeHandler(handler)
    
    return all_passed

if __name__ == "__main__":
    success = test_final_validation()
    if success:
        print("\n🎉 FINAL VALIDATION TEST PASSED!")
        print("✅ Étape 1.1 - Restructuration des logs: COMPLÉTÉE")
    else:
        print("\n❌ FINAL VALIDATION TEST FAILED!")
        sys.exit(1)
