#!/usr/bin/env python3
"""
Script de diagnostic pour les décisions de vocabulaire
Permet de comprendre pourquoi certains mots sont traduits à tort
"""

import sys
sys.path.append('src')

from frequency_loader import FrequencyLoader
import simplemma

def diagnose_word_decision(word_original: str, language: str = 'pt', top_n: int = 800):
    """Diagnostique complète pour une décision de mot"""

    print(f"\n=== DIAGNOSTIC POUR: '{word_original}' (langue: {language}, seuil: {top_n}) ===\n")

    loader = FrequencyLoader()

    # 1. Test du mot original
    rank_original = loader.get_word_rank(word_original, language, top_n)
    print(f"1. Mot original: '{word_original}'")
    print(f"   → Rang dans top {top_n}: {rank_original}")
    print(f"   → Statut: {'CONNU' if rank_original else 'INCONNU'}")

    # 2. Test de lemmatisation
    word_lemmatized = simplemma.lemmatize(word_original, lang=language)
    print(f"\n2. Lemmatisation: '{word_original}' → '{word_lemmatized}'")

    if word_lemmatized != word_original:
        rank_lemma = loader.get_word_rank(word_lemmatized, language, top_n)
        print(f"   → Rang du lemme dans top {top_n}: {rank_lemma}")
        print(f"   → Statut du lemme: {'CONNU' if rank_lemma else 'INCONNU'}")
    else:
        print(f"   → Pas de changement lors de la lemmatisation")

    # 3. Simulation de la logique actuelle
    print(f"\n3. Logique actuelle de l'algorithme:")
    known_words = loader.get_top_n_words(language, top_n)
    word_lower = word_lemmatized.lower()

    is_known_current = word_lower in known_words
    print(f"   → Recherche: '{word_lower}' dans known_words")
    print(f"   → Résultat: {'CONNU' if is_known_current else 'INCONNU'}")
    print(f"   → Action: {'GARDER' if is_known_current else 'TRADUIRE'}")

    # 4. Logique proposée (mot original + lemme)
    print(f"\n4. Logique améliorée proposée:")
    word_original_lower = word_original.lower()
    is_known_improved = (word_original_lower in known_words) or (word_lower in known_words)
    print(f"   → Test 1: '{word_original_lower}' dans known_words = {word_original_lower in known_words}")
    print(f"   → Test 2: '{word_lower}' dans known_words = {word_lower in known_words}")
    print(f"   → Résultat combiné: {'CONNU' if is_known_improved else 'INCONNU'}")
    print(f"   → Action: {'GARDER' if is_known_improved else 'TRADUIRE'}")

    # 5. Analyse du problème
    print(f"\n5. Analyse:")
    if rank_original and not is_known_current:
        print(f"   🚨 PROBLÈME IDENTIFIÉ: Le mot original '{word_original}' (rang {rank_original}) devrait être CONNU")
        print(f"      mais est traité comme INCONNU car son lemme '{word_lemmatized}' n'est pas dans le top {top_n}")
        print(f"   💡 SOLUTION: Vérifier AUSSI le mot original avant lemmatisation")
    elif not rank_original and is_known_current:
        print(f"   🚨 PROBLÈME IDENTIFIÉ: Le lemme '{word_lemmatized}' est CONNU mais le mot original '{word_original}' ne l'est pas")
    else:
        print(f"   ✅ Logique cohérente")

    return {
        'word_original': word_original,
        'word_lemmatized': word_lemmatized,
        'rank_original': rank_original,
        'rank_lemma': loader.get_word_rank(word_lemmatized, language, top_n) if word_lemmatized != word_original else None,
        'is_known_current': is_known_current,
        'is_known_improved': is_known_improved,
        'needs_fix': rank_original and not is_known_current
    }

if __name__ == "__main__":
    # Tests avec les mots problématiques
    test_words = ['gostaria', 'esquecer', 'você', 'para', 'que']

    results = []
    for word in test_words:
        result = diagnose_word_decision(word)
        results.append(result)

    # Résumé des problèmes
    problems = [r for r in results if r['needs_fix']]
    print(f"\n\n=== RÉSUMÉ ===")
    print(f"Mots testés: {len(test_words)}")
    print(f"Problèmes identifiés: {len(problems)}")

    if problems:
        print(f"\nMots nécessitant une correction:")
        for p in problems:
            print(f"  - '{p['word_original']}' (rang {p['rank_original']}) → lemme '{p['word_lemmatized']}'")