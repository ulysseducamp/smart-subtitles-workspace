#!/usr/bin/env python3
"""
Tests unitaires pour la fonction apply_translation()
Teste regex + word boundaries + case insensitive
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from subtitle_fusion import apply_translation


def test_basic_translation():
    """Test de base: traduction simple"""
    print("=" * 60)
    print("TEST: Traduction de base")
    print("=" * 60)

    text = "Il mange du pain."
    result = apply_translation(text, "mange", "eats")
    expected = "Il mange (eats) du pain."

    status = "✅" if result == expected else "❌"
    print(f"{status} Traduction simple")
    print(f"   Input: '{text}'")
    print(f"   Expected: '{expected}'")
    print(f"   Got: '{result}'")
    if result != expected:
        print(f"   ⚠️  MISMATCH!")
    print()


def test_case_insensitive():
    """Test case insensitive: majuscules/minuscules"""
    print("=" * 60)
    print("TEST: Case Insensitive")
    print("=" * 60)

    tests = [
        ("Mange ton repas!", "mange", "eat", "Mange (eat) ton repas!"),
        ("MANGE ton repas!", "mange", "eat", "MANGE (eat) ton repas!"),
        ("Il MANGE du pain.", "mange", "eat", "Il MANGE (eat) du pain."),
    ]

    for input_text, word, translation, expected in tests:
        result = apply_translation(input_text, word, translation)
        status = "✅" if result == expected else "❌"
        print(f"{status} Case insensitive: '{word}' → '{translation}'")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got: '{result}'")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_punctuation():
    """Test avec ponctuation autour des mots"""
    print("=" * 60)
    print("TEST: Ponctuation")
    print("=" * 60)

    tests = [
        ("mange, mange!", "mange", "eat", "mange (eat), mange (eat)!"),
        ("Il mange.", "mange", "eats", "Il mange (eats)."),
        ("(mange)", "mange", "eat", "(mange (eat))"),
        ("mange...", "mange", "eat", "mange (eat)..."),
        ("'mange'", "mange", "eat", "'mange (eat)'"),
    ]

    for input_text, word, translation, expected in tests:
        result = apply_translation(input_text, word, translation)
        status = "✅" if result == expected else "❌"
        print(f"{status} Ponctuation: '{input_text}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got: '{result}'")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_word_boundaries():
    """Test word boundaries: ne pas remplacer dans un autre mot"""
    print("=" * 60)
    print("TEST: Word Boundaries")
    print("=" * 60)

    tests = [
        # "et" ne doit PAS être remplacé dans "Antoinette"
        ("Marie-Antoinette et il", "et", "and", "Marie-Antoinette et (and) il"),
        # "mange" ne doit PAS être remplacé dans "mangeons"
        ("Nous mangeons", "mange", "eat", "Nous mangeons"),
        # "il" ne doit PAS être remplacé dans "famille"
        ("Une famille", "il", "he", "Une famille"),
    ]

    for input_text, word, translation, expected in tests:
        result = apply_translation(input_text, word, translation)
        status = "✅" if result == expected else "❌"
        print(f"{status} Word boundaries: '{word}' in '{input_text}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got: '{result}'")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_multiple_occurrences():
    """Test remplacement de toutes les occurrences"""
    print("=" * 60)
    print("TEST: Occurrences Multiples")
    print("=" * 60)

    tests = [
        ("Il mange et elle mange.", "mange", "eats", "Il mange (eats) et elle mange (eats)."),
        ("Mange, mange, mange!", "mange", "eat", "Mange (eat), mange (eat), mange (eat)!"),
    ]

    for input_text, word, translation, expected in tests:
        result = apply_translation(input_text, word, translation)
        status = "✅" if result == expected else "❌"
        print(f"{status} Multiple occurrences: '{word}'")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got: '{result}'")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_special_characters():
    """Test avec caractères spéciaux dans les mots"""
    print("=" * 60)
    print("TEST: Caractères Spéciaux")
    print("=" * 60)

    tests = [
        ("Il a un café.", "café", "coffee", "Il a un café (coffee)."),
        ("C'est ça.", "ça", "that", "C'est ça (that)."),
        ("Où est-il?", "où", "where", "Où (where) est-il?"),
    ]

    for input_text, word, translation, expected in tests:
        result = apply_translation(input_text, word, translation)
        status = "✅" if result == expected else "❌"
        print(f"{status} Caractères spéciaux: '{word}'")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got: '{result}'")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_lupin_real_case():
    """Test avec le cas réel Lupin: Marie-Antoinette et il"""
    print("=" * 60)
    print("TEST: Cas Réel Lupin")
    print("=" * 60)

    text = "Il a appartenu à Marie-Antoinette et il vaut des millions."

    # "et" doit être traduit mais PAS dans "Antoinette"
    result = apply_translation(text, "et", "and")
    expected = "Il a appartenu à Marie-Antoinette et (and) il vaut des millions."

    status = "✅" if result == expected else "❌"
    print(f"{status} Lupin: 'et' ne doit pas être dans 'Antoinette'")
    print(f"   Input: '{text}'")
    print(f"   Expected: '{expected}'")
    print(f"   Got: '{result}'")
    if result != expected:
        print(f"   ⚠️  MISMATCH!")
    print()


def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "=" * 60)
    print("RUNNING ALL APPLY_TRANSLATION TESTS")
    print("=" * 60 + "\n")

    test_basic_translation()
    test_case_insensitive()
    test_punctuation()
    test_word_boundaries()
    test_multiple_occurrences()
    test_special_characters()
    test_lupin_real_case()

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
