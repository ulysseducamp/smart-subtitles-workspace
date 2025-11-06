#!/usr/bin/env python3
"""
Tests complets pour la fonction normalize_words()
Teste tous les cas particuliers: apostrophes, tirets, noms composés, dialogues, etc.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from srt_parser import normalize_words


def test_apostrophes():
    """Test handling of apostrophes (contractions)"""
    print("=" * 60)
    print("TEST: Apostrophes")
    print("=" * 60)

    tests = [
        ("l'école", ["école"], "Apostrophe standard"),
        ("c'est", ["est"], "Apostrophe with 'c'"),
        ("d'accord", ["accord"], "Apostrophe with 'd'"),
        ("j'ai", ["ai"], "Single letter before apostrophe"),
        ("aujourd'hui", ["aujourd", "hui"], "Apostrophe in middle"),
        ("'école", ["école"], "Apostrophe at start"),
        ("test'", ["test"], "Apostrophe at end"),
        ("'", [], "Apostrophe alone"),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_hyphens():
    """Test handling of hyphens (compound words and grammatical constructions)"""
    print("=" * 60)
    print("TEST: Hyphens (Tirets)")
    print("=" * 60)

    tests = [
        ("Marie-Antoinette", ["marie", "antoinette"], "Compound proper name"),
        ("Jean-Pierre", ["jean", "pierre"], "Another compound name"),
        ("est-ce", ["est", "ce"], "Grammatical construction"),
        ("a-t-il", ["il"], "Grammatical with single letters (a, t filtered)"),
        ("peut-être", ["peut", "être"], "Common compound word"),
        ("Arc-en-Ciel", ["arc", "en", "ciel"], "Multiple hyphens"),
        ("c'est-à-dire", ["est", "dire"], "Apostrophe + hyphens (à filtered)"),
        ("-test", ["test"], "Hyphen at start (dialogue)"),
        ("test-", ["test"], "Hyphen at end"),
        ("-", [], "Hyphen alone"),
        ("--test", ["test"], "Multiple hyphens at start"),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_dialogue_markers():
    """Test handling of dialogue markers (common in subtitles)"""
    print("=" * 60)
    print("TEST: Dialogue Markers")
    print("=" * 60)

    tests = [
        ("- Bonjour", ["bonjour"], "Dialogue marker at start"),
        ("- Bonjour tout le monde", ["bonjour", "tout", "le", "monde"], "Dialogue with multiple words"),
        ("Regarde -", ["regarde"], "Hyphen at end"),
        ("- C'est Marie-Antoinette!", ["est", "marie", "antoinette"], "Dialogue with apostrophe and hyphen"),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_mixed_punctuation():
    """Test handling of mixed punctuation"""
    print("=" * 60)
    print("TEST: Mixed Punctuation")
    print("=" * 60)

    tests = [
        ("Hello, world!", ["hello", "world"], "Comma and exclamation"),
        ("Qu'est-ce que c'est?", ["qu", "est", "ce", "que", "est"], "Multiple apostrophes and hyphen"),
        ("(test)", ["test"], "Parentheses"),
        ("[test]", ["test"], "Brackets"),
        ("test...", ["test"], "Multiple periods"),
        ("test;test", ["test", "test"], "Semicolon"),
        ("50%", ["50"], "Percentage sign"),
        ("test@test", ["test", "test"], "At sign"),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_html_tags():
    """Test handling of HTML tags in subtitles"""
    print("=" * 60)
    print("TEST: HTML Tags")
    print("=" * 60)

    tests = [
        ("<i>test</i>", ["test"], "Italic tags"),
        ("<b>test</b>", ["test"], "Bold tags"),
        ("<i>C'est Marie-Antoinette</i>", ["est", "marie", "antoinette"], "Tags with apostrophe and hyphen"),
        ("<i>test</i> <b>word</b>", ["test", "word"], "Multiple tags"),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_single_letter_filtering():
    """Test that single letters are filtered out"""
    print("=" * 60)
    print("TEST: Single Letter Filtering")
    print("=" * 60)

    tests = [
        ("a", [], "Single letter 'a'"),
        ("à", [], "Single letter with accent"),
        ("j'ai vu ça", ["ai", "vu", "ça"], "Sentence with single letters"),
        ("Il a vu le chat", ["il", "vu", "le", "chat"], "Sentence (a filtered)"),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_real_subtitle_examples():
    """Test with real subtitle examples from Lupin"""
    print("=" * 60)
    print("TEST: Real Subtitle Examples")
    print("=" * 60)

    tests = [
        (
            "Il a appartenu à Marie-Antoinette et il vaut des millions.",
            ["il", "appartenu", "marie", "antoinette", "et", "il", "vaut", "des", "millions"],
            "Lupin subtitle #72 (the problematic one)"
        ),
        (
            "<i>Il a appartenu à Marie-Antoinette</i> <i>et il vaut des millions.</i>",
            ["il", "appartenu", "marie", "antoinette", "et", "il", "vaut", "des", "millions"],
            "Lupin subtitle #72 with HTML tags"
        ),
        (
            "Offert par Louis XVI à Marie-Antoinette,",
            ["offert", "par", "louis", "xvi", "marie", "antoinette"],
            "Lupin subtitle #176"
        ),
        (
            "<i>le collier de la Reine,</i> <i>bijou ayant appartenu à Marie-Antoinette,</i>",
            ["le", "collier", "de", "la", "reine", "bijou", "ayant", "appartenu", "marie", "antoinette"],
            "Lupin subtitle #464"
        ),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def test_unicode_and_accents():
    """Test handling of Unicode characters and accents"""
    print("=" * 60)
    print("TEST: Unicode and Accents")
    print("=" * 60)

    tests = [
        ("école", ["école"], "Accent in word"),
        ("été", ["été"], "Multiple accents"),
        ("ça", ["ça"], "C cédille"),
        ("naïve", ["naïve"], "Diaeresis"),
        ("Noël", ["noël"], "Accent in name (lowercase)"),
    ]

    for input_text, expected, description in tests:
        result = normalize_words(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}")
        print(f"   Input: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        if result != expected:
            print(f"   ⚠️  MISMATCH!")
        print()


def run_all_tests():
    """Run all test suites"""
    print("\n" + "=" * 60)
    print("RUNNING ALL NORMALIZE_WORDS TESTS")
    print("=" * 60 + "\n")

    test_apostrophes()
    test_hyphens()
    test_dialogue_markers()
    test_mixed_punctuation()
    test_html_tags()
    test_single_letter_filtering()
    test_real_subtitle_examples()
    test_unicode_and_accents()

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
