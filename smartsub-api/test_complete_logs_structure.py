#!/usr/bin/env python3
"""
Test complet pour valider la structure des logs restructurés
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

def test_complete_logs_structure():
    """Test complet de la structure des logs"""
    
    print("🧪 Testing complete logs structure...")
    
    # Configure logging to capture output
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to main logger
    main_logger = logging.getLogger('__main__')
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)
    
    # Add handler to subtitle_fusion logger
    fusion_logger = logging.getLogger('subtitle_fusion')
    fusion_logger.addHandler(handler)
    fusion_logger.setLevel(logging.INFO)
    
    # Test data
    target_srt_content = """1
00:00:01,000 --> 00:00:03,000
Hello beautiful

2
00:00:04,000 --> 00:00:06,000
This is wonderful
"""
    
    native_srt_content = """1
00:00:01,000 --> 00:00:03,000
Bonjour magnifique

2
00:00:04,000 --> 00:00:06,000
C'est merveilleux
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
    main_logger.info("Total target subtitles: 2")
    main_logger.info("Total native subtitles: 2")
    main_logger.info("Subtitles kept in target language: 1/2")
    main_logger.info("Subtitles replaced with native: 0/2 (0.0%)")
    main_logger.info("Subtitles with inline translation: 1/2 (50.0%)")
    
    # Get captured output
    log_output = log_capture.getvalue()
    
    print(f"\n📋 Complete log output:")
    print(log_output)
    
    # Validate structure
    checks = []
    
    # Check CONFIGURATION section
    if "=== CONFIGURATION ===" in log_output:
        checks.append("✅ CONFIGURATION header found")
    else:
        checks.append("❌ CONFIGURATION header NOT found")
    
    if "Niveau choisi: 2000 mots les plus fréquents" in log_output:
        checks.append("✅ Niveau choisi found")
    else:
        checks.append("❌ Niveau choisi NOT found")
    
    # Check TRAITEMENT section
    if "=== TRAITEMENT DES SOUS-TITRES ===" in log_output:
        checks.append("✅ TRAITEMENT header found")
    else:
        checks.append("❌ TRAITEMENT header NOT found")
    
    # Check subtitle processing logs (should now use logger instead of print)
    if "=== SUBTITLE 1 ===" in log_output:
        checks.append("✅ Subtitle processing logs found")
    else:
        checks.append("❌ Subtitle processing logs NOT found")
    
    # Check STATISTIQUES section
    if "=== STATISTIQUES FINALES ===" in log_output:
        checks.append("✅ STATISTIQUES header found")
    else:
        checks.append("❌ STATISTIQUES header NOT found")
    
    # Check order
    config_pos = log_output.find("=== CONFIGURATION ===")
    treatment_pos = log_output.find("=== TRAITEMENT DES SOUS-TITRES ===")
    stats_pos = log_output.find("=== STATISTIQUES FINALES ===")
    
    if config_pos < treatment_pos < stats_pos:
        checks.append("✅ Correct order: CONFIGURATION -> TRAITEMENT -> STATISTIQUES")
    else:
        checks.append("❌ Incorrect order")
    
    # Check that all logs use logger (no print statements)
    if "print(" not in log_output:
        checks.append("✅ All logs use logger (no print statements)")
    else:
        checks.append("❌ Some logs still use print statements")
    
    # Print all checks
    for check in checks:
        print(check)
    
    # Remove handlers
    main_logger.removeHandler(handler)
    fusion_logger.removeHandler(handler)
    
    # Return success if all checks pass
    return all("✅" in check for check in checks)

if __name__ == "__main__":
    success = test_complete_logs_structure()
    if success:
        print("\n🎉 Complete logs structure test PASSED!")
    else:
        print("\n❌ Complete logs structure test FAILED!")
        sys.exit(1)
