#!/usr/bin/env python3
"""
Test to investigate why "et" (rank 6) is considered unknown
"""
import sys
sys.path.insert(0, 'src')

from subtitle_fusion import create_alignment_mapping, SubtitleFusionEngine
from frequency_loader import initialize_frequency_loader, get_frequency_loader

# Initialize
initialize_frequency_loader()
freq_loader = get_frequency_loader()
known_words = freq_loader.get_top_n_words('fr', top_n=1000)

# Test subtitle (exact from Lupin S01E01 subtitle #72)
subtitle_text = 'Il a appartenu à Marie-Antoinette et il vaut des millions.'

print('=== Test du sous-titre exact (Lupin S01E01 #72) ===')
print(f'Texte: {subtitle_text}')
print()

# Create token mappings
mappings = create_alignment_mapping(subtitle_text, 'fr')

print('Token Mappings:')
for i, m in enumerate(mappings):
    filtered_str = '❌ FILTRÉ' if m.is_filtered else '✅'
    if m.lemmatized_word:
        known_str = '✅ CONNU' if m.lemmatized_word.lower() in known_words else '❌ INCONNU'
        rank = freq_loader.get_word_rank(m.lemmatized_word, 'fr', top_n=1000)
        rank_str = f'(rang {rank})' if rank else '(hors top 1000)'
    else:
        known_str = ''
        rank_str = ''
    print(f'  [{i}] {filtered_str} {known_str} | orig="{m.original_word}" → lemma="{m.lemmatized_word}" {rank_str}')
print()

# Check active mappings (non-filtered)
active_mappings = [m for m in mappings if not m.is_filtered]
print(f'Active mappings (non-filtered): {len(active_mappings)}/{len(mappings)}')
print()

# Find 'et' in active mappings
et_mappings = [m for m in active_mappings if m.original_word.lower() == 'et' or m.lemmatized_word == 'et']
print(f'Mappings pour "et": {len(et_mappings)}')
for m in et_mappings:
    in_known = m.lemmatized_word in known_words
    print(f'  - orig="{m.original_word}", lemma="{m.lemmatized_word}", dans known_words? {in_known}')
print()

# Simulate the is_word_known check
engine = SubtitleFusionEngine()
if et_mappings:
    for m in et_mappings:
        is_known = engine.is_word_known(m.lemmatized_word, known_words, 'fr', original_word=m.original_word, subtitle_index='72')
        print(f'  engine.is_word_known("{m.lemmatized_word}", ...) = {is_known}')
