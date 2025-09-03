#!/usr/bin/env python3
"""
Test script for the /fuse-subtitles endpoint
Tests the real CLI integration
"""

import requests
import os

def test_fuse_subtitles():
    """Test the fuse-subtitles endpoint with real files"""
    
    # URL de l'API
    url = "http://127.0.0.1:3000/fuse-subtitles"
    
    # Chemin vers les fichiers de test
    target_srt = "../subtitles-fusion-algorithm-public/fr.srt"
    native_srt = "../subtitles-fusion-algorithm-public/en.srt"
    frequency_list = "../subtitles-fusion-algorithm-public/frequency-lists/fr-5000.txt"
    
    # Vérifier que les fichiers existent
    for file_path in [target_srt, native_srt, frequency_list]:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
    
    print("✅ All test files found")
    
    # Préparer les données de la requête
    data = {
        "target_language": "fr",
        "native_language": "en", 
        "top_n_words": 2000,
        "enable_inline_translation": False
    }
    
    # Préparer les fichiers
    files = {
        "target_srt": ("fr.srt", open(target_srt, "rb"), "text/plain"),
        "native_srt": ("en.srt", open(native_srt, "rb"), "text/plain"),
        "frequency_list": ("fr-5000.txt", open(frequency_list, "rb"), "text/plain")
    }
    
    try:
        print("🚀 Sending request to /fuse-subtitles...")
        print(f"📝 Target language: {data['target_language']}")
        print(f"📝 Native language: {data['native_language']}")
        print(f"📊 Top N words: {data['top_n_words']}")
        
        # Envoyer la requête - FastAPI attend les paramètres comme Form data
        response = requests.post(url, data=data, files=files)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"📊 Processing time: {result['stats']['processing_time']}")
            print(f"📁 Output SRT size: {len(result['output_srt'])} characters")
            print(f"📊 Files processed: {result['stats']['files_processed']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
        
    finally:
        # Fermer les fichiers
        for file_obj in files.values():
            file_obj[1].close()

if __name__ == "__main__":
    print("🧪 Testing /fuse-subtitles endpoint...")
    success = test_fuse_subtitles()
    
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")

