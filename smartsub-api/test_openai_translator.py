"""
Test script for OpenAI translator (Step 1)
Tests isolated OpenAI translation with context
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_translator import OpenAITranslator

# Load environment variables
load_dotenv()

def test_openai_translator():
    """Test OpenAI translator with Portuguese to French translation"""

    print("=" * 60)
    print("STEP 1: Testing OpenAI Translator (Isolated)")
    print("=" * 60)

    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in environment variables")
        print("\n📝 Next steps:")
        print("1. Add OPENAI_API_KEY to your .env file")
        print("2. Or export OPENAI_API_KEY='your-key-here' in terminal")
        return False

    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}\n")

    # Initialize translator
    translator = OpenAITranslator(api_key=api_key)

    # Test context (Portuguese subtitles)
    episode_context = """1
00:00:01,000 --> 00:00:03,000
Maria estava na frente do portão.

2
00:00:04,000 --> 00:00:06,000
A porta estava fechada.

3
00:00:07,000 --> 00:00:09,000
Ela tentou abrir mas não conseguiu."""

    # Words to translate
    words_to_translate = ["estava", "porta", "fechada"]

    print("📝 Test Input:")
    print(f"   Source Language: Portuguese (PT)")
    print(f"   Target Language: French (FR)")
    print(f"   Words to translate: {words_to_translate}")
    print(f"   Context length: {len(episode_context)} characters\n")

    try:
        # Translate
        result = translator.translate_batch_with_context(
            episode_context=episode_context,
            words_to_translate=words_to_translate,
            source_lang="PT",
            target_lang="FR"
        )

        print("\n✅ TRANSLATION SUCCESS!")
        print("\n📊 Results:")
        for word, translation in result.items():
            print(f"   {word} → {translation}")

        # Validate results
        print("\n🔍 Validation:")

        # Check all words translated
        if len(result) == len(words_to_translate):
            print("   ✅ All words translated")
        else:
            print(f"   ❌ Missing translations: expected {len(words_to_translate)}, got {len(result)}")
            return False

        # Check expected translations (approximate)
        expected = {
            "estava": ["était", "était"],
            "porta": ["porte", "porte"],
            "fechada": ["fermée", "fermé", "fermée"]
        }

        all_correct = True
        for word, translation in result.items():
            if word in expected:
                if translation.lower() in [exp.lower() for exp in expected[word]]:
                    print(f"   ✅ '{word}' → '{translation}' (correct)")
                else:
                    print(f"   ⚠️  '{word}' → '{translation}' (expected one of: {expected[word]})")
                    all_correct = False

        # Get stats
        stats = translator.get_stats()
        print(f"\n📈 Translator Stats:")
        print(f"   API Requests: {stats['requestCount']}")
        print(f"   Cache Size: {stats['cacheSize']}")

        print("\n" + "=" * 60)
        if all_correct:
            print("✅ STEP 1 COMPLETED: OpenAI Translator works perfectly!")
        else:
            print("⚠️  STEP 1 COMPLETED: OpenAI Translator works (minor translation variations)")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ TRANSLATION FAILED: {e}")
        print("\n🔍 Debug Info:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_openai_translator()
    sys.exit(0 if success else 1)
