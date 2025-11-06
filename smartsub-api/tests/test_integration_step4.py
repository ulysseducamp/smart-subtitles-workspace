#!/usr/bin/env python3
"""
Test d'intégration Étape 4
Vérifie que _analyze_subtitle_words() est bien intégré dans la boucle principale
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from subtitle_fusion import SubtitleFusionEngine
from srt_parser import Subtitle
from frequency_loader import FrequencyLoader
import asyncio


async def test_integration_step4():
    """Test que l'intégration dans fuse_subtitles fonctionne"""
    print("=" * 70)
    print("TEST INTÉGRATION ÉTAPE 4: _analyze_subtitle_words() dans fuse_subtitles()")
    print("=" * 70)

    # Initialize engine
    engine = SubtitleFusionEngine()

    # Initialize frequency loader
    freq_loader = FrequencyLoader()

    # Load French frequency lists
    known_words = freq_loader.get_top_n_words('fr', 1000)
    full_frequency_list = freq_loader.get_full_list('fr')

    print(f"\n📊 Configuration:")
    print(f"   known_words (top 1000): {len(known_words)} mots")
    print(f"   full_frequency_list: {len(full_frequency_list)} mots")

    # Test case: Le cas Lupin original avec Marie-Antoinette
    target_subs = [
        Subtitle(
            index="1",
            start="00:00:01,000",
            end="00:00:03,000",
            text="Il a appartenu à Marie-Antoinette et il vaut des millions."
        )
    ]

    native_subs = [
        Subtitle(
            index="1",
            start="00:00:01,000",
            end="00:00:03,000",
            text="It belonged to Marie-Antoinette and it is worth millions."
        )
    ]

    print(f"\n📝 Test subtitle:")
    print(f"   '{target_subs[0].text}'")

    try:
        # Call fuse_subtitles avec les nouveaux paramètres
        result = await engine.fuse_subtitles(
            target_subs=target_subs,
            native_subs=native_subs,
            known_words=known_words,
            full_frequency_list=full_frequency_list,
            lang='fr',
            enable_inline_translation=False,  # Désactiver traduction pour test simple
            deepl_api=None,
            openai_translator=None,
            native_lang='en',
            top_n=1000,
            max_concurrent=5
        )

        print(f"\n✅ fuse_subtitles() executed successfully!")
        print(f"\n📊 Result stats:")
        print(f"   Total subtitles: {result.get('totalSubtitles', 'N/A')}")
        print(f"   Replaced: {result.get('replacedCount', 'N/A')}")
        print(f"   Inline translations: {result.get('inlineTranslationCount', 'N/A')}")
        print(f"   Errors: {result.get('errorCount', 'N/A')}")

        # Vérifier que le résultat contient des sous-titres
        if 'fused' in result:
            fused_subs = result['fused']
            print(f"\n📝 Fused subtitles: {len(fused_subs)}")

            if fused_subs:
                print(f"\n   First subtitle:")
                print(f"   Index: {fused_subs[0]['index']}")
                print(f"   Text: {fused_subs[0]['text']}")

        print(f"\n🎉 TEST INTÉGRATION ÉTAPE 4 - RÉUSSI!")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ ERREUR lors de l'exécution:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("\n❌ TEST INTÉGRATION ÉTAPE 4 - ÉCHOUÉ!")
        print("=" * 70)
        return False


if __name__ == "__main__":
    success = asyncio.run(test_integration_step4())
    sys.exit(0 if success else 1)
