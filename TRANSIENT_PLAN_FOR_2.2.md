# PLAN TRANSIENT POUR ÉTAPE 2.2 : Déploiement Railway

## 📋 Vue d'ensemble
**Objectif** : Déployer l'API FastAPI sur Railway pour la rendre accessible sur internet
**Prérequis** : Compte Railway, projet Git configuré
**Durée estimée** : 2-3 heures
**Difficulté** : Moyenne

---

## 🚀 PHASE 1 : Préparation du Projet

### 1.1 Vérification de la Structure
- [x] Vérifier que `smartsub-api/` contient tous les fichiers nécessaires
- [x] S'assurer que `requirements.txt` est à jour
- [x] Vérifier que `main.py` fonctionne localement

### 1.2 Création des Fichiers de Configuration Railway
- [x] Créer `railway.toml` à la racine du projet
- [x] Créer `Procfile` pour Railway
- [x] Vérifier la configuration CORS dans `main.py`

---

## 🔐 PHASE 1.5 : Sécurisation avec API Key Simple

### 1.5.1 Configuration de la Variable d'Environnement
1. **Dans l'onglet "Variables" de Railway :**
   - [ ] Ajouter `API_KEY` = [générer une clé secrète aléatoire]
   - [ ] Exemple de clé : `sk-smartsub-abc123def456ghi789`

### 1.5.2 Modification du Code pour Sécurisation
- [x] Modifier `main.py` pour vérifier l'API key
- [x] Ajouter middleware de validation API key
- [x] Tester la sécurisation localement
- [ ] Commiter et pousser les changements

### 1.5.3 Création du Fichier .env.example
- [ ] Créer `.env.example` avec des valeurs factices
- [ ] Ajouter `.env` au `.gitignore` (si pas déjà fait)

---

## 🔧 PHASE 2 : Configuration Railway

### 2.1 Création du Projet Railway
1. **Aller sur [railway.app](https://railway.app)**
2. **Se connecter avec GitHub**
3. **Cliquer sur "New Project"**
4. **Choisir "Deploy from GitHub repo"**
5. **Sélectionner votre repository `smart-subtitles-workspace`**
6. **Nommer le projet** : `smartsub-api`

### 2.2 Configuration du Déploiement
1. **Dans l'onglet "Settings" du projet Railway :**
   - [x] Vérifier que la branche par défaut est `main`
   - [x] Activer "Auto Deploy" si disponible
   - [ ] Cliquer sur "Generate Domain" dans la section "Networking"
   - [ ] Noter l'URL générée (ex: `https://smartsub-api-production.up.railway.app`)

### 2.3 Configuration des Variables d'Environnement
Dans l'onglet "Variables" de Railway, ajouter :
- [ ] `PORT` = `8000`
- [ ] `PYTHON_VERSION` = `3.11`
- [ ] `API_KEY` = [clé générée à l'étape 1.5.1]
- [ ] `DEEPL_API_KEY` = [votre clé DeepL si disponible]
- [ ] `SUPABASE_URL` = [URL de votre base Supabase]
- [ ] `SUPABASE_KEY` = [Clé de votre base Supabase]

---

## 🚀 PHASE 3 : Déploiement

### 3.1 Premier Déploiement
1. **Railway va automatiquement détecter le projet Python**
2. **Attendre que le build se termine** (2-5 minutes)
3. **Vérifier les logs de build** dans l'onglet "Deployments"
4. **Noter l'URL finale** du déploiement

### 3.2 Vérification du Déploiement
- [ ] Tester l'endpoint `/` : `https://[url-railway]/`
- [ ] Tester l'endpoint `/health` : `https://[url-railway]/health`
- [ ] Vérifier que l'API répond correctement

---

## 🧪 PHASE 4 : Tests et Validation

### 4.1 Tests des Endpoints
- [ ] Tester l'accès sans API key (doit retourner 401)
- [ ] Tester l'accès avec API key valide
- [ ] Tester `/fuse-subtitles` avec des fichiers SRT de test
- [ ] Vérifier la gestion des erreurs
- [ ] Tester la limite de taille des fichiers
- [ ] Vérifier la performance

### 4.2 Tests d'Intégration
- [ ] Tester avec l'extension Chrome (si disponible)
- [ ] Vérifier la connectivité depuis différents réseaux
- [ ] Tester la stabilité sur la durée

---

## 🔍 PHASE 5 : Monitoring et Optimisation

### 5.1 Monitoring Railway
- [ ] Configurer les alertes de Railway
- [ ] Surveiller l'utilisation des ressources
- [ ] Vérifier les logs d'erreur

### 5.2 Optimisations
- [ ] Ajuster la configuration si nécessaire
- [ ] Optimiser les performances
- [ ] Documenter les bonnes pratiques

---

## 📝 NOTES ET MODIFICATIONS

### Problèmes Rencontrés
- [ ] 
- [ ] 
- [ ] 

### Solutions Appliquées
- [ ] 
- [ ] 
- [ ] 

### Modifications du Plan
- [ ] 
- [ ] 
- [ ] 

---

## ✅ CHECKLIST FINALE

- [ ] API déployée sur Railway
- [ ] Endpoints accessibles sur internet
- [ ] Tests de base passés
- [ ] Variables d'environnement configurées
- [ ] Documentation mise à jour
- [ ] Prêt pour l'intégration Chrome Extension

---

## 🆘 DÉPANNAGE

### Erreurs Communes
1. **Build échoue** : Vérifier `requirements.txt` et `main.py`
2. **Port déjà utilisé** : Vérifier la variable `PORT`
3. **Variables d'environnement manquantes** : Vérifier la configuration Railway
4. **CORS errors** : Vérifier la configuration CORS dans `main.py`

### Contacts
- Documentation Railway : [docs.railway.app](https://docs.railway.app)
- Support Railway : Via le chat intégré

---

**Dernière mise à jour** : [Date]
**Statut** : En cours
**Prochaine étape** : [À définir]
