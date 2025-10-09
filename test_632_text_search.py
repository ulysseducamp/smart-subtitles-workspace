"""
Test to find PT 632/633 by TEXT in fusion output
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from srt_parser import parse_srt
from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import FrequencyLoader
import asyncio

# Initialize
freq_lists_dir = Path(__file__).parent / "smartsub-api" / "src" / "frequency_lists"
freq_loader = FrequencyLoader(frequency_lists_dir=freq_lists_dir)

# Load SRT files
pt_file = "Berlin.S01E08.Un éléphant menacé d'extinction.pt-BR.srt"
fr_file = "Berlin.S01E08.Un éléphant menacé d'extinction.fr.srt"

with open(pt_file, 'r', encoding='utf-8') as f:
    pt_content = f.read()
with open(fr_file, 'r', encoding='utf-8') as f:
    fr_content = f.read()

pt_subs = parse_srt(pt_content)
fr_subs = parse_srt(fr_content)

# Get top 800 PT words
known_words = freq_loader.get_top_n_words('PT', 800)

# Test fusion
engine = SubtitleFusionEngine()

async def test_fusion():
    result = await engine.fuse_subtitles(
        target_subs=pt_subs,
        native_subs=fr_subs,
        known_words=known_words,
        lang='PT',
        enable_inline_translation=False,
        deepl_api=None,
        openai_translator=None,
        native_lang='FR',
        top_n=800
    )
    return result

result = asyncio.run(test_fusion())

print("🔍 Searching for PT 632/633 by TEXT in fusion output\n")

# Search by text fragments
search_texts = {
    "PT_632": "Enquanto isso",
    "PT_633": "instalavam um quarto",
    "FR_629": "Pendant ce temps",
    "FR_630": "périmètre de sécurité"
}

for label, search_text in search_texts.items():
    found = [s for s in result['hybrid'] if search_text in s.text]
    if found:
        for sub in found:
            print(f"✅ {label} FOUND (re-indexed as {sub.index}):")
            print(f"   {sub.start} → {sub.end}")
            print(f"   Text: {sub.text[:100]}...")
            print()
    else:
        print(f"❌ {label} NOT found")
        print()

# Check for temporal overlaps in output
print("\n⏱️  Checking for temporal overlaps in final output:")
from datetime import datetime, timedelta

def srt_to_ms(srt_time):
    """Convert SRT time to milliseconds"""
    parts = srt_time.replace(',', ':').split(':')
    hours, minutes, seconds, ms = map(int, parts)
    return hours * 3600000 + minutes * 60000 + seconds * 1000 + ms

# Find overlapping subtitles
overlaps = []
for i, sub1 in enumerate(result['hybrid']):
    for sub2 in result['hybrid'][i+1:]:
        start1_ms = srt_to_ms(sub1.start)
        end1_ms = srt_to_ms(sub1.end)
        start2_ms = srt_to_ms(sub2.start)
        end2_ms = srt_to_ms(sub2.end)

        # Check overlap
        if start2_ms < end1_ms:
            overlap_duration = (end1_ms - start2_ms) / 1000.0
            overlaps.append({
                'sub1': sub1,
                'sub2': sub2,
                'overlap_duration': overlap_duration
            })
            # Only check immediate next subtitle
            break

# Show first 10 overlaps
print(f"Found {len(overlaps)} temporal overlaps")
print("\nFirst 10 overlaps:")
for i, overlap in enumerate(overlaps[:10]):
    print(f"\n{i+1}. Overlap duration: {overlap['overlap_duration']:.2f}s")
    print(f"   Sub {overlap['sub1'].index}: {overlap['sub1'].start} → {overlap['sub1'].end}")
    print(f"      {overlap['sub1'].text[:60]}...")
    print(f"   Sub {overlap['sub2'].index}: {overlap['sub2'].start} → {overlap['sub2'].end}")
    print(f"      {overlap['sub2'].text[:60]}...")
