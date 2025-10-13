#!/usr/bin/env python3
"""
Manual test to verify native fallback triggers when translation fails.

This test intentionally breaks a translation to force the fallback mechanism.
"""

import sys
import os
import asyncio

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from subtitle_fusion import SubtitleFusionEngine
from srt_parser import Subtitle
from frequency_loader import initialize_frequency_loader, get_frequency_loader


async def test_fallback_mechanism():
    """Test that fallback is triggered when translation fails."""

    print("=" * 80)
    print("MANUAL FALLBACK TEST")
    print("=" * 80)
    print()

    # Initialize frequency loader
    print("🔧 Initializing frequency loader...")
    initialize_frequency_loader()
    print("✅ Frequency loader initialized\n")

    # Create simple test data (using SRT time format: HH:MM:SS,mmm)
    target_subs = [
        Subtitle(index=1, start="00:00:01,000", end="00:00:03,000", text="Olá, como você está?"),
        Subtitle(index=2, start="00:00:04,000", end="00:00:06,000", text="Eu estou bem, obrigado."),
        Subtitle(index=3, start="00:00:07,000", end="00:00:09,000", text="A delegada chegou."),  # "delegada" will be forced to fail
    ]

    native_subs = [
        Subtitle(index=1, start="00:00:01,000", end="00:00:03,000", text="Bonjour, comment allez-vous ?"),
        Subtitle(index=2, start="00:00:04,000", end="00:00:06,000", text="Je vais bien, merci."),
        Subtitle(index=3, start="00:00:07,000", end="00:00:09,000", text="La commissaire est arrivée."),
    ]

    # Get frequency loader
    frequency_loader = get_frequency_loader()
    known_words = frequency_loader.get_top_n_words('pt', 2000)

    # Create engine
    engine = SubtitleFusionEngine()

    # Create a mock translator that will intentionally skip "delegada"
    class MockTranslator:
        def __init__(self):
            self.call_count = 0

        async def translate_batch_parallel(self, words_with_contexts, source_lang, target_lang, max_concurrent=8):
            """Mock parallel translation that intentionally skips 'delegada'."""
            from typing import List, Tuple, Dict

            self.call_count += 1
            print(f"\n🔧 MockTranslator.translate_batch_parallel called (call #{self.call_count})")
            print(f"   Source: {source_lang} → Target: {target_lang}")
            print(f"   Words to translate: {len(words_with_contexts)}")

            # Create translations for all words EXCEPT 'delegada'
            translations = {}
            for word, context in words_with_contexts:
                if word == "delegada":
                    print(f"   ❌ INTENTIONALLY SKIPPING: '{word}' (to force fallback)")
                    print(f"      Context: \"{context}\"")
                else:
                    # Simple mock translation
                    translations[word] = f"[mock-{word}]"
                    print(f"   ✅ Translating: '{word}' → '{translations[word]}'")

            print(f"   📊 Returning {len(translations)}/{len(words_with_contexts)} translations")
            return translations

    mock_translator = MockTranslator()

    print("\n" + "=" * 80)
    print("RUNNING FUSION WITH MOCK TRANSLATOR")
    print("=" * 80)
    print()

    # Run fusion with mock translator
    result = await engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang='pt',
        enable_inline_translation=True,
        deepl_api=None,
        openai_translator=mock_translator,
        native_lang='fr',
        top_n=2000,
        max_concurrent=8
    )

    print("\n" + "=" * 80)
    print("FUSION RESULTS")
    print("=" * 80)
    print(f"✅ Success: {result['success']}")
    print(f"📊 Inline translations: {result['inlineTranslationCount']}")
    print(f"🔄 Fallback count: {result['fallbackCount']}")
    print(f"❌ Error count: {result['errorCount']}")
    print()

    print("Hybrid subtitles:")
    for sub in result['hybrid']:
        print(f"  [{sub.index}] {sub.text}")
    print()

    # Verify expectations
    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)

    if result['fallbackCount'] > 0:
        print(f"✅ SUCCESS: Fallback was triggered {result['fallbackCount']} time(s)")
        print("   The warning logs should appear above showing:")
        print("   - ⚠️  TRANSLATION FAILED for word 'delegada'")
        print("   - 🔄 Attempting FR fallback")
        print("   - ✅ FR fallback applied or ⚠️  No FR fallback found")
    else:
        print("❌ FAILURE: Fallback was NOT triggered")
        print("   Expected fallbackCount > 0, got 0")
        print("   This means the detection is not working correctly")

    print()
    print("Expected behavior:")
    print("  1. MockTranslator should skip 'delegada'")
    print("  2. Fusion should detect missing translation")
    print("  3. Warning log should appear: ⚠️  TRANSLATION FAILED")
    print("  4. Fallback should apply FR subtitle for subtitle #3")
    print("  5. fallbackCount should be 1")
    print()

    return result['fallbackCount'] > 0


if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_fallback_mechanism())

    print("=" * 80)
    if success:
        print("✅ TEST PASSED: Fallback mechanism works correctly")
    else:
        print("❌ TEST FAILED: Fallback mechanism did not trigger")
    print("=" * 80)

    sys.exit(0 if success else 1)
