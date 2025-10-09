"""
Test to understand PT 632/633 double subtitle display issue
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "smartsub-api" / "src"))

from srt_parser import parse_srt
from subtitle_fusion import SubtitleFusionEngine
from frequency_loader import FrequencyLoader

# Initialize frequency loader
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

print("🔍 Analyzing PT 632/633 double subtitle issue\n")

# Find PT 632 and 633
pt_632 = next((s for s in pt_subs if s.index == "632"), None)
pt_633 = next((s for s in pt_subs if s.index == "633"), None)

# Find FR 629 and 630
fr_629 = next((s for s in fr_subs if s.index == "629"), None)
fr_630 = next((s for s in fr_subs if s.index == "630"), None)

print("📌 PT 632:")
print(f"   {pt_632.start} → {pt_632.end}")
print(f"   Text: {pt_632.text}")
print()

print("📌 PT 633:")
print(f"   {pt_633.start} → {pt_633.end}")
print(f"   Text: {pt_633.text}")
print()

print("📌 FR 629:")
print(f"   {fr_629.start} → {fr_629.end}")
print(f"   Text: {fr_629.text}")
print()

print("📌 FR 630:")
print(f"   {fr_630.start} → {fr_630.end}")
print(f"   Text: {fr_630.text}")
print()

# Get top 800 PT words
known_words = freq_loader.get_top_n_words('PT', 800)
print(f"📚 Known words (PT, top 800): {len(known_words)} words\n")

# Test fusion with top 800
engine = SubtitleFusionEngine()

import asyncio

async def test_fusion():
    result = await engine.fuse_subtitles(
        target_subs=pt_subs,
        native_subs=fr_subs,
        known_words=known_words,
        lang='PT',
        enable_inline_translation=False,  # Disable to see pure fusion logic
        deepl_api=None,
        openai_translator=None,
        native_lang='FR',
        top_n=800
    )
    return result

result = asyncio.run(test_fusion())

print("\n📊 Fusion Results:")
print(f"   Total output subtitles: {len(result['hybrid'])}")

# Check if PT 632, PT 633, FR 629, FR 630 are in output
output_indices = [s.index for s in result['hybrid']]

print("\n🔎 Checking output for PT 632, 633 and FR 629, 630:")
if "632" in output_indices:
    pt_632_out = next((s for s in result['hybrid'] if s.index == "632"), None)
    print(f"   ✅ PT 632 FOUND in output")
    print(f"      {pt_632_out.start} → {pt_632_out.end}")
    print(f"      Text: {pt_632_out.text}")
else:
    print(f"   ❌ PT 632 NOT in output")

if "633" in output_indices:
    pt_633_out = next((s for s in result['hybrid'] if s.index == "633"), None)
    print(f"   ✅ PT 633 FOUND in output")
    print(f"      {pt_633_out.start} → {pt_633_out.end}")
    print(f"      Text: {pt_633_out.text}")
else:
    print(f"   ❌ PT 633 NOT in output")

if "629" in output_indices:
    fr_629_out = next((s for s in result['hybrid'] if s.index == "629"), None)
    print(f"   ✅ FR 629 FOUND in output")
    print(f"      {fr_629_out.start} → {fr_629_out.end}")
    print(f"      Text: {fr_629_out.text}")
else:
    print(f"   ❌ FR 629 NOT in output")

if "630" in output_indices:
    fr_630_out = next((s for s in result['hybrid'] if s.index == "630"), None)
    print(f"   ✅ FR 630 FOUND in output")
    print(f"      {fr_630_out.start} → {fr_630_out.end}")
    print(f"      Text: {fr_630_out.text}")
else:
    print(f"   ❌ FR 630 NOT in output")

# Check for temporal overlap
print("\n⏱️  Temporal overlap analysis:")
print(f"   PT 632: {pt_632.start} → {pt_632.end}")
print(f"   FR 629: {fr_629.start} → {fr_629.end}")
print(f"   Overlap period: ~23.71s to 24.42s (both visible)")
