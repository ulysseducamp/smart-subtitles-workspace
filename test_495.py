#!/usr/bin/env python3
"""Check if PT 495 causes PT 496 to be processed"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'smartsub-api/src'))

from srt_parser import parse_srt, normalize_words
from lemmatizer import smart_lemmatize_line
from frequency_loader import get_frequency_loader, initialize_frequency_loader
from subtitle_fusion import SubtitleFusionEngine
from pathlib import Path
import re

# Initialize
freq_lists_path = Path(__file__).parent / 'smartsub-api' / 'src' / 'frequency_lists'
initialize_frequency_loader(freq_lists_path)

# Parse
with open("Berlin.S01E08.Un éléphant menacé d'extinction.pt-BR.srt", "r", encoding="utf-8") as f:
    pt_subs = parse_srt(f.read())
with open("Berlin.S01E08.Un éléphant menacé d'extinction.fr.srt", "r", encoding="utf-8") as f:
    fr_subs = parse_srt(f.read())

# Find PT 495, 496, 497
pt_495 = next((s for s in pt_subs if s.index == "495"), None)
pt_496 = next((s for s in pt_subs if s.index == "496"), None)
pt_497 = next((s for s in pt_subs if s.index == "497"), None)

print(f"PT 495: {pt_495.start} → {pt_495.end}")
print(f"Text: {pt_495.text}")
print(f"\nPT 496: {pt_496.start} → {pt_496.end}")
print(f"Text: {pt_496.text}")
print(f"\nPT 497: {pt_497.start} → {pt_497.end}")
print(f"Text: {pt_497.text}")

# Analyze PT 495
text_no_html = re.sub(r'<[^>]*>', '', pt_495.text)
text_no_brackets = re.sub(r'\[.*?\]', '', text_no_html)
normalized_words = normalize_words(text_no_brackets)
lemmatized_words = smart_lemmatize_line(' '.join(normalized_words), 'pt') if normalized_words else []

print(f"\n=== PT 495 Analysis ===")
print(f"Normalized: {normalized_words}")
print(f"Lemmatized: {lemmatized_words}")

frequency_loader = get_frequency_loader()
known_words = frequency_loader.get_top_n_words('pt', 800)

unknown_count_495 = 0
for word in lemmatized_words:
    is_known = word.lower() in known_words
    rank = frequency_loader.get_word_rank(word, 'pt', 800)
    status = f"✅ KNOWN (rank {rank})" if is_known else "❌ UNKNOWN"
    print(f"   '{word}' → {status}")
    if not is_known:
        unknown_count_495 += 1

print(f"\n🎯 PT 495 has {unknown_count_495} unknown words")

# If PT 495 needs replacement, check intersecting FR
if unknown_count_495 >= 2:
    print("\n→ PT 495 needs REPLACEMENT (2+ unknown words)")

    engine = SubtitleFusionEngine()
    fr_matches = [
        s for s in fr_subs
        if engine._has_intersection(pt_495.start, pt_495.end, s.start, s.end)
    ]

    print(f"\nIntersecting FR subtitles for PT 495: {[s.index for s in fr_matches]}")
    for fr in fr_matches:
        print(f"   FR {fr.index}: {fr.start} → {fr.end}")
        print(f"   Text: {fr.text}")

    # Check if these FR also intersect with PT 496
    if fr_matches:
        combined_start = fr_matches[0].start
        combined_end = fr_matches[-1].end
        print(f"\nCombined FR range: {combined_start} → {combined_end}")

        overlapping_pt = [
            s for s in pt_subs
            if engine._has_intersection(combined_start, combined_end, s.start, s.end)
        ]
        print(f"\nPT subtitles that would be marked as processed: {[s.index for s in overlapping_pt]}")

        if '496' in [s.index for s in overlapping_pt]:
            print("\n🔴 PT 496 WOULD BE MARKED AS PROCESSED by PT 495 replacement!")
else:
    print("\n→ PT 495 does NOT need replacement")
    print("→ PT 496 should be processed independently")
