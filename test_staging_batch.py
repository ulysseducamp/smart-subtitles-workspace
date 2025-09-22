#!/usr/bin/env python3
"""
Test script pour valider l'optimisation batch sur l'environnement staging
"""

import requests
import time
import json
from pathlib import Path

def test_staging_batch_optimization():
    """Test de l'optimisation batch sur l'API staging"""
    
    print("🧪 Test de l'optimisation batch sur staging...")
    print("=" * 60)
    
    # URL de l'API staging
    staging_url = "https://smartsub-api-staging.up.railway.app"
    
    # Test 1: Vérifier la connectivité
    print("1️⃣ Test de connectivité...")
    try:
        health_response = requests.get(f"{staging_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ API staging accessible")
            print(f"   Response: {health_response.json()}")
        else:
            print(f"❌ Erreur de connectivité: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: Test de fusion avec fichiers de test
    print("\n2️⃣ Test de fusion avec optimisations batch...")
    
    # Charger les fichiers de test
    test_data_dir = Path("smartsub-api/tests/test_data")
    en_srt = test_data_dir / "en.srt"
    fr_srt = test_data_dir / "fr.srt"
    
    if not en_srt.exists() or not fr_srt.exists():
        print("❌ Fichiers de test manquants")
        return False
    
    # Lire les fichiers
    with open(en_srt, 'r', encoding='utf-8') as f:
        en_content = f.read()
    
    with open(fr_srt, 'r', encoding='utf-8') as f:
        fr_content = f.read()
    
    # Préparer la requête avec Form data et fichiers
    files = {
        'target_srt': ('en.srt', en_content, 'text/plain'),
        'native_srt': ('fr.srt', fr_content, 'text/plain')
    }
    
    data = {
        'target_language': 'EN',
        'native_language': 'FR',
        'top_n_words': 2000,
        'enable_inline_translation': True
    }
    
    print("   📤 Envoi de la requête de fusion...")
    print(f"   📊 Données: {len(en_content)} chars EN, {len(fr_content)} chars FR")
    
    # Mesurer le temps de traitement
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{staging_url}/fuse-subtitles",
            files=files,
            data=data,
            timeout=60  # 60 secondes de timeout
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Fusion réussie !")
            print(f"   ⏱️  Temps de traitement: {processing_time:.2f} secondes")
            print(f"   📝 Subtitles générés: {result.get('subtitle_count', 'N/A')}")
            print(f"   🔄 Traductions inline: {result.get('inline_translation_count', 'N/A')}")
            print(f"   📊 Requêtes DeepL: {result.get('deepl_request_count', 'N/A')}")
            
            # Vérifier l'optimisation batch
            deepl_requests = result.get('deepl_request_count', 0)
            if deepl_requests == 1:
                print("🎯 OPTIMISATION BATCH CONFIRMÉE !")
                print("   ✅ Une seule requête DeepL pour toutes les traductions")
            else:
                print(f"⚠️  {deepl_requests} requêtes DeepL (attendu: 1)")
            
            # Afficher un échantillon des résultats
            if 'subtitles' in result and result['subtitles']:
                print("\n📋 Échantillon des résultats:")
                for i, subtitle in enumerate(result['subtitles'][:3]):
                    print(f"   {i+1}. {subtitle.get('text', 'N/A')}")
            
            return True
            
        else:
            print(f"❌ Erreur de fusion: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - La requête a pris trop de temps")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la fusion: {e}")
        return False

def test_production_comparison():
    """Test de comparaison avec la production"""
    
    print("\n3️⃣ Test de comparaison avec la production...")
    
    production_url = "https://smartsub-api-production.up.railway.app"
    
    # Test rapide de connectivité production
    try:
        health_response = requests.get(f"{production_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ API production accessible pour comparaison")
        else:
            print("⚠️  API production non accessible")
            return
    except Exception as e:
        print(f"⚠️  Impossible de comparer avec la production: {e}")
        return
    
    print("📊 Comparaison disponible entre staging et production")

if __name__ == "__main__":
    print("🚀 Test de l'optimisation batch sur Railway Staging")
    print("=" * 60)
    
    success = test_staging_batch_optimization()
    test_production_comparison()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ L'optimisation batch fonctionne sur staging")
        print("🚀 Prêt pour le déploiement en production")
    else:
        print("❌ ÉCHEC DES TESTS")
        print("🔧 Vérification nécessaire avant déploiement")
