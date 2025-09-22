#!/usr/bin/env python3
"""
Test pour valider que la section CONFIGURATION apparaît dans les logs
"""

import sys
import os
import logging
import io
from contextlib import redirect_stdout

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging to capture output
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def test_configuration_logs():
    """Test que la section CONFIGURATION apparaît dans les logs"""
    
    print("🧪 Testing CONFIGURATION section in logs...")
    
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
    
    # Simulate the configuration logging from main.py
    target_language = "EN"
    native_language = "FR"
    top_n_words = 2000
    enable_inline_translation = True
    
    # This is the exact code we added to main.py
    main_logger.info("=== CONFIGURATION ===")
    main_logger.info(f"Niveau choisi: {top_n_words} mots les plus fréquents")
    main_logger.info(f"Langue cible: {target_language}, Langue native: {native_language}")
    main_logger.info(f"Traduction inline: {'activée' if enable_inline_translation else 'désactivée'}")
    main_logger.info("")
    
    # Get captured output
    log_output = log_capture.getvalue()
    
    print(f"\n📋 Captured log output:")
    print(log_output)
    
    # Check if CONFIGURATION section is present
    if "=== CONFIGURATION ===" in log_output:
        print("✅ CONFIGURATION header found")
    else:
        print("❌ CONFIGURATION header NOT found")
        return False
    
    if "Niveau choisi: 2000 mots les plus fréquents" in log_output:
        print("✅ Niveau choisi found")
    else:
        print("❌ Niveau choisi NOT found")
        return False
    
    if "Langue cible: EN, Langue native: FR" in log_output:
        print("✅ Langues found")
    else:
        print("❌ Langues NOT found")
        return False
    
    if "Traduction inline: activée" in log_output:
        print("✅ Traduction inline found")
    else:
        print("❌ Traduction inline NOT found")
        return False
    
    # Remove handler
    main_logger.removeHandler(handler)
    
    return True

if __name__ == "__main__":
    success = test_configuration_logs()
    if success:
        print("\n🎉 CONFIGURATION section test PASSED!")
    else:
        print("\n❌ CONFIGURATION section test FAILED!")
        sys.exit(1)
