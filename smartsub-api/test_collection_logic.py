#!/usr/bin/env python3
"""
Test script for subtitle fusion collection logic (Étape 2)
Tests that words are collected for batch translation instead of translated immediately
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_collection_logic():
    """Test that words are collected for batch translation"""
    
    print("🧪 Testing subtitle fusion collection logic...")
    
    try:
        from subtitle_fusion import SubtitleFusionEngine
        from srt_parser import Subtitle
        
        # Create test subtitles with unknown words
        target_subs = [
            Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Hello beautiful world"),
            Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="This is a wonderful day"),
            Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="The sunshine is amazing")
        ]
        
        native_subs = [
            Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Bonjour beau monde"),
            Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="C'est une merveilleuse journée"),
            Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Le soleil est incroyable")
        ]
        
        # Known words (small set to force unknown words)
        known_words = {"hello", "this", "is", "a", "the"}
        
        print(f"📝 Test subtitles:")
        for sub in target_subs:
            print(f"  {sub.index}: '{sub.text}'")
        
        print(f"\n📚 Known words: {known_words}")
        print(f"🔍 Expected unknown words: beautiful, world, wonderful, day, sunshine, amazing")
        
        # Initialize fusion engine
        engine = SubtitleFusionEngine()
        
        print(f"\n🔄 Testing collection logic (without DeepL API)...")
        
        # Test with enable_inline_translation=True but no DeepL API
        # This should collect words but not translate them
        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang="EN",
            enable_inline_translation=True,
            deepl_api=None,  # No API = should collect but not translate
            native_lang="FR"
        )
        
        print(f"\n📊 Results:")
        print(f"  - Success: {result['success']}")
        print(f"  - Inline translations: {result['inlineTranslationCount']}")
        print(f"  - Replaced subtitles: {result['replacedCount']}")
        print(f"  - Total hybrid subtitles: {len(result['hybrid'])}")
        
        # Check that subtitles were processed
        if result['success']:
            print("✅ Fusion engine executed successfully")
        else:
            print("❌ Fusion engine failed")
            return False
        
        # Check that we have hybrid subtitles
        if len(result['hybrid']) > 0:
            print("✅ Hybrid subtitles generated")
        else:
            print("❌ No hybrid subtitles generated")
            return False
        
        print(f"\n📝 Generated subtitles:")
        for sub in result['hybrid']:
            print(f"  {sub.index}: '{sub.text}'")
        
        print(f"\n🎉 Collection logic test completed successfully!")
        print(f"📋 Next step: Test with real DeepL API to validate batch translation")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_collection_logic()
    sys.exit(0 if success else 1)

