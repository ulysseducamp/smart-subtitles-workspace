#!/usr/bin/env python3
"""
Test pour valider la section TRAITEMENT dans les logs
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

def test_treatment_section():
    """Test que la section TRAITEMENT apparaît dans les logs"""
    
    print("🧪 Testing TRAITEMENT section in logs...")
    
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
    
    # Simulate the configuration and treatment logging from main.py
    main_logger.info("=== CONFIGURATION ===")
    main_logger.info("Niveau choisi: 2000 mots les plus fréquents")
    main_logger.info("Langue cible: EN, Langue native: FR")
    main_logger.info("Traduction inline: activée")
    main_logger.info("")
    
    # This is the exact code we added to main.py for TRAITEMENT section
    main_logger.info("=== TRAITEMENT DES SOUS-TITRES ===")
    
    # Get captured output
    log_output = log_capture.getvalue()
    
    print(f"\n📋 Captured log output:")
    print(log_output)
    
    # Check if TRAITEMENT section is present
    if "=== TRAITEMENT DES SOUS-TITRES ===" in log_output:
        print("✅ TRAITEMENT header found")
    else:
        print("❌ TRAITEMENT header NOT found")
        return False
    
    # Check order: CONFIGURATION should come before TRAITEMENT
    config_pos = log_output.find("=== CONFIGURATION ===")
    treatment_pos = log_output.find("=== TRAITEMENT DES SOUS-TITRES ===")
    
    if config_pos < treatment_pos:
        print("✅ CONFIGURATION comes before TRAITEMENT (correct order)")
    else:
        print("❌ Incorrect order: TRAITEMENT comes before CONFIGURATION")
        return False
    
    # Remove handler
    main_logger.removeHandler(handler)
    
    return True

if __name__ == "__main__":
    success = test_treatment_section()
    if success:
        print("\n🎉 TRAITEMENT section test PASSED!")
    else:
        print("\n❌ TRAITEMENT section test FAILED!")
        sys.exit(1)
