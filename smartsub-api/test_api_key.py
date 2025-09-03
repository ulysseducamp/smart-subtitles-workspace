#!/usr/bin/env python3
"""
Test script pour vérifier la validation API key
"""

import requests
import os

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "sk-smartsub-abc123def456ghi789"  # Utilisez la même clé que dans Railway

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
    
    # Définir la variable d'environnement pour le test
    os.environ["API_KEY"] = API_KEY
    
    test_without_api_key()
    test_with_valid_api_key()
    test_health_endpoint()
    
    print("\n" + "=" * 40)
    print("�� Tests terminés!")
