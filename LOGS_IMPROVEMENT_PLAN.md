# Plan d'Amélioration des Logs de Traitement des Sous-titres

## Objectif
Améliorer la clarté et l'utilité des logs de traitement des sous-titres pour faciliter le debugging et la validation de la qualité du traitement.

## Problèmes identifiés
1. **Logs éparpillés** : Les statistiques sont dispersées entre les logs de traitement
2. **Niveau choisi non affiché** : Le nombre de mots de vocabulaire choisi n'est pas visible
3. **Position des mots non visible** : Impossible de voir le rang des mots dans la liste de fréquence
4. **Limite trop faible** : Seulement 20 sous-titres affichés au lieu de 40
5. **Sous-titre final manquant** : Le texte final affiché à l'utilisateur n'est pas visible

## Structure cible des logs
```
=== CONFIGURATION ===
Niveau choisi: 2000 mots les plus fréquents
Langue cible: pt, Langue native: fr
Traduction inline: activée

=== TRAITEMENT DES SOUS-TITRES (40 premiers) ===
=== SUBTITLE 1 ===
Original: "[efeito sonoro dramático]"
Mots analysés:
  - efeito → rang 1247/2000 (connu)
  - sonoro → rang 1890/2000 (connu) 
  - dramático → inconnu (hors des 2000 premiers)
Décision: remplacé par sous-titre natif
Raison: 1 mot inconnu détecté
Sous-titre final: "[fracas]\n[crescendo]"

=== STATISTIQUES FINALES ===
Total sous-titres cibles: 695
Total sous-titres natifs: 676
Sous-titres gardés en langue cible: 404/695
Sous-titres remplacés par natifs: 291/695 (41.9%)
Sous-titres avec traduction inline: 138/695 (19.9%)
...
```

## Plan d'Action

### Étape 1: Restructuration des logs
**Objectif** : Regrouper les logs en sections claires (Configuration, Traitement, Statistiques)

#### 1.1 Créer la structure de logs regroupés
- [ ] Modifier `main.py` pour afficher la section CONFIGURATION au début
- [ ] Déplacer toutes les statistiques finales vers la fin
- [ ] Créer des séparateurs visuels clairs entre les sections

#### 1.2 Tester la nouvelle structure
- [ ] Exécuter un test de traitement de sous-titres
- [ ] Vérifier que les logs sont bien structurés
- [ ] Valider que toutes les informations sont présentes

### Étape 2: Affichage du niveau choisi
**Objectif** : Afficher clairement le nombre de mots de vocabulaire choisi

#### 2.1 Ajouter l'affichage du niveau
- [ ] Modifier `main.py` pour afficher "Niveau choisi: X mots les plus fréquents"
- [ ] Utiliser le paramètre `top_n_words` reçu de l'utilisateur

#### 2.2 Tester l'affichage du niveau
- [ ] Tester avec différents niveaux (1000, 2000, 5000 mots)
- [ ] Vérifier que l'affichage est correct

### Étape 3: Position des mots dans la liste de fréquence
**Objectif** : Afficher le rang de chaque mot dans la liste de fréquence

#### 3.1 Modifier FrequencyLoader pour retourner le rang
- [ ] Ajouter une méthode `get_word_rank(word, language, top_n)` dans `FrequencyLoader`
- [ ] Cette méthode doit retourner le rang (1-indexed) ou None si le mot n'est pas dans les top_n

#### 3.2 Adapter les logs pour afficher le rang
- [ ] Modifier `subtitle_fusion.py` pour utiliser la nouvelle méthode
- [ ] Afficher "mot → rang X/Y (connu)" ou "mot → inconnu (hors des Y premiers)"

#### 3.3 Tester l'affichage des rangs
- [ ] Tester avec des mots connus et inconnus
- [ ] Vérifier que les rangs sont corrects
- [ ] Valider que les performances ne sont pas dégradées

### Étape 4: Affichage du sous-titre final
**Objectif** : Afficher le texte final qui sera montré à l'utilisateur pour chaque sous-titre

#### 4.1 Stocker les informations de debug
- [ ] Créer une structure pour stocker les infos de debug de chaque sous-titre
- [ ] Inclure le texte final qui sera affiché

#### 4.2 Afficher les logs après le batch translation
- [ ] Modifier le flux pour afficher les logs de debug après le batch translation
- [ ] Inclure le sous-titre final avec les traductions inline appliquées

#### 4.3 Tester l'affichage du sous-titre final
- [ ] Tester avec des sous-titres ayant des traductions inline
- [ ] Vérifier que le texte final est correct
- [ ] Valider que tous les types de sous-titres sont bien affichés

### Étape 5: Augmenter la limite à 40 sous-titres
**Objectif** : Afficher 40 sous-titres au lieu de 20 pour une meilleure analyse

#### 5.1 Modifier la limite
- [ ] Changer `debug_shown < 20` vers `debug_shown < 40` dans `subtitle_fusion.py`

#### 5.2 Tester la nouvelle limite
- [ ] Exécuter un test avec plus de 40 sous-titres
- [ ] Vérifier que 40 sous-titres sont bien affichés
- [ ] Valider que les performances restent acceptables

## Critères de validation
- [ ] Les logs sont clairs et structurés
- [ ] Toutes les informations importantes sont visibles
- [ ] Les performances ne sont pas dégradées
- [ ] Le système fonctionne avec tous les types de sous-titres
- [ ] Les tests passent sans erreur

## Fichiers à modifier
- `smartsub-api/main.py` : Structure des logs et affichage du niveau
- `smartsub-api/src/frequency_loader.py` : Méthode pour obtenir le rang des mots
- `smartsub-api/src/subtitle_fusion.py` : Logs détaillés et affichage du sous-titre final

## Notes techniques
- Maintenir la compatibilité avec le système existant
- Tester chaque étape individuellement
- Garder les performances optimales
- Documenter les changements

---
**Date de création** : Janvier 2025  
**Statut** : En attente de début d'implémentation  
**Prochaine étape** : Étape 1.1 - Créer la structure de logs regroupés
