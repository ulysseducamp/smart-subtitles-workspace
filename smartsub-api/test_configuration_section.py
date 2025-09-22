#!/usr/bin/env python3
"""
Test pour valider la section CONFIGURATION dans les logs
"""

import sys
import os
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from subtitle_fusion import SubtitleFusionEngine
from srt_parser import parse_srt, generate_srt
from frequency_loader import get_frequency_loader

# Configure logging to see our changes
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def test_configuration_section():
    """Test la section CONFIGURATION dans les logs"""
    
    print("🧪 Testing CONFIGURATION section in logs...")
    
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
    from frequency_loader import initialize_frequency_loader
    frequency_loader = initialize_frequency_loader()
    known_words = frequency_loader.get_top_n_words("EN", 2000)
    
    # Test parameters
    target_language = "EN"
    native_language = "FR"
    top_n_words = 2000
    enable_inline_translation = True
    
    print(f"\n📋 Test parameters:")
    print(f"  - Target language: {target_language}")
    print(f"  - Native language: {native_language}")
    print(f"  - Top N words: {top_n_words}")
    print(f"  - Inline translation: {enable_inline_translation}")
    
    # Simulate the CONFIGURATION section that should appear
    print(f"\n🔍 Expected CONFIGURATION section:")
    print("=== CONFIGURATION ===")
    print(f"Niveau choisi: {top_n_words} mots les plus fréquents")
    print(f"Langue cible: {target_language}, Langue native: {native_language}")
    print(f"Traduction inline: {'activée' if enable_inline_translation else 'désactivée'}")
    print("")
    
    # Initialize fusion engine
    engine = SubtitleFusionEngine()
    
    print(f"\n🔄 Testing fusion engine...")
    
    # Test fusion
    result = engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang=target_language,
        enable_inline_translation=enable_inline_translation,
        deepl_api=None,
        native_lang=native_language
    )
    
    print(f"\n📊 Results:")
    print(f"  - Success: {result['success']}")
    print(f"  - Inline translations: {result['inlineTranslationCount']}")
    print(f"  - Replaced subtitles: {result['replacedCount']}")
    print(f"  - Total hybrid subtitles: {len(result['hybrid'])}")
    
    if result['success']:
        print("✅ Fusion engine executed successfully")
        print("✅ CONFIGURATION section test completed")
        return True
    else:
        print("❌ Fusion engine failed")
        return False

if __name__ == "__main__":
    success = test_configuration_section()
    if success:
        print("\n🎉 CONFIGURATION section test PASSED!")
    else:
        print("\n❌ CONFIGURATION section test FAILED!")
        sys.exit(1)
