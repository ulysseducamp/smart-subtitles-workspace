#!/usr/bin/env python3
"""
Test script pour vérifier la validation API key
"""

import requests
import os
from dotenv import load_dotenv

# Charger automatiquement le fichier .env
load_dotenv()

# Configuration
BASE_URL = "http://localhost:3000"
API_KEY = os.getenv("API_KEY")  # Utilise la variable d'environnement comme le reste du code

def test_without_api_key():
    """Test sans API key - doit retourner 401"""
    print("🔒 Test sans API key...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"❌ Échec: Status {response.status_code}")
        print(f"   Réponse: {response.json()}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_with_valid_api_key():
    """Test avec API key valide - doit fonctionner"""
    print("\n✅ Test avec API key valide...")
    try:
        response = requests.get(f"{BASE_URL}/?api_key={API_KEY}")
        print(f"✅ Succès: Status {response.status_code}")
        print(f"   Réponse: {response.json()}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_health_endpoint():
    """Test endpoint /health - doit toujours fonctionner"""
    print("\n🏥 Test endpoint /health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Succès: Status {response.status_code}")
        print(f"   Réponse: {response.json()}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🧪 Test de la validation API key")
    print("=" * 40)
    
    # Vérifier que la clé API est disponible
    if not API_KEY:
        print("❌ Erreur: API_KEY non trouvée dans le fichier .env")
        print("   Assurez-vous que le fichier .env contient: API_KEY=ta_cle_ici")
        exit(1)
    
    test_without_api_key()
    test_with_valid_api_key()
    test_health_endpoint()
    
    print("\n" + "=" * 40)
    print("�� Tests terminés!")
