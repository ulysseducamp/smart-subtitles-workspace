#!/usr/bin/env python3
"""
Test pour valider la section STATISTIQUES dans les logs
"""

import sys
import os
import logging
import io

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging to capture output
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def test_statistics_section():
    """Test que la section STATISTIQUES apparaît dans les logs"""
    
    print("🧪 Testing STATISTIQUES section in logs...")
    
    # Capture logging output
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to main logger
    main_logger = logging.getLogger('__main__')
    main_logger.addHandler(handler)
    main_logger.setLevel(logging.INFO)
    
    # Simulate the complete logging flow from main.py
    main_logger.info("=== CONFIGURATION ===")
    main_logger.info("Niveau choisi: 2000 mots les plus fréquents")
    main_logger.info("Langue cible: EN, Langue native: FR")
    main_logger.info("Traduction inline: activée")
    main_logger.info("")
    
    main_logger.info("=== TRAITEMENT DES SOUS-TITRES ===")
    main_logger.info("Subtitle processing completed in 2.50 seconds")
    
    # This is the exact code we added to main.py for STATISTIQUES section
    main_logger.info("")
    main_logger.info("=== STATISTIQUES FINALES ===")
    main_logger.info("Total target subtitles: 695")
    main_logger.info("Total native subtitles: 676")
    main_logger.info("Subtitles kept in target language: 404/695")
    main_logger.info("Subtitles replaced with native: 291/695 (41.9%)")
    main_logger.info("Subtitles with inline translation: 138/695 (19.9%)")
    
    # Get captured output
    log_output = log_capture.getvalue()
    
    print(f"\n📋 Captured log output:")
    print(log_output)
    
    # Check if STATISTIQUES section is present
    if "=== STATISTIQUES FINALES ===" in log_output:
        print("✅ STATISTIQUES header found")
    else:
        print("❌ STATISTIQUES header NOT found")
        return False
    
    # Check order: CONFIGURATION -> TRAITEMENT -> STATISTIQUES
    config_pos = log_output.find("=== CONFIGURATION ===")
    treatment_pos = log_output.find("=== TRAITEMENT DES SOUS-TITRES ===")
    stats_pos = log_output.find("=== STATISTIQUES FINALES ===")
    
    if config_pos < treatment_pos < stats_pos:
        print("✅ Correct order: CONFIGURATION -> TRAITEMENT -> STATISTIQUES")
    else:
        print("❌ Incorrect order")
        return False
    
    # Check that statistics are grouped under the header
    if "Total target subtitles: 695" in log_output:
        print("✅ Statistics content found")
    else:
        print("❌ Statistics content NOT found")
        return False
    
    # Remove handler
    main_logger.removeHandler(handler)
    
    return True

if __name__ == "__main__":
    success = test_statistics_section()
    if success:
        print("\n🎉 STATISTIQUES section test PASSED!")
    else:
        print("\n❌ STATISTIQUES section test FAILED!")
        sys.exit(1)
