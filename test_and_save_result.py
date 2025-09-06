#!/usr/bin/env python3
"""
Script pour tester l'algorithme et sauvegarder le résultat complet
"""

import requests
import json
from pathlib import Path

def test_and_save_result():
    # Configuration
    url = "https://smartsub-api-production.up.railway.app/fuse-subtitles"
    api_key = "sk-smartsub-abc123def456ghi789"
    
    # Fichiers de test
    script_dir = Path(__file__).parent
    test_files_dir = script_dir / "subtitles-fusion-algorithm-public"
    
    files = {
        'target_srt': open(test_files_dir / "en.srt", 'rb'),
        'native_srt': open(test_files_dir / "fr.srt", 'rb'),
        'frequency_list': open(test_files_dir / "frequency-lists" / "en-10000.txt", 'rb')
    }
    
    data = {
        'target_language': 'en',
        'native_language': 'fr',
        'top_n_words': 1000,  # Plus petit pour forcer plus de remplacements
        'enable_inline_translation': False
    }
    
    params = {'api_key': api_key}
    
    print("🧪 Test de l'algorithme de fusion de sous-titres...")
    print(f"📁 Fichiers utilisés:")
    print(f"   - Sous-titres anglais: {test_files_dir / 'en.srt'}")
    print(f"   - Sous-titres français: {test_files_dir / 'fr.srt'}")
    print(f"   - Liste de fréquence: {test_files_dir / 'frequency-lists' / 'fr-5000.txt'}")
    print(f"📊 Paramètres: vocabulaire connu = {data['top_n_words']} mots")
    
    try:
        response = requests.post(url, files=files, data=data, params=params, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            output_srt = result.get('output_srt', '')
            
            # Sauvegarder le résultat
            output_file = script_dir / "resultat_fusion_api.srt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_srt)
            
            print(f"\n✅ Succès!")
            print(f"💾 Résultat sauvegardé dans: {output_file}")
            print(f"📊 Taille du résultat: {len(output_srt)} caractères")
            
            # Afficher les premières lignes du résultat
            lines = output_srt.split('\n')[:20]
            print(f"\n📖 Aperçu du résultat (20 premières lignes):")
            for i, line in enumerate(lines, 1):
                print(f"   {i:2d}: {line}")
            
            total_lines = len(output_srt.split('\n'))
            if total_lines > 20:
                print(f"   ... ({total_lines - 20} lignes supplémentaires)")
                
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        for f in files.values():
            f.close()

if __name__ == "__main__":
    test_and_save_result()
