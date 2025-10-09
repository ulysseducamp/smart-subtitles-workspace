"""
Check PT 633 word analysis
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from frequency_loader import FrequencyLoader
import re

# Initialize
freq_lists_dir = Path(__file__).parent / "smartsub-api" / "src" / "frequency_lists"
freq_loader = FrequencyLoader(frequency_lists_dir=freq_lists_dir)

# Get top 800 PT words
known_words = freq_loader.get_top_n_words('PT', 800)

# PT 633 text
pt_633_text = "<i>instalavam um quarto centro de comando</i>\n<i>a 60km da capital.</i>"

# Clean and split
text_clean = re.sub(r'<[^>]*>', '', pt_633_text)  # Remove HTML
text_clean = re.sub(r'\[.*?\]', '', text_clean)   # Remove brackets
words = re.findall(r'\b\w+\b', text_clean.lower())

print("🔍 PT 633 word analysis\n")
print(f"Text: {pt_633_text}")
print(f"Words: {words}\n")

unknown = [w for w in words if w not in known_words]
print(f"📊 With top 800 words:")
print(f"   Total words: {len(words)}")
print(f"   Known: {len(words) - len(unknown)}")
print(f"   Unknown: {len(unknown)}")
if unknown:
    print(f"   Unknown words: {unknown}")
print()

# Check individual word ranks
print("📋 Individual word ranks:")
for word in words:
    rank = freq_loader.get_word_rank(word, 'PT')
    if rank:
        print(f"   '{word}': rank {rank}")
    else:
        print(f"   '{word}': NOT in frequency list")
