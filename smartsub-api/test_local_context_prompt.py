"""
Test unitaire pour valider le nouveau format de prompt avec contexte local
Sans appel API réel - juste pour vérifier le format et estimer les tokens
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openai_translator import OpenAITranslator

def estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ≈ 0.75 words in English/Romance languages)"""
    words = text.split()
    return int(len(words) * 1.3)

def test_local_context_prompt():
    """Test prompt generation with local context"""

    print("=" * 70)
    print("TEST UNITAIRE: Nouveau format de prompt avec contexte local")
    print("=" * 70)

    # Initialize translator (fake API key since we won't call the API)
    translator = OpenAITranslator(api_key="fake_key_for_testing")

    # Simulate word contexts (192 words from real episode test)
    # Using realistic examples from Portuguese to French
    word_contexts = {
        "caminhando": "Eu estava caminhando pela rua.",
        "ajudar": "Você pode me ajudar aqui.",
        "biblioteca": "Ela mora perto da biblioteca.",
        "portão": "Maria estava na frente do portão.",
        "fechada": "A porta estava fechada.",
        "tentou": "Ela tentou abrir mas não conseguiu.",
        "jardim": "O jardim estava silencioso.",
        "respondeu": "Ninguém respondeu quando ela chamou.",
        # Add more examples to simulate realistic batch size
        "esperando": "Ele estava no banco esperando.",
        "gerente": "O gerente do banco chegou.",
    }

    words_to_translate = list(word_contexts.keys())

    print(f"\n📊 Test Configuration:")
    print(f"   Words to translate: {len(words_to_translate)}")
    print(f"   Source language: Portuguese (PT)")
    print(f"   Target language: French (FR)")
    print(f"   Using LOCAL context (one subtitle per word)")

    # Build the prompt
    prompt = translator._build_translation_prompt(
        word_contexts=word_contexts,
        words_to_translate=words_to_translate,
        source_lang="PT",
        target_lang="FR"
    )

    # Analyze prompt
    prompt_length = len(prompt)
    estimated_tokens = estimate_tokens(prompt)

    print(f"\n📝 Generated Prompt:")
    print("=" * 70)
    print(prompt)
    print("=" * 70)

    print(f"\n📊 Prompt Statistics:")
    print(f"   Character count: {prompt_length:,}")
    print(f"   Word count: {len(prompt.split()):,}")
    print(f"   Estimated tokens: ~{estimated_tokens:,}")

    # Comparison with old approach (estimated)
    print(f"\n📉 Comparison with Full Episode Context:")
    print(f"   OLD approach (640 subtitles): ~19,587 tokens")
    print(f"   NEW approach (local context): ~{estimated_tokens:,} tokens")

    if estimated_tokens < 19587:
        reduction_percent = ((19587 - estimated_tokens) / 19587) * 100
        print(f"   ✅ Token reduction: {reduction_percent:.1f}%")
        print(f"   ✅ Expected speedup: {19587 / estimated_tokens:.1f}x faster API calls")

    # Validate prompt format
    print(f"\n🔍 Format Validation:")
    checks = [
        ("Contains word contexts", "appears in:" in prompt),
        ("Contains translation rules", "TRANSLATION RULES:" in prompt),
        ("Mentions source/target languages", "Portuguese" in prompt and "French" in prompt),
        ("Has concise format", estimated_tokens < 5000),
    ]

    all_passed = True
    for check_name, check_result in checks:
        status = "✅" if check_result else "❌"
        print(f"   {status} {check_name}")
        if not check_result:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ TEST PASSED: Prompt format is correct and optimized!")
        print("   Ready to test with real OpenAI API call.")
    else:
        print("❌ TEST FAILED: Prompt format needs adjustment.")
    print("=" * 70)

    return all_passed

if __name__ == "__main__":
    success = test_local_context_prompt()
    sys.exit(0 if success else 1)
