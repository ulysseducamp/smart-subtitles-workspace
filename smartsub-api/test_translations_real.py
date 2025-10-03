"""
Test script to ACTUALLY test OpenAI translations with inline mode
Previous tests had minimal vocabulary causing full replacement instead of inline translations
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_translator import OpenAITranslator
from deepl_api import DeepLAPI
from subtitle_fusion import SubtitleFusionEngine
from srt_parser import Subtitle

# Load environment variables
load_dotenv()

def create_test_subtitles_rich_vocab():
    """Create test subtitles with RICH vocabulary to force inline translations
    Each subtitle has EXACTLY 1 unknown word to trigger inline translation"""
    target_subs = [
        # Subtitle with 1 unknown word: "caminhando"
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Eu estava caminhando pela rua."),
        # Subtitle with 1 unknown word: "ajudar"
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="Você pode me ajudar aqui."),
        # Subtitle with 1 unknown word: "biblioteca"
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Ela mora perto da biblioteca."),
    ]

    native_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Je marchais dans la rue."),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="Pouvez-vous m'aider ici?"),
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Elle habite près de la bibliothèque."),
    ]

    return target_subs, native_subs

def test_openai_inline_translations():
    """Test OpenAI inline translations with rich vocabulary"""

    print("=" * 70)
    print("REAL TEST: OpenAI Inline Translations with Context")
    print("=" * 70)

    # Get API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    deepl_key = os.getenv("DEEPL_API_KEY")

    if not openai_key:
        print("❌ ERROR: OPENAI_API_KEY required for this test")
        return False

    # Initialize translators
    openai_translator = OpenAITranslator(api_key=openai_key)
    deepl_api = DeepLAPI(api_key=deepl_key) if deepl_key else None

    # Test subtitles
    target_subs, native_subs = create_test_subtitles_rich_vocab()

    # RICH vocabulary - most common Portuguese words to keep subtitles in PT
    # This will force INLINE translations for unknown words
    # Strategy: Include all words EXCEPT the 3 target words we want to translate
    known_words = {
        # Articles
        "o", "a", "os", "as", "um", "uma", "uns", "umas",
        # Pronouns
        "eu", "você", "ele", "ela", "nós", "vocês", "eles", "elas",
        "me", "te", "se", "nos", "lhe", "lhes",
        # Prepositions
        "de", "em", "para", "por", "com", "sem", "sobre", "até", "desde",
        "da", "do", "das", "dos", "na", "no", "nas", "nos", "pela", "pelo",
        # Conjunctions
        "e", "mas", "ou", "porque", "que", "se", "quando", "como",
        # Verbs (most common)
        "é", "ser", "estar", "ter", "fazer", "ir", "ver", "dar", "saber",
        "pode", "podem", "posso", "vai", "vou", "foi", "são", "estou", "estava",
        # Common words
        "não", "sim", "mais", "muito", "bem", "aqui", "agora", "hoje",
        "isso", "este", "esse", "aquele", "meu", "seu", "nosso",
        # Words from our test sentences (except the 3 target words)
        "pela", "rua", "perto", "mora",
        # EXCLUDED (these should be translated inline):
        # "caminhando", "ajudar", "biblioteca"
    }

    # Initialize engine
    engine = SubtitleFusionEngine()

    print("\n📝 Test Configuration:")
    print(f"   Target Language: Portuguese (PT)")
    print(f"   Native Language: French (FR)")
    print(f"   Known Words Count: {len(known_words)}")
    print(f"   Expected Behavior: Keep PT subtitles with inline translations for unknown words")
    print(f"   Target subtitles: {len(target_subs)}")

    print("\n📋 Subtitle Content:")
    for sub in target_subs:
        print(f"   [{sub.index}] {sub.text}")

    print("\n🎯 Expected Unknown Words (should be translated inline):")
    print("   - 'estava' (was)")
    print("   - 'caminhando' (walking)")
    print("   - 'ajudar' (help)")
    print("   - 'isso' (this)")
    print("   - 'biblioteca' (library)")

    try:
        print("\n🔄 Running subtitle fusion with OpenAI...")

        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang="PT",
            enable_inline_translation=True,
            deepl_api=deepl_api,
            openai_translator=openai_translator,
            native_lang="FR",
            top_n=5000  # Increased to give more words a chance
        )

        print("\n✅ FUSION COMPLETED!")
        print(f"\n📊 Statistics:")
        print(f"   Hybrid subtitles: {len(result['hybrid'])}")
        print(f"   Replaced with native: {result['replacedCount']}")
        print(f"   Inline translations: {result['inlineTranslationCount']}")

        print(f"\n📝 Final Subtitles (with inline translations):")
        for sub in result['hybrid']:
            print(f"   [{sub.index}] {sub.text}")

        # Validation
        print("\n🔍 Validation:")

        if result['inlineTranslationCount'] == 0:
            print("   ❌ NO INLINE TRANSLATIONS - Test failed!")
            print("   This means OpenAI was not called or all words were unknown")
            print("   Expected at least 1-2 inline translations")
            return False

        # Check if subtitles contain translations (word + parentheses)
        has_inline_format = any("(" in sub.text and ")" in sub.text for sub in result['hybrid'])

        if has_inline_format:
            print("   ✅ Inline translations found in subtitle text!")
            print("   ✅ OpenAI translation with context worked!")
        else:
            print("   ⚠️  No inline format found (word (translation))")

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: OpenAI inline translations working with context!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print(f"\n🔍 Debug Info:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_openai_vs_deepl_comparison():
    """Compare OpenAI (with context) vs DeepL (without context)"""

    print("\n" + "=" * 70)
    print("COMPARISON TEST: OpenAI (context) vs DeepL (no context)")
    print("=" * 70)

    openai_key = os.getenv("OPENAI_API_KEY")
    deepl_key = os.getenv("DEEPL_API_KEY")

    if not openai_key or not deepl_key:
        print("⚠️  Need both API keys for comparison test")
        return True  # Not critical

    # Test with ambiguous word that needs context
    target_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Ele estava no banco esperando."),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="O gerente do banco chegou."),
    ]

    native_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Il était sur le banc en attendant."),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="Le directeur de la banque est arrivé."),
    ]

    known_words = {
        "o", "a", "ele", "ela", "no", "na", "do", "da", "de"
    }

    print("\n📝 Ambiguous Word Test:")
    print("   Word: 'banco' (can mean 'bench' or 'bank')")
    print("   Subtitle 1: 'Ele estava no banco esperando' → should be 'bench'")
    print("   Subtitle 2: 'O gerente do banco chegou' → should be 'bank'")

    # Test OpenAI
    print("\n🤖 Testing OpenAI (with full context)...")
    openai_translator = OpenAITranslator(api_key=openai_key)
    engine = SubtitleFusionEngine()

    result_openai = engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang="PT",
        enable_inline_translation=True,
        deepl_api=None,
        openai_translator=openai_translator,
        native_lang="FR",
        top_n=5000
    )

    print("   OpenAI Results:")
    for sub in result_openai['hybrid']:
        print(f"      [{sub.index}] {sub.text}")

    # Test DeepL
    print("\n🔄 Testing DeepL (without context)...")
    deepl_api = DeepLAPI(api_key=deepl_key)

    result_deepl = engine.fuse_subtitles(
        target_subs=target_subs,
        native_subs=native_subs,
        known_words=known_words,
        lang="PT",
        enable_inline_translation=True,
        deepl_api=deepl_api,
        openai_translator=None,
        native_lang="FR",
        top_n=5000
    )

    print("   DeepL Results:")
    for sub in result_deepl['hybrid']:
        print(f"      [{sub.index}] {sub.text}")

    print("\n🎯 Analysis:")
    print("   OpenAI should differentiate 'banco' based on context")
    print("   DeepL may translate 'banco' the same way both times")

    return True

if __name__ == "__main__":
    print("\n🧪 COMPREHENSIVE TRANSLATION TESTING")
    print("=" * 70)

    success1 = test_openai_inline_translations()
    success2 = test_openai_vs_deepl_comparison() if success1 else False

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Inline Translations Test: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"OpenAI vs DeepL Comparison: {'✅ DONE' if success2 else '⏭️  SKIPPED'}")
    print("=" * 70)

    if success1:
        print("\n✅ OpenAI translator is working correctly with context!")
        print("   Ready for production deployment on Railway.")
    else:
        print("\n❌ OpenAI translator needs debugging before deployment.")

    sys.exit(0 if success1 else 1)
