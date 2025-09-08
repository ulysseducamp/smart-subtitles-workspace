#!/usr/bin/env python3
"""
Test diagnostic pour l'API Railway - Test EN -> FR
"""

import requests
import json
from pathlib import Path

def test_en_to_fr():
    """Test EN -> FR avec différents niveaux de vocabulaire"""
    
    # Configuration
    base_url = "https://smartsub-api-production.up.railway.app"
    endpoint = "/fuse-subtitles"
    api_key = "sk-smartsub-abc123def456ghi789"
    
    # Fichiers de test
    script_dir = Path(__file__).parent
    target_srt = script_dir / "smartsub-api" / "tests" / "test_data" / "en.srt"
    native_srt = script_dir / "smartsub-api" / "tests" / "test_data" / "fr.srt"
    
    print("🧪 Test diagnostic EN -> FR")
    print(f"📁 Target SRT: {target_srt}")
    print(f"📁 Native SRT: {native_srt}")
    
    # Vérifier que les fichiers existent
    if not target_srt.exists():
        print(f"❌ Fichier target manquant: {target_srt}")
        return
    if not native_srt.exists():
        print(f"❌ Fichier native manquant: {native_srt}")
        return
    
    # Test avec différents niveaux de vocabulaire
    vocabulary_levels = [100, 500, 1000, 2000, 3000]
    
    for vocab_level in vocabulary_levels:
        print(f"\n{'='*60}")
        print(f"🧪 Test avec vocabulaire: {vocab_level} mots")
        print(f"{'='*60}")
        
        # Préparer les fichiers
        files = {
            'target_srt': open(target_srt, 'rb'),
            'native_srt': open(native_srt, 'rb')
        }
        
        # Paramètres
        data = {
            'target_language': 'en',
            'native_language': 'fr', 
            'top_n_words': vocab_level,
            'enable_inline_translation': False
        }
        
        # Paramètres URL
        params = {'api_key': api_key}
        
        try:
            # Faire la requête
            url = f"{base_url}{endpoint}"
            print(f"🌐 URL: {url}")
            print(f"📊 Paramètres: {data}")
            
            response = requests.post(url, files=files, data=data, params=params, timeout=60)
            
            print(f"📈 Status Code: {response.status_code}")
            print(f"⏱️  Response Time: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print("✅ Succès!")
                    
                    # Analyser les statistiques
                    if 'stats' in result:
                        stats = result['stats']
                        print(f"📊 Statistiques:")
                        for key, value in stats.items():
                            print(f"   {key}: {value}")
                    
                    # Analyser le contenu SRT
                    if 'output_srt' in result:
                        output_srt = result['output_srt']
                        lines = output_srt.split('\n')
                        
                        # Compter les lignes de sous-titres (pas les numéros ni les timestamps)
                        subtitle_lines = []
                        for line in lines:
                            line = line.strip()
                            if line and not line.isdigit() and '-->' not in line:
                                subtitle_lines.append(line)
                        
                        print(f"📝 Nombre de sous-titres: {len(subtitle_lines)}")
                        
                        # Afficher les premiers sous-titres
                        print(f"📖 Premiers sous-titres:")
                        for i, line in enumerate(subtitle_lines[:5]):
                            print(f"   {i+1}: {line}")
                        
                        if len(subtitle_lines) > 5:
                            print(f"   ... ({len(subtitle_lines) - 5} autres)")
                    
                except json.JSONDecodeError:
                    print("❌ Réponse JSON invalide")
                    print(f"📄 Contenu: {response.text[:500]}")
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(f"📄 Contenu: {response.text}")
                
        except Exception as e:
            print(f"💥 Erreur: {e}")
            
        finally:
            # Fermer les fichiers
            for file_handle in files.values():
                file_handle.close()

if __name__ == "__main__":
    test_en_to_fr()
