#!/usr/bin/env python3
"""Check PT 763"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'smartsub-api/src'))

from srt_parser import parse_srt, normalize_words
from lemmatizer import smart_lemmatize_line
from frequency_loader import get_frequency_loader, initialize_frequency_loader
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

# Find PT 763
pt_763 = next((s for s in pt_subs if s.index == "763"), None)
print(f"PT 763: {pt_763.start} → {pt_763.end}")
print(f"Text: {pt_763.text}")

# Analyze words
text_no_html = re.sub(r'<[^>]*>', '', pt_763.text)
text_no_brackets = re.sub(r'\[.*?\]', '', text_no_html)
normalized_words = normalize_words(text_no_brackets)
lemmatized_words = smart_lemmatize_line(' '.join(normalized_words), 'pt') if normalized_words else []

print(f"\nNormalized: {normalized_words}")
print(f"Lemmatized: {lemmatized_words}")

# Check known words
frequency_loader = get_frequency_loader()
known_words = frequency_loader.get_top_n_words('pt', 800)

unknown_count = 0
for word in lemmatized_words:
    is_known = word.lower() in known_words
    rank = frequency_loader.get_word_rank(word, 'pt', 800)
    status = f"✅ KNOWN (rank {rank})" if is_known else "❌ UNKNOWN"
    print(f"   '{word}' → {status}")
    if not is_known:
        unknown_count += 1

print(f"\n🎯 PT 763 has {unknown_count} unknown words")

# Find intersecting FR subtitles
from subtitle_fusion import SubtitleFusionEngine
engine = SubtitleFusionEngine()

fr_matches = [
    s for s in fr_subs
    if engine._has_intersection(pt_763.start, pt_763.end, s.start, s.end)
]

print(f"\nIntersecting FR subtitles: {[s.index for s in fr_matches]}")
for fr in fr_matches:
    print(f"   FR {fr.index}: {fr.start} → {fr.end}")
    print(f"   Text: {fr.text}")

# Find what PT subtitles would be marked as "processed"
if fr_matches:
    combined_start = fr_matches[0].start
    combined_end = fr_matches[-1].end
    print(f"\nCombined FR range: {combined_start} → {combined_end}")

    overlapping_pt = [
        s for s in pt_subs
        if engine._has_intersection(combined_start, combined_end, s.start, s.end)
    ]
    print(f"PT subtitles that would be marked as processed: {[s.index for s in overlapping_pt]}")
