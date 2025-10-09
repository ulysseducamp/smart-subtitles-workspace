"""
Analyze PT 234 and 235 for unknown words
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from frequency_loader import FrequencyLoader
from subtitle_fusion import SubtitleFusionEngine
import re

# Initialize
freq_lists_dir = Path(__file__).parent / "smartsub-api" / "src" / "frequency_lists"
freq_loader = FrequencyLoader(frequency_lists_dir=freq_lists_dir)
engine = SubtitleFusionEngine()

# Get top 800 PT words
known_words = freq_loader.get_top_n_words('PT', 800)

# PT 234 and 235 texts
pt_234_text = "[homem] <i>Delegada, temos os possíveis</i>\n<i>suspeitos. Um homem e uma mulher.</i>"
pt_235_text = "<i>Espanhóis, 30 anos</i>\n<i>e roubaram um carro patrulha no hospital.</i>"

def analyze_subtitle(text, index, known_words, engine):
    # Clean text
    text_clean = re.sub(r'<[^>]*>', '', text)
    text_clean = re.sub(r'\[.*?\]', '', text_clean)

    # Extract words (preserve case for proper noun detection)
    words_with_case = re.findall(r'\b\w+\b', text_clean)

    print(f"\n{'='*60}")
    print(f"PT {index}: {text[:80]}...")
    print(f"{'='*60}")
    print(f"Words: {words_with_case}\n")

    # Analyze each word
    unknown_count = 0
    unknown_words = []
    proper_nouns = []
    known_count = 0

    for word in words_with_case:
        is_proper = engine.is_proper_noun(word, text, known_words)
        word_lower = word.lower()
        is_known = word_lower in known_words

        if is_proper:
            proper_nouns.append(word)
            status = "PROPER NOUN (ignored)"
        elif is_known:
            known_count += 1
            status = "KNOWN"
        else:
            unknown_count += 1
            unknown_words.append(word_lower)
            status = "UNKNOWN"

        rank = freq_loader.get_word_rank(word_lower, 'PT')
        rank_str = f"rank {rank}" if rank else "NOT in list"

        print(f"  '{word}': {status} ({rank_str})")

    print(f"\n📊 Summary:")
    print(f"  Total words: {len(words_with_case)}")
    print(f"  Known: {known_count}")
    print(f"  Proper nouns: {len(proper_nouns)}")
    print(f"  Unknown (excluding proper nouns): {unknown_count}")
    if unknown_words:
        print(f"  Unknown words: {unknown_words}")

    # Decision
    print(f"\n🎯 DECISION:")
    if unknown_count == 0:
        print(f"  → KEEP in PT (all words known/proper nouns)")
    elif unknown_count == 1:
        print(f"  → INLINE TRANSLATION for '{unknown_words[0]}'")
    else:
        print(f"  → REPLACE with FR ({unknown_count} unknown words)")

    return unknown_count

# Analyze both
unknown_234 = analyze_subtitle(pt_234_text, "234", known_words, engine)
unknown_235 = analyze_subtitle(pt_235_text, "235", known_words, engine)

print(f"\n{'='*60}")
print("OVERALL ANALYSIS")
print(f"{'='*60}")
print(f"PT 234: {unknown_234} unknown words")
print(f"PT 235: {unknown_235} unknown words")
