"""
Test unitaire pour les fonctions de nettoyage de ponctuation
"""

import sys
sys.path.insert(0, 'src')

from subtitle_fusion import clean_word_for_translation, extract_trailing_punctuation

def test_clean_word_for_translation():
    """Test de la fonction clean_word_for_translation"""
    print("=== Test clean_word_for_translation ===\n")

    test_cases = [
        # (input, expected_output, description)
        ("tensão]", "tensão", "Crochet à la fin"),
        ("[ofegando]", "ofegando", "Crochets au début et à la fin"),
        ("motor.", "motor", "Point à la fin"),
        ("pré-lavagem", "pré-lavagem", "Trait d'union interne préservé"),
        ("d'água", "d'água", "Apostrophe interne préservée"),
        ("...esperando", "esperando", "Ellipse au début"),
        ("uísque?!", "uísque", "Multiples ponctuations à la fin"),
        ("banco", "banco", "Pas de ponctuation"),
        ("delegada,", "delegada", "Virgule à la fin"),
        ("—Olá!", "Olá", "Tiret dialogue et exclamation"),
    ]

    passed = 0
    failed = 0

    for input_word, expected, description in test_cases:
        result = clean_word_for_translation(input_word)
        status = "✅" if result == expected else "❌"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {description}")
        print(f"   Input:    '{input_word}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got:      '{result}'")
        print()

    print(f"Résultats: {passed} réussis, {failed} échoués\n")
    return failed == 0

def test_extract_trailing_punctuation():
    """Test de la fonction extract_trailing_punctuation"""
    print("=== Test extract_trailing_punctuation ===\n")

    test_cases = [
        # (input, expected_output, description)
        ("motor.", ".", "Point à la fin"),
        ("tensão]", "]", "Crochet à la fin"),
        ("banco", "", "Pas de ponctuation"),
        ("uísque?!", "?!", "Multiples ponctuations à la fin"),
        ("delegada,", ",", "Virgule à la fin"),
        ("[ofegando]", "]", "Crochet à la fin (début ignoré)"),
        ("pré-lavagem", "", "Trait d'union interne (pas trailing)"),
    ]

    passed = 0
    failed = 0

    for input_word, expected, description in test_cases:
        result = extract_trailing_punctuation(input_word)
        status = "✅" if result == expected else "❌"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {description}")
        print(f"   Input:    '{input_word}'")
        print(f"   Expected: '{expected}'")
        print(f"   Got:      '{result}'")
        print()

    print(f"Résultats: {passed} réussis, {failed} échoués\n")
    return failed == 0

def test_combined_workflow():
    """Test du workflow complet : clean + extract + rebuild"""
    print("=== Test Workflow Complet ===\n")

    test_cases = [
        # (original_word, translation, expected_result, description)
        ("tensão]", "tension", "tensão (tension)]", "Crochet à la fin"),
        ("motor.", "moteur", "motor (moteur).", "Point à la fin"),
        ("[ofegando]", "haletant", "ofegando (haletant)]", "Crochets début et fin"),
        ("banco", "banque", "banco (banque)", "Pas de ponctuation"),
    ]

    passed = 0
    failed = 0

    for original_word, translation, expected, description in test_cases:
        # Simulate the workflow
        clean_word = clean_word_for_translation(original_word)
        trailing_punct = extract_trailing_punctuation(original_word)
        result = f"{clean_word} ({translation}){trailing_punct}"

        status = "✅" if result == expected else "❌"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} {description}")
        print(f"   Original:  '{original_word}'")
        print(f"   Translation: '{translation}'")
        print(f"   Expected:  '{expected}'")
        print(f"   Got:       '{result}'")
        print()

    print(f"Résultats: {passed} réussis, {failed} échoués\n")
    return failed == 0

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TEST UNITAIRE - Nettoyage de Ponctuation")
    print("="*60 + "\n")

    test1_ok = test_clean_word_for_translation()
    test2_ok = test_extract_trailing_punctuation()
    test3_ok = test_combined_workflow()

    print("="*60)
    if test1_ok and test2_ok and test3_ok:
        print("✅ TOUS LES TESTS PASSENT !")
        sys.exit(0)
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        sys.exit(1)
