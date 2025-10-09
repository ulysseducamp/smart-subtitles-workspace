"""
Test the fix for PT 632/633 double subtitle display
Verify that FR 629 is excluded from PT 633 replacement (better match with PT 632)
"""
import sys
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from srt_parser import parse_srt
from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import FrequencyLoader

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

print("🔍 Testing fix for PT 632/633 double subtitle display\n")
print("="*70)

# Show original timestamps
pt_632 = next((s for s in pt_subs if s.index == "632"), None)
pt_633 = next((s for s in pt_subs if s.index == "633"), None)
fr_629 = next((s for s in fr_subs if s.index == "629"), None)
fr_630 = next((s for s in fr_subs if s.index == "630"), None)

print("\n📌 Original subtitles:")
print(f"   PT 632: {pt_632.start} → {pt_632.end}")
print(f"           {pt_632.text[:60]}...")
print(f"   PT 633: {pt_633.start} → {pt_633.end}")
print(f"           {pt_633.text[:60]}...")
print(f"   FR 629: {fr_629.start} → {fr_629.end}")
print(f"           {fr_629.text[:60]}...")
print(f"   FR 630: {fr_630.start} → {fr_630.end}")
print(f"           {fr_630.text[:60]}...")

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

print("\n" + "="*70)
print("🔄 Running fusion with fix...")
print("="*70)

result = asyncio.run(test_fusion())

print("\n" + "="*70)
print("📊 RESULTS:")
print("="*70)

# Search for PT 632 and PT 633 in output by timestamp
output_632_633 = [
    s for s in result['hybrid']
    if (s.start == pt_632.start or s.start == pt_633.start)
]

print(f"\nSubtitles at PT 632/633 timestamps:")
for sub in output_632_633:
    print(f"\n   Index: {sub.index}")
    print(f"   Time: {sub.start} → {sub.end}")
    print(f"   Text: {sub.text[:80]}...")

# Verify expectations
print("\n" + "="*70)
print("✅ VERIFICATION:")
print("="*70)

# Check if we have exactly 2 subtitles (one for PT 632 area, one for PT 633)
if len(output_632_633) == 2:
    print("✅ Correct number of subtitles (2)")
else:
    print(f"❌ Wrong number of subtitles: {len(output_632_633)} (expected 2)")

# Check timestamps don't overlap
if len(output_632_633) >= 2:
    sub1 = output_632_633[0]
    sub2 = output_632_633[1]

    # Parse timestamps to compare
    def srt_to_ms(time):
        parts = time.replace(',', ':').split(':')
        h, m, s, ms = map(int, parts)
        return h * 3600000 + m * 60000 + s * 1000 + ms

    end1 = srt_to_ms(sub1.end)
    start2 = srt_to_ms(sub2.start)

    if start2 > end1:
        print(f"✅ No temporal overlap between subtitles")
    else:
        overlap_ms = end1 - start2
        print(f"⚠️  Temporal overlap: {overlap_ms}ms")

print("\n" + "="*70)
print("Expected behavior:")
print("  - PT 632 area: Should be kept in PT (1 unknown word) or replaced by FR 629 only")
print("  - PT 633 area: Should be replaced by FR 630 only (NOT FR 629+630)")
print("  - No temporal overlap → No double subtitle display")
print("="*70)
