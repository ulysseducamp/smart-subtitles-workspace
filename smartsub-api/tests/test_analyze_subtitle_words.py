#!/usr/bin/env python3
"""
Test unitaire pour _analyze_subtitle_words()
Teste la détection en 2 phases des noms propres
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from subtitle_fusion import SubtitleFusionEngine


def test_analyze_subtitle_words():
    """Test de la nouvelle méthode d'analyse"""
    print("=" * 70)
    print("TEST: _analyze_subtitle_words() - Détection noms propres en 2 phases")
    print("=" * 70)

    # Initialize engine
    engine = SubtitleFusionEngine()

    # Mock data pour le test
    # known_words = top 1000 mots français (simulé)
    known_words = {
        "il", "être", "avoir", "que", "ne", "dans", "ce", "qui", "pas",
        "pour", "sur", "se", "son", "plus", "par", "je", "avec", "tout",
        "faire", "nous", "mettre", "autre", "on", "mais", "leur", "comme",
        "ou", "si", "avant", "dire", "elle", "devoir", "donner", "deux",
        "même", "prendre", "où", "aussi", "celui", "bien", "entre", "sans",
        "manger",  # rang ~27, dans top 1000
        "du", "pain", "habiter", "et"  # Ajout pour les tests
    }

    # full_frequency_list = TOUS les mots français (5000, simulé)
    full_frequency_list = known_words.copy()
    full_frequency_list.update({
        "osciller",  # Rang 3542, PAS dans top 1000
        "génial",  # Mot rare mais réel
        "appartenir",  # Forme lemmatisée
    })

    print("\n📊 Configuration test:")
    print(f"   known_words (top 1000): {len(known_words)} mots")
    print(f"   full_frequency_list: {len(full_frequency_list)} mots")
    print()

    # Test 1: Mot normal au début (dans known_words)
    print("─" * 70)
    print("Test 1: 'Il mange du pain'")
    print("   Attendu: 'Il' potentiel → dans known_words → CONNU")
    print("           'mange' normal → lemme 'manger' → dans known_words → CONNU")

    result = engine._analyze_subtitle_words(
        "Il mange du pain",
        "fr",
        known_words,
        full_frequency_list
    )

    print(f"\n   Résultat:")
    print(f"   - Mots normalisés: {result['normalized_words']}")
    print(f"   - Lemmes: {result['lemmatized_words']}")
    print(f"   - Statuts: {result['word_statuses']}")
    print(f"   - Noms propres: {result['proper_nouns']}")
    print(f"   - Mots inconnus: {result['unknown_words']}")

    assert result['unknown_words'] == [], f"Expected no unknown words, got {result['unknown_words']}"
    print("   ✅ Test 1 PASS\n")

    # Test 2: Nom propre confirmé au milieu
    print("─" * 70)
    print("Test 2: 'Il habite à Netflix'")
    print("   Attendu: 'Il' potentiel → dans known_words → CONNU")
    print("           'Netflix' confirmé propre → CONNU (pas lemmatisé)")

    result = engine._analyze_subtitle_words(
        "Il habite à Netflix",
        "fr",
        known_words,
        full_frequency_list
    )

    print(f"\n   Résultat:")
    print(f"   - Mots normalisés: {result['normalized_words']}")
    print(f"   - Noms propres: {result['proper_nouns']}")
    print(f"   - Mots inconnus: {result['unknown_words']}")

    assert "netflix" in result['proper_nouns'], f"Expected 'netflix' in proper nouns"
    assert result['unknown_words'] == [], f"Expected no unknown words"
    print("   ✅ Test 2 PASS\n")

    # Test 3: Mot rare au début (dans full_list mais PAS dans known_words)
    print("─" * 70)
    print("Test 3: 'Oscille entre deux'")
    print("   Attendu: 'Oscille' potentiel → lemme 'osciller'")
    print("           → PAS dans known_words")
    print("           → DANS full_frequency_list")
    print("           → MOT INCONNU (à traduire)")

    result = engine._analyze_subtitle_words(
        "Oscille entre deux",
        "fr",
        known_words,
        full_frequency_list
    )

    print(f"\n   Résultat:")
    print(f"   - Mots normalisés: {result['normalized_words']}")
    print(f"   - Lemmes: {result['lemmatized_words']}")
    print(f"   - Mots inconnus: {result['unknown_words']}")

    assert "oscille" in result['unknown_words'], f"Expected 'oscille' in unknown words"
    assert "oscille" not in result['proper_nouns'], f"'oscille' should not be a proper noun"
    print("   ✅ Test 3 PASS\n")

    # Test 4: Vrai nom propre au début (pas dans full_list)
    print("─" * 70)
    print("Test 4: 'Netflix est génial'")
    print("   Attendu: 'Netflix' potentiel → lemme 'netflix'")
    print("           → PAS dans known_words")
    print("           → PAS dans full_frequency_list")
    print("           → NOM PROPRE (considéré connu)")

    result = engine._analyze_subtitle_words(
        "Netflix est génial",
        "fr",
        known_words,
        full_frequency_list
    )

    print(f"\n   Résultat:")
    print(f"   - Mots normalisés: {result['normalized_words']}")
    print(f"   - Noms propres: {result['proper_nouns']}")
    print(f"   - Mots inconnus: {result['unknown_words']}")

    assert "netflix" in result['proper_nouns'], f"Expected 'netflix' in proper nouns"
    assert "netflix" not in result['unknown_words'], f"'netflix' should not be unknown"
    print("   ✅ Test 4 PASS\n")

    # Test 5: Marie-Antoinette (le cas original!)
    print("─" * 70)
    print("Test 5: 'Il a appartenu à Marie-Antoinette et il'")
    print("   Attendu: 'Marie' et 'Antoinette' au milieu → noms propres confirmés")
    print("           'et' normal → connu")

    result = engine._analyze_subtitle_words(
        "Il a appartenu à Marie-Antoinette et il",
        "fr",
        known_words,
        full_frequency_list
    )

    print(f"\n   Résultat:")
    print(f"   - Mots normalisés: {result['normalized_words']}")
    print(f"   - Noms propres: {result['proper_nouns']}")
    print(f"   - Mots inconnus: {result['unknown_words']}")

    assert "marie" in result['proper_nouns'], f"Expected 'marie' in proper nouns"
    assert "antoinette" in result['proper_nouns'], f"Expected 'antoinette' in proper nouns"
    assert "et" not in result['unknown_words'], f"'et' should be known"
    print("   ✅ Test 5 PASS - Le cas original fonctionne!\n")

    print("=" * 70)
    print("🎉 TOUS LES TESTS PASSENT!")
    print("=" * 70)


if __name__ == "__main__":
    test_analyze_subtitle_words()
