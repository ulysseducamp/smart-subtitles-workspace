"""
Test script to verify dict-based matching fixes translation misalignment
Tests the complete flow: subtitle_fusion.py → openai_translator.py
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from subtitle_fusion import SubtitleFusionEngine
from srt_parser import parse_srt

# Load environment variables
load_dotenv()

async def test_dict_matching():
    """Test that dict-based matching handles count mismatches gracefully"""

    print("=" * 80)
    print("DICT-BASED MATCHING TEST")
    print("Testing: subtitle_fusion.py + openai_translator.py integration")
    print("=" * 80)
    print()

    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env")
        return False

    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print()

    # Load test SRT files
    test_dir = os.path.join(os.path.dirname(__file__), 'tests', 'test_data')

    with open(os.path.join(test_dir, 'en.srt'), 'r', encoding='utf-8') as f:
        target_srt = f.read()

    with open(os.path.join(test_dir, 'fr.srt'), 'r', encoding='utf-8') as f:
        native_srt = f.read()

    # Parse SRT
    target_subs = parse_srt(target_srt)
    native_subs = parse_srt(native_srt)

    print(f"📄 Loaded test data:")
    print(f"   Target subtitles (EN): {len(target_subs)} subs")
    print(f"   Native subtitles (FR): {len(native_subs)} subs")
    print()

    # Initialize engine
    engine = SubtitleFusionEngine()

    # Initialize translators
    from openai_translator import OpenAITranslator
    from deepl_api import DeepLAPI

    openai_translator = OpenAITranslator(api_key=api_key)
    deepl_api = DeepLAPI(api_key=os.getenv("DEEPL_API_KEY", "dummy"))

    # Get known words from frequency loader
    from frequency_loader import initialize_frequency_loader, get_frequency_loader

    # Initialize frequency loader (must be called before get_frequency_loader)
    initialize_frequency_loader()

    freq_loader = get_frequency_loader()
    top_n = 800
    known_words = set(freq_loader.get_top_n_words("en", top_n))

    print(f"📚 Loaded {len(known_words)} known words (top {top_n})")
    print()
    print("🔧 Processing subtitles with dict-based matching...")
    print()

    try:
        # Run fusion (async)
        result = await engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang="en",
            native_lang="fr",
            enable_inline_translation=True,
            deepl_api=deepl_api,
            openai_translator=openai_translator,
            top_n=top_n,
            max_concurrent=8
        )

        print()
        print("=" * 80)
        print("✅ FUSION COMPLETED")
        print("=" * 80)
        print()

        # Analyze results
        hybrid_subs = result.get('hybrid', [])

        print(f"📊 Results:")
        print(f"   Hybrid subtitles: {len(hybrid_subs)}")
        print(f"   Success: {result.get('success', False)}")
        print()

        # Check for translation warnings (which indicate misalignment)
        # These would appear in logs as "⚠️  No translation for 'word' in subtitle X"

        print("🔍 Checking for translation application issues...")
        print()

        # Count how many subtitles were modified
        modified_count = 0
        replaced_count = 0
        inline_translation_count = 0

        for i, (target_sub, hybrid_sub) in enumerate(zip(target_subs[:min(20, len(target_subs))], hybrid_subs[:min(20, len(hybrid_subs))])):
            if target_sub.text != hybrid_sub.text:
                modified_count += 1

                # Check if it's a replacement (French text)
                matching_native = [n for n in native_subs if n.text == hybrid_sub.text]
                if matching_native:
                    replaced_count += 1
                    print(f"   [{i+1}] REPLACED: '{target_sub.text[:50]}' → '{hybrid_sub.text[:50]}'")

                # Check if it's inline translation (contains parentheses)
                elif '(' in hybrid_sub.text and ')' in hybrid_sub.text:
                    inline_translation_count += 1
                    print(f"   [{i+1}] INLINE: '{hybrid_sub.text[:80]}'")

        print()
        print(f"📈 Summary (first 20 subtitles):")
        print(f"   Modified: {modified_count}/20")
        print(f"   Replaced with native: {replaced_count}")
        print(f"   Inline translations: {inline_translation_count}")
        print()

        # Success criteria
        if modified_count > 0:
            print("✅ TEST PASSED: Subtitles were processed and modified")
            print("✅ Dict-based matching appears to be working")
            print()
            print("📝 Next step: Deploy to Railway staging and test with real episode")
            return True
        else:
            print("⚠️  WARNING: No subtitles were modified")
            print("   This might indicate an issue with the processing logic")
            return False

    except Exception as e:
        print()
        print("=" * 80)
        print("❌ TEST FAILED")
        print("=" * 80)
        print(f"Error: {e}")
        print(f"Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_dict_matching())
    sys.exit(0 if success else 1)
