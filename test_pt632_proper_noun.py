"""
Test if 'Paris' is detected as proper noun in PT 632
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import FrequencyLoader
import re

# Initialize
freq_lists_dir = Path(__file__).parent / "smartsub-api" / "src" / "frequency_lists"
freq_loader = FrequencyLoader(frequency_lists_dir=freq_lists_dir)

# Get top 800 PT words
known_words = freq_loader.get_top_n_words('PT', 800)

# PT 632 text
pt_632_text = "[Berlim] <i>Enquanto isso,</i>\n<i>nos arredores de Paris,</i>"

# Create engine
engine = SubtitleFusionEngine()

# Clean text
text_clean = re.sub(r'<[^>]*>', '', pt_632_text)
text_clean = re.sub(r'\[.*?\]', '', text_clean)

# Extract words
words_with_case = re.findall(r'\b\w+\b', text_clean)  # Preserve case

print("🔍 PT 632 proper noun detection\n")
print(f"Text: {pt_632_text}")
print(f"Words (with case): {words_with_case}\n")

# Test each word
for word in words_with_case:
    is_proper = engine.is_proper_noun(word, pt_632_text, known_words)
    word_lower = word.lower()
    is_known = word_lower in known_words

    print(f"📝 '{word}':")
    print(f"   Capitalized: {word[0].isupper() if word else False}")
    print(f"   Is proper noun: {is_proper}")
    print(f"   Is known (lowercase): {is_known}")

    if is_proper:
        print(f"   → IGNORED (proper noun)")
    elif is_known:
        print(f"   → KNOWN")
    else:
        print(f"   → UNKNOWN")
    print()

# Count unknown words (excluding proper nouns)
unknown_count = 0
unknown_words = []
for word in words_with_case:
    is_proper = engine.is_proper_noun(word, pt_632_text, known_words)
    word_lower = word.lower()
    is_known = word_lower in known_words

    if not is_proper and not is_known:
        unknown_count += 1
        unknown_words.append(word_lower)

print(f"📊 Final decision:")
print(f"   Total words: {len(words_with_case)}")
print(f"   Unknown words (excluding proper nouns): {unknown_count}")
print(f"   Unknown words list: {unknown_words}")

if unknown_count == 0:
    print(f"\n✅ Decision: KEEP in PT (all words known/proper nouns)")
elif unknown_count == 1:
    print(f"\n✅ Decision: INLINE TRANSLATION for '{unknown_words[0]}'")
else:
    print(f"\n✅ Decision: REPLACE with FR (2+ unknown words)")
