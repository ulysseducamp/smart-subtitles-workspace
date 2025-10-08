#!/usr/bin/env python3
"""Check if PT 764 is inline translation case"""

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

# Find PT 764
pt_764 = next((s for s in pt_subs if s.index == "764"), None)
print(f"PT 764: {pt_764.text}")

# Analyze words
text_no_html = re.sub(r'<[^>]*>', '', pt_764.text)
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

print(f"\n🎯 Total unknown words: {unknown_count}")
if unknown_count == 1:
    print("→ This is an INLINE TRANSLATION case (1 unknown word)")
elif unknown_count >= 2:
    print("→ This should be REPLACED by French subtitle (2+ unknown words)")
else:
    print("→ This should be KEPT in Portuguese (0 unknown words)")
