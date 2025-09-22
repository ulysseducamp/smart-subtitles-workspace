#!/usr/bin/env python3
"""
Test script for batch translation integration (Étape 3)
Tests the complete batch translation workflow with real DeepL API
"""

import os
import sys

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_batch_integration():
    """Test the complete batch translation workflow"""
    
    print("🧪 Testing batch translation integration...")
    
    # Get API key from .env.test file
    api_key = None
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env.test')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('DEEPL_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    break
    
    if not api_key:
        print("❌ DEEPL_API_KEY not found in .env.test file")
        return False
    
    try:
        from subtitle_fusion import SubtitleFusionEngine
        from srt_parser import Subtitle
        from deepl_api import DeepLAPI
        
        # Create test subtitles with exactly 1 unknown word each
        target_subs = [
            Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Hello beautiful"),
            Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="This is wonderful"),
            Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="The sunshine"),
            Subtitle(index="4", start="00:00:10,000", end="00:00:12,000", text="A amazing day"),
            Subtitle(index="5", start="00:00:13,000", end="00:00:15,000", text="Very good"),
        ]
        
        native_subs = [
            Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Bonjour beau"),
            Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="C'est merveilleux"),
            Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Le soleil"),
            Subtitle(index="4", start="00:00:10,000", end="00:00:12,000", text="Une journée incroyable"),
            Subtitle(index="5", start="00:00:13,000", end="00:00:15,000", text="Très bien"),
        ]
        
        # Known words (larger set to ensure only 1 unknown word per subtitle)
        known_words = {"hello", "this", "is", "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "very", "good"}
        
        print(f"📝 Test subtitles:")
        for sub in target_subs:
            print(f"  {sub.index}: '{sub.text}'")
        
        print(f"\n📚 Known words: {len(known_words)} words")
        print(f"🔍 Expected unknown words: beautiful, wonderful, sunshine, amazing, day")
        
        # Initialize DeepL API
        deepl_api = DeepLAPI(api_key)
        print(f"✅ DeepL API initialized")
        
        # Initialize fusion engine
        engine = SubtitleFusionEngine()
        
        print(f"\n🔄 Testing complete batch translation workflow...")
        
        # Test with real DeepL API
        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang="EN",
            enable_inline_translation=True,
            deepl_api=deepl_api,
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
        
        print(f"\n📝 Generated subtitles with inline translations:")
        for sub in result['hybrid']:
            print(f"  {sub.index}: '{sub.text}'")
        
        # Check DeepL API statistics
        stats = deepl_api.get_stats()
        print(f"\n📈 DeepL API Statistics:")
        print(f"  - Total requests: {stats['requestCount']}")
        print(f"  - Cache size: {stats['cacheSize']}")
        
        # Verify batch translation worked (should be 1 request for all words)
        if stats['requestCount'] == 1:
            print("✅ Batch translation successful - only 1 API request made!")
        else:
            print(f"❌ Expected 1 API request, got {stats['requestCount']}")
            return False
        
        # Verify inline translations were applied
        if result['inlineTranslationCount'] > 0:
            print(f"✅ {result['inlineTranslationCount']} inline translations applied")
        else:
            print("❌ No inline translations applied")
            return False
        
        print(f"\n🎉 Batch translation integration test completed successfully!")
        print(f"📋 Next step: Test with real SRT files for end-to-end validation")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_batch_integration()
    sys.exit(0 if success else 1)

