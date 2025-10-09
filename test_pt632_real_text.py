"""
Test PT 632 with EXACT text from SRT file
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from srt_parser import parse_srt

# Load PT SRT
with open("Berlin.S01E08.Un éléphant menacé d'extinction.pt-BR.srt", 'r', encoding='utf-8') as f:
    pt_content = f.read()

pt_subs = parse_srt(pt_content)

# Find PT 632
pt_632 = next((s for s in pt_subs if s.index == "632"), None)

if pt_632:
    print("🔍 PT 632 EXACT TEXT from SRT:")
    print(f"   Index: {pt_632.index}")
    print(f"   Time: {pt_632.start} → {pt_632.end}")
    print(f"   Text: {repr(pt_632.text)}")
    print()

    # Now test with the fusion engine
    from frequency_loader import FrequencyLoader
    from subtitle_fusion import SubtitleFusionEngine
    import re

    freq_lists_dir = Path(__file__).parent / "smartsub-api" / "src" / "frequency_lists"
    freq_loader = FrequencyLoader(frequency_lists_dir=freq_lists_dir)
    engine = SubtitleFusionEngine()

    known_words = freq_loader.get_top_n_words('PT', 800)

    # Clean text
    text_clean = re.sub(r'<[^>]*>', '', pt_632.text)
    text_clean = re.sub(r'\[.*?\]', '', text_clean)

    # Extract words (preserve case)
    words_with_case = re.findall(r'\b\w+\b', text_clean)

    print("Words (with case):", words_with_case)
    print()

    # Analyze each word
    unknown_count = 0
    unknown_words = []

    for word in words_with_case:
        is_proper = engine.is_proper_noun(word, pt_632.text, known_words)
        word_lower = word.lower()
        is_known = word_lower in known_words

        rank = freq_loader.get_word_rank(word_lower, 'PT')
        rank_str = f"rank {rank}" if rank else "NOT in list"

        if is_proper:
            status = "PROPER NOUN"
        elif is_known:
            status = "KNOWN"
        else:
            status = "UNKNOWN"
            unknown_count += 1
            unknown_words.append(word_lower)

        print(f"  '{word}': {status} ({rank_str})")

    print(f"\n📊 Final count:")
    print(f"  Total words: {len(words_with_case)}")
    print(f"  Unknown (excluding proper nouns): {unknown_count}")
    if unknown_words:
        print(f"  Unknown words: {unknown_words}")

    print(f"\n🎯 DECISION:")
    if unknown_count == 0:
        print(f"  → KEEP in PT (all words known/proper nouns)")
    elif unknown_count == 1:
        print(f"  → INLINE TRANSLATION for '{unknown_words[0]}'")
    else:
        print(f"  → REPLACE with FR ({unknown_count} unknown words)")
else:
    print("❌ PT 632 not found")
