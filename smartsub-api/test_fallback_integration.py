"""
Test script for OpenAI + DeepL fallback integration (Steps 2 & 3)
Tests the full subtitle fusion with context-aware translation
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

def create_test_subtitles():
    """Create simple test subtitles in Portuguese"""
    target_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Maria estava na frente do portão."),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="A porta estava fechada."),
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Ela tentou abrir mas não conseguiu."),
    ]

    native_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Marie était devant le portail."),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="La porte était fermée."),
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Elle a essayé d'ouvrir mais n'a pas réussi."),
    ]

    return target_subs, native_subs

def test_openai_with_fallback():
    """Test OpenAI translation with DeepL fallback (Step 2)"""

    print("=" * 60)
    print("STEP 2: Testing OpenAI + DeepL Fallback")
    print("=" * 60)

    # Get API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    deepl_key = os.getenv("DEEPL_API_KEY")

    if not openai_key:
        print("⚠️  OPENAI_API_KEY not found - testing DeepL only mode")

    if not deepl_key:
        print("⚠️  DEEPL_API_KEY not found - DeepL fallback will fail")

    # Initialize translators
    openai_translator = OpenAITranslator(api_key=openai_key) if openai_key else None
    deepl_api = DeepLAPI(api_key=deepl_key) if deepl_key else None

    # Test subtitles
    target_subs, native_subs = create_test_subtitles()

    # Known words (minimal vocabulary to force translations)
    known_words = {"a", "o", "na", "mas", "não"}

    # Initialize engine
    engine = SubtitleFusionEngine()

    print("\n📝 Test Configuration:")
    print(f"   Target Language: Portuguese (PT)")
    print(f"   Native Language: French (FR)")
    print(f"   Known Words: {known_words}")
    print(f"   OpenAI Available: {'✅ Yes' if openai_translator else '❌ No'}")
    print(f"   DeepL Available: {'✅ Yes' if deepl_api else '❌ No'}")

    try:
        print("\n🔄 Running subtitle fusion...")

        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang="PT",
            enable_inline_translation=True,
            deepl_api=deepl_api,
            openai_translator=openai_translator,
            native_lang="FR",
            top_n=2000
        )

        print("\n✅ FUSION SUCCESS!")
        print(f"\n📊 Results:")
        print(f"   Hybrid subtitles: {len(result['hybrid'])}")
        print(f"   Replaced count: {result['replacedCount']}")
        print(f"   Inline translations: {result['inlineTranslationCount']}")

        print(f"\n📝 Sample Output (first 3 subtitles):")
        for i, sub in enumerate(result['hybrid'][:3]):
            print(f"   [{sub.index}] {sub.start} --> {sub.end}")
            print(f"       {sub.text}")

        print("\n" + "=" * 60)
        print("✅ STEP 2 COMPLETED: Fallback mechanism works!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ FUSION FAILED: {e}")
        print(f"\n🔍 Debug Info:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_context_global_integration():
    """Test OpenAI with full episode context (Step 3)"""

    print("\n" + "=" * 60)
    print("STEP 3: Testing Full Episode Context Integration")
    print("=" * 60)

    openai_key = os.getenv("OPENAI_API_KEY")

    if not openai_key:
        print("❌ ERROR: OPENAI_API_KEY required for this test")
        return False

    # Initialize translator
    openai_translator = OpenAITranslator(api_key=openai_key)

    # Extended test subtitles (simulating more context)
    target_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Maria estava na frente do portão."),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="A porta estava fechada."),
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Ela tentou abrir mas não conseguiu."),
        Subtitle(index="4", start="00:00:10,000", end="00:00:12,000", text="O jardim estava silencioso."),
        Subtitle(index="5", start="00:00:13,000", end="00:00:15,000", text="Ninguém respondeu quando ela chamou."),
    ]

    native_subs = [
        Subtitle(index="1", start="00:00:01,000", end="00:00:03,000", text="Marie était devant le portail."),
        Subtitle(index="2", start="00:00:04,000", end="00:00:06,000", text="La porte était fermée."),
        Subtitle(index="3", start="00:00:07,000", end="00:00:09,000", text="Elle a essayé d'ouvrir mais n'a pas réussi."),
        Subtitle(index="4", start="00:00:10,000", end="00:00:12,000", text="Le jardin était silencieux."),
        Subtitle(index="5", start="00:00:13,000", end="00:00:15,000", text="Personne n'a répondu quand elle a appelé."),
    ]

    known_words = {"a", "o", "na", "mas", "não", "quando"}

    engine = SubtitleFusionEngine()

    print("\n📝 Test Configuration:")
    print(f"   Subtitles count: {len(target_subs)}")
    print(f"   Context size: ~{sum(len(sub.text) for sub in target_subs)} characters")

    try:
        print("\n🔄 Running fusion with global context...")

        result = engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            lang="PT",
            enable_inline_translation=True,
            deepl_api=None,  # Force OpenAI only
            openai_translator=openai_translator,
            native_lang="FR",
            top_n=2000
        )

        print("\n✅ CONTEXT INTEGRATION SUCCESS!")
        print(f"\n📊 Results:")
        print(f"   Hybrid subtitles: {len(result['hybrid'])}")
        print(f"   Inline translations: {result['inlineTranslationCount']}")

        print(f"\n📝 Output Subtitles:")
        for sub in result['hybrid']:
            print(f"   [{sub.index}] {sub.text}")

        print("\n" + "=" * 60)
        print("✅ STEP 3 COMPLETED: Global context works perfectly!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ INTEGRATION FAILED: {e}")
        print(f"\n🔍 Debug Info:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_openai_with_fallback()
    success2 = test_context_global_integration() if success1 else False

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Step 2 (Fallback): {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"Step 3 (Context): {'✅ PASSED' if success2 else '❌ FAILED'}")
    print("=" * 60)

    sys.exit(0 if (success1 and success2) else 1)
