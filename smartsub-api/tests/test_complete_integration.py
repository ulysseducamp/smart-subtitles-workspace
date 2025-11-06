#!/usr/bin/env python3
"""
Test Complet End-to-End
Teste tous les cas particuliers du refactor:
1. Marie-Antoinette et il (cas original)
2. Noms propres (début vs milieu)
3. Mots rares vs noms propres
4. Majuscules/minuscules
5. Ponctuation
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from subtitle_fusion import SubtitleFusionEngine, apply_translation
from srt_parser import Subtitle, normalize_words
from frequency_loader import FrequencyLoader
import asyncio


def test_apply_translation_cases():
    """Test tous les cas de apply_translation()"""
    print("=" * 70)
    print("TEST 1: apply_translation() - Tous les cas")
    print("=" * 70)

    tests = [
        # Test 1: Le cas original Lupin
        (
            "Il a appartenu à Marie-Antoinette et il vaut des millions.",
            "et",
            "and",
            "Il a appartenu à Marie-Antoinette et (and) il vaut des millions.",
            "✅ 'et' traduit mais PAS dans 'Antoinette'"
        ),
        # Test 2: Majuscules/minuscules
        (
            "Il Mange du pain.",
            "mange",
            "eats",
            "Il Mange (eats) du pain.",
            "✅ 'Mange' (majuscule) matché"
        ),
        # Test 3: Ponctuation
        (
            "Il mange, vraiment!",
            "mange",
            "eats",
            "Il mange (eats), vraiment!",
            "✅ Ponctuation préservée"
        ),
        # Test 4: Occurrences multiples
        (
            "Il mange et elle mange.",
            "mange",
            "eats",
            "Il mange (eats) et elle mange (eats).",
            "✅ Toutes les occurrences"
        ),
    ]

    all_passed = True
    for input_text, word, translation, expected, description in tests:
        result = apply_translation(input_text, word, translation)
        passed = result == expected

        if passed:
            print(f"✅ {description}")
        else:
            print(f"❌ {description}")
            print(f"   Input: '{input_text}'")
            print(f"   Expected: '{expected}'")
            print(f"   Got: '{result}'")
            all_passed = False

    print()
    return all_passed


def test_normalize_words_cases():
    """Test tous les cas de normalize_words()"""
    print("=" * 70)
    print("TEST 2: normalize_words() - Tous les cas")
    print("=" * 70)

    tests = [
        (
            "Il a appartenu à Marie-Antoinette et il",
            ["il", "appartenu", "marie", "antoinette", "et", "il"],
            "✅ Marie-Antoinette split correctement"
        ),
        (
            "l'école",
            ["école"],
            "✅ Apostrophe enlevée"
        ),
        (
            "c'est",
            ["est"],
            "✅ c' filtré (1 lettre)"
        ),
    ]

    all_passed = True
    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        passed = result == expected

        if passed:
            print(f"{description}")
        else:
            print(f"❌ {description}")
            print(f"   Input: '{input_text}'")
            print(f"   Expected: {expected}")
            print(f"   Got: {result}")
            all_passed = False

    print()
    return all_passed


async def test_full_integration():
    """Test intégration complète avec _analyze_subtitle_words()"""
    print("=" * 70)
    print("TEST 3: Intégration complète _analyze_subtitle_words()")
    print("=" * 70)

    engine = SubtitleFusionEngine()
    freq_loader = FrequencyLoader()

    # Simuler un niveau de 1000 mots
    known_words = freq_loader.get_top_n_words('fr', 1000)
    full_frequency_list = freq_loader.get_full_list('fr')

    print(f"📊 Frequency lists chargées: {len(known_words)} known, {len(full_frequency_list)} full")

    tests = [
        {
            "text": "Il habite à Netflix",
            "expected_proper_nouns": ["netflix"],
            "expected_unknown": ["habite"],  # "habite" pas dans top 1000
            "description": "✅ Netflix (milieu) = nom propre confirmé, 'habite' inconnu"
        },
        {
            "text": "Il a appartenu à Marie-Antoinette et il",
            "expected_proper_nouns": ["marie", "antoinette"],
            "expected_unknown": [],  # "appartenir" (lemme) est dans top 1000
            "description": "✅ Marie-Antoinette (milieu) = noms propres, 'appartenir' connu"
        },
    ]

    all_passed = True
    for test in tests:
        analysis = engine._analyze_subtitle_words(
            test["text"],
            'fr',
            known_words,
            full_frequency_list
        )

        # Vérifier noms propres
        proper_match = set(analysis['proper_nouns']) == set(test['expected_proper_nouns'])
        # Vérifier mots inconnus
        unknown_match = set(analysis['unknown_words']) == set(test['expected_unknown'])

        if proper_match and unknown_match:
            print(f"{test['description']}")
        else:
            print(f"❌ {test['description']}")
            print(f"   Text: '{test['text']}'")
            if not proper_match:
                print(f"   Expected proper nouns: {test['expected_proper_nouns']}")
                print(f"   Got: {analysis['proper_nouns']}")
            if not unknown_match:
                print(f"   Expected unknown: {test['expected_unknown']}")
                print(f"   Got: {analysis['unknown_words']}")
            all_passed = False

    print()
    return all_passed


async def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "=" * 70)
    print("🧪 TESTS COMPLETS FINAUX - TOUS LES CAS PARTICULIERS")
    print("=" * 70 + "\n")

    test1 = test_apply_translation_cases()
    test2 = test_normalize_words_cases()
    test3 = await test_full_integration()

    print("=" * 70)
    if test1 and test2 and test3:
        print("🎉 TOUS LES TESTS PASSENT!")
        print("=" * 70)
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
