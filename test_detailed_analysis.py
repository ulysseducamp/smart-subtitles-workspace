#!/usr/bin/env python3
"""
Test détaillé pour analyser le traitement des sous-titres avec 1000 mots
"""

import requests
import json
from pathlib import Path

def analyze_subtitle_processing():
    """Analyse détaillée du traitement des sous-titres"""
    
    # Configuration
    base_url = "https://smartsub-api-production.up.railway.app"
    endpoint = "/fuse-subtitles"
    api_key = "sk-smartsub-abc123def456ghi789"
    
    # Fichiers de test
    script_dir = Path(__file__).parent
    target_srt = script_dir / "smartsub-api" / "tests" / "test_data" / "en.srt"
    native_srt = script_dir / "smartsub-api" / "tests" / "test_data" / "fr.srt"
    
    print("🔍 Analyse détaillée du traitement des sous-titres")
    print(f"📊 Niveau de vocabulaire: 1000 mots")
    print(f"🎯 Direction: EN -> FR")
    print("="*80)
    
    # Lire les fichiers originaux pour comparaison
    with open(target_srt, 'r', encoding='utf-8') as f:
        original_en = f.read()
    
    with open(native_srt, 'r', encoding='utf-8') as f:
        original_fr = f.read()
    
    # Parser les sous-titres originaux
    en_subtitles = parse_srt_content(original_en)
    fr_subtitles = parse_srt_content(original_fr)
    
    print(f"📝 Sous-titres anglais originaux: {len(en_subtitles)}")
    print(f"📝 Sous-titres français originaux: {len(fr_subtitles)}")
    print()
    
    # Faire la requête à l'API
    files = {
        'target_srt': open(target_srt, 'rb'),
        'native_srt': open(native_srt, 'rb')
    }
    
    data = {
        'target_language': 'en',
        'native_language': 'fr', 
        'top_n_words': 1000,
        'enable_inline_translation': False
    }
    
    params = {'api_key': api_key}
    
    try:
        url = f"{base_url}{endpoint}"
        response = requests.post(url, files=files, data=data, params=params, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            if 'output_srt' in result:
                processed_srt = result['output_srt']
                processed_subtitles = parse_srt_content(processed_srt)
                
                print(f"📊 Statistiques de traitement:")
                if 'stats' in result:
                    stats = result['stats']
                    for key, value in stats.items():
                        print(f"   {key}: {value}")
                print()
                
                print("🔍 Analyse des 20 premiers sous-titres:")
                print("="*80)
                print(f"{'#':<3} {'Temps':<20} {'Original EN':<30} {'Traité':<30} {'Status'}")
                print("="*80)
                
                # Analyser les 20 premiers sous-titres
                for i in range(min(20, len(processed_subtitles))):
                    processed = processed_subtitles[i]
                    
                    # Trouver le sous-titre anglais correspondant
                    original_en_text = ""
                    if i < len(en_subtitles):
                        original_en_text = en_subtitles[i]['text']
                    
                    # Déterminer le statut
                    if processed['text'] == original_en_text:
                        status = "🟡 GARDÉ (EN)"
                    elif processed['text'] in [sub['text'] for sub in fr_subtitles]:
                        status = "🔴 REMPLACÉ (FR)"
                    else:
                        status = "🟢 MIXTE"
                    
                    # Tronquer les textes pour l'affichage
                    original_display = original_en_text[:27] + "..." if len(original_en_text) > 30 else original_en_text
                    processed_display = processed['text'][:27] + "..." if len(processed['text']) > 30 else processed['text']
                    
                    print(f"{i+1:<3} {processed['start']:<20} {original_display:<30} {processed_display:<30} {status}")
                
                print("="*80)
                print("📊 Légende:")
                print("🟡 GARDÉ (EN) = Sous-titre anglais conservé (mots connus)")
                print("🔴 REMPLACÉ (FR) = Sous-titre remplacé par français (mots inconnus)")
                print("🟢 MIXTE = Sous-titre modifié (traduction partielle)")
                
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"📄 Contenu: {response.text}")
            
    except Exception as e:
        print(f"💥 Erreur: {e}")
        
    finally:
        for file_handle in files.values():
            file_handle.close()

def parse_srt_content(srt_content):
    """Parser le contenu SRT et retourner une liste de sous-titres"""
    subtitles = []
    lines = srt_content.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Chercher un numéro de sous-titre
        if line.isdigit():
            # Numéro trouvé, chercher le timestamp
            if i + 1 < len(lines):
                timestamp_line = lines[i + 1].strip()
                if '-->' in timestamp_line:
                    # Timestamp trouvé, chercher le texte
                    text_lines = []
                    j = i + 2
                    while j < len(lines) and lines[j].strip() != '':
                        text_lines.append(lines[j].strip())
                        j += 1
                    
                    if text_lines:
                        subtitle = {
                            'number': int(line),
                            'start': timestamp_line.split(' --> ')[0],
                            'end': timestamp_line.split(' --> ')[1],
                            'text': ' '.join(text_lines)
                        }
                        subtitles.append(subtitle)
                    
                    i = j
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1
    
    return subtitles

if __name__ == "__main__":
    analyze_subtitle_processing()
