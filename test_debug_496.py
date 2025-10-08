#!/usr/bin/env python3
"""
Debug script to trace PT 496 specifically
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'smartsub-api/src'))

from srt_parser import parse_srt
from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import get_frequency_loader, initialize_frequency_loader
from pathlib import Path
import asyncio
import logging

# Configure logging to see INFO logs
logging.basicConfig(level=logging.INFO, format='%(message)s')

async def debug_pt_496():
    """Debug why PT 496 disappears"""

    # Initialize frequency loader
    freq_lists_path = Path(__file__).parent / 'smartsub-api' / 'src' / 'frequency_lists'
    initialize_frequency_loader(freq_lists_path)

    # Parse SRT files
    with open("Berlin.S01E08.Un éléphant menacé d'extinction.pt-BR.srt", "r", encoding="utf-8") as f:
        pt_subs = parse_srt(f.read())
    with open("Berlin.S01E08.Un éléphant menacé d'extinction.fr.srt", "r", encoding="utf-8") as f:
        fr_subs = parse_srt(f.read())

    # Find PT 496
    pt_496 = next((s for s in pt_subs if s.index == "496"), None)
    print(f"🔍 PT 496: {pt_496.start} → {pt_496.end}")
    print(f"   Text: {pt_496.text}")

    # Find all subtitles before and after PT 496
    pt_495 = next((s for s in pt_subs if s.index == "495"), None)
    pt_497 = next((s for s in pt_subs if s.index == "497"), None)

    print(f"\n📍 Context:")
    print(f"   PT 495: {pt_495.start} → {pt_495.end} | {pt_495.text}")
    print(f"   PT 496: {pt_496.start} → {pt_496.end} | {pt_496.text}")
    print(f"   PT 497: {pt_497.start} → {pt_497.end} | {pt_497.text}")

    # Load known words
    frequency_loader = get_frequency_loader()
    known_words = frequency_loader.get_top_n_words('pt', 800)

    # Check words in PT 496
    from srt_parser import normalize_words
    from lemmatizer import smart_lemmatize_line
    import re

    text_no_html = re.sub(r'<[^>]*>', '', pt_496.text)
    text_no_brackets = re.sub(r'\[.*?\]', '', text_no_html)
    normalized_words = normalize_words(text_no_brackets)
    lemmatized_words = smart_lemmatize_line(' '.join(normalized_words), 'pt') if normalized_words else []

    print(f"\n📝 Word analysis for PT 496:")
    print(f"   Original: {text_no_brackets}")
    print(f"   Normalized: {normalized_words}")
    print(f"   Lemmatized: {lemmatized_words}")

    for word in lemmatized_words:
        is_known = word.lower() in known_words
        rank = frequency_loader.get_word_rank(word, 'pt', 800)
        status = f"✅ KNOWN (rank {rank})" if is_known else "❌ UNKNOWN"
        print(f"      '{word}' → {status}")

    # Run fusion and track PT 496
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

    # Check if PT 496 timestamp exists in output
    found = None
    for sub in result['hybrid']:
        if sub.start == pt_496.start and sub.end == pt_496.end:
            found = sub
            break

    if found:
        print(f"\n✅ PT 496 FOUND in output as index {found.index}")
        print(f"   Text: {found.text}")
    else:
        print(f"\n❌ PT 496 NOT FOUND in output")

        # Check if replaced by FR subtitle
        print(f"\n🔎 Checking for FR replacement...")
        for sub in result['hybrid']:
            # Check if timestamp overlaps with PT 496
            engine_obj = SubtitleFusionEngine()
            if engine_obj._has_intersection(sub.start, sub.end, pt_496.start, pt_496.end):
                print(f"   Found overlapping subtitle: Index {sub.index} | {sub.start} → {sub.end}")
                print(f"   Text: {sub.text}")

if __name__ == "__main__":
    asyncio.run(debug_pt_496())
