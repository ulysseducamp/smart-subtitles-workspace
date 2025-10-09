"""
Check how many unknown words in PT 632
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from frequency_loader import FrequencyLoader

# Initialize
freq_lists_dir = Path(__file__).parent / "smartsub-api" / "src" / "frequency_lists"
freq_loader = FrequencyLoader(frequency_lists_dir=freq_lists_dir)

# Get top 800 PT words
known_words_800 = freq_loader.get_top_n_words('PT', 800)
known_words_2000 = freq_loader.get_top_n_words('PT', 2000)

# PT 632 text
pt_632_text = "[Berlim] Enquanto isso, nos arredores de Paris,"

# Clean and split
import re
text_clean = re.sub(r'<[^>]*>', '', pt_632_text)  # Remove HTML
text_clean = re.sub(r'\[.*?\]', '', text_clean)   # Remove [Berlim]
words = re.findall(r'\b\w+\b', text_clean.lower())

print("🔍 PT 632 word analysis\n")
print(f"Text: {pt_632_text}")
print(f"Words: {words}\n")

print("📊 With top 800 words:")
unknown_800 = [w for w in words if w not in known_words_800]
print(f"   Known: {len(words) - len(unknown_800)}")
print(f"   Unknown: {len(unknown_800)}")
if unknown_800:
    print(f"   Unknown words: {unknown_800}")
print()

print("📊 With top 2000 words:")
unknown_2000 = [w for w in words if w not in known_words_2000]
print(f"   Known: {len(words) - len(unknown_2000)}")
print(f"   Unknown: {len(unknown_2000)}")
if unknown_2000:
    print(f"   Unknown words: {unknown_2000}")
print()

# Check individual word ranks
print("📋 Individual word ranks:")
for word in words:
    rank = freq_loader.get_word_rank(word, 'PT')
    if rank:
        print(f"   '{word}': rank {rank}")
    else:
        print(f"   '{word}': NOT in frequency list")
