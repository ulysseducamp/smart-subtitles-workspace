#!/usr/bin/env python3
"""
Test script to reproduce subtitle synchronization issues
Tests with Berlin S01E08 SRT files
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'smartsub-api/src'))

from srt_parser import parse_srt
from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import get_frequency_loader, initialize_frequency_loader
import asyncio
import os

def analyze_specific_subtitles():
    """Analyze the specific subtitles reported as missing"""

    # Parse SRT files
    print("📁 Parsing SRT files...")
    with open("Berlin.S01E08.Un éléphant menacé d'extinction.pt-BR.srt", "r", encoding="utf-8") as f:
        pt_subs = parse_srt(f.read())
    with open("Berlin.S01E08.Un éléphant menacé d'extinction.fr.srt", "r", encoding="utf-8") as f:
        fr_subs = parse_srt(f.read())

    print(f"✅ PT subtitles: {len(pt_subs)}")
    print(f"✅ FR subtitles: {len(fr_subs)}")

    # Check specific missing subtitles
    missing_cases = [
        {"pt_index": "496", "pt_time": "00:32:49,125 --> 00:32:52,166", "fr_indices": ["494", "495"]},
        {"pt_index": "513", "pt_time": "00:33:50,000 --> 00:33:51,416", "fr_indices": ["511"]},
        {"pt_index": "764", "pt_time": "00:52:10,875 --> 00:52:15,083", "fr_indices": ["759"]},
        {"pt_index": "767", "pt_time": "00:52:24,500 --> 00:52:27,083", "fr_indices": ["761"]},
    ]

    print("\n🔍 Analyzing specific missing subtitle cases...")
    for case in missing_cases:
        pt_sub = next((s for s in pt_subs if s.index == case["pt_index"]), None)
        if pt_sub:
            print(f"\n📌 PT {case['pt_index']}: {pt_sub.start} → {pt_sub.end}")
            print(f"   Text: {pt_sub.text}")

            # Find intersecting FR subtitles
            engine = SubtitleFusionEngine()
            fr_matches = [
                s for s in fr_subs
                if engine._has_intersection(pt_sub.start, pt_sub.end, s.start, s.end)
            ]
            print(f"   Intersecting FR subtitles: {[s.index for s in fr_matches]}")
            for fr in fr_matches:
                print(f"      FR {fr.index}: {fr.start} → {fr.end} | {fr.text}")

async def test_fusion_with_800_words():
    """Test fusion with 800 word threshold (user's test condition)"""

    print("\n🧪 Testing fusion with 800-word threshold...")

    # Parse SRT files
    with open("Berlin.S01E08.Un éléphant menacé d'extinction.pt-BR.srt", "r", encoding="utf-8") as f:
        pt_subs = parse_srt(f.read())
    with open("Berlin.S01E08.Un éléphant menacé d'extinction.fr.srt", "r", encoding="utf-8") as f:
        fr_subs = parse_srt(f.read())

    # Load frequency words
    frequency_loader = get_frequency_loader()
    known_words = frequency_loader.get_top_n_words('pt', 800)

    print(f"📚 Known words (PT, top 800): {len(known_words)} words")

    # Run fusion
    engine = SubtitleFusionEngine()
    result = await engine.fuse_subtitles(
        target_subs=pt_subs,
        native_subs=fr_subs,
        known_words=known_words,
        lang='pt',
        enable_inline_translation=True,
        native_lang='fr',
        top_n=800
    )

    print(f"\n📊 Fusion Results:")
    print(f"   Total output subtitles: {len(result['hybrid'])}")
    print(f"   Replaced: {result['replacedCount']}")
    print(f"   Inline translations: {result['inlineTranslationCount']}")

    # Check if specific subtitles are in output
    output_indices = [s.index for s in result['hybrid']]
    missing_cases = ["496", "513", "764", "767"]

    print(f"\n🔎 Checking for reported missing subtitles...")
    for idx in missing_cases:
        # Find in output by timestamp instead of index (index gets rewritten)
        pt_sub = next((s for s in pt_subs if s.index == idx), None)
        if pt_sub:
            found = any(
                s.start == pt_sub.start and s.end == pt_sub.end
                for s in result['hybrid']
            )
            status = "✅ FOUND" if found else "❌ MISSING"
            print(f"   PT {idx} ({pt_sub.start} → {pt_sub.end}): {status}")

    # Check ordering of output
    print(f"\n📋 Output subtitle ordering (first 20):")
    for i, sub in enumerate(result['hybrid'][:20]):
        print(f"   {i+1}. Index={sub.index} | {sub.start} → {sub.end}")

    # Check if timestamps are in order
    timestamps_ordered = all(
        engine._srt_time_to_ms(result['hybrid'][i].start) <=
        engine._srt_time_to_ms(result['hybrid'][i+1].start)
        for i in range(len(result['hybrid']) - 1)
    )
    print(f"\n⏱️  Timestamps in chronological order: {'✅ YES' if timestamps_ordered else '❌ NO'}")

    return result

if __name__ == "__main__":
    print("🚀 Subtitle Synchronization Bug Test\n")

    # Initialize frequency loader
    from pathlib import Path
    freq_lists_path = Path(__file__).parent / 'smartsub-api' / 'src' / 'frequency_lists'
    initialize_frequency_loader(freq_lists_path)

    # Analyze specific cases
    analyze_specific_subtitles()

    # Test fusion
    asyncio.run(test_fusion_with_800_words())
