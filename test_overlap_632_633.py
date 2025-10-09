"""
Test overlap durations pour vérifier la solution proposée
"""

def srt_to_ms(srt_time):
    """Convert SRT time to milliseconds"""
    parts = srt_time.replace(',', ':').split(':')
    hours, minutes, seconds, ms = map(int, parts)
    return hours * 3600000 + minutes * 60000 + seconds * 1000 + ms

def calculate_intersection(sub1_start, sub1_end, sub2_start, sub2_end):
    """Calculate intersection duration in seconds"""
    start1_ms = srt_to_ms(sub1_start)
    end1_ms = srt_to_ms(sub1_end)
    start2_ms = srt_to_ms(sub2_start)
    end2_ms = srt_to_ms(sub2_end)

    intersection_start = max(start1_ms, start2_ms)
    intersection_end = min(end1_ms, end2_ms)

    if intersection_end <= intersection_start:
        return 0.0

    return (intersection_end - intersection_start) / 1000.0

# Subtitles timestamps
pt_632 = {"start": "00:43:21,291", "end": "00:43:23,708"}
pt_633 = {"start": "00:43:23,791", "end": "00:43:27,083"}
fr_629 = {"start": "00:43:21,750", "end": "00:43:24,416"}
fr_630 = {"start": "00:43:24,500", "end": "00:43:27,458"}

print("🔍 ANALYSE DES OVERLAPS\n")
print("="*60)

# FR 629 avec PT 632 et PT 633
overlap_629_632 = calculate_intersection(fr_629["start"], fr_629["end"],
                                         pt_632["start"], pt_632["end"])
overlap_629_633 = calculate_intersection(fr_629["start"], fr_629["end"],
                                         pt_633["start"], pt_633["end"])

print("\n📌 FR 629 :")
print(f"   Overlap avec PT 632 (précédent) : {overlap_629_632:.3f}s")
print(f"   Overlap avec PT 633 (current)    : {overlap_629_633:.3f}s")

if overlap_629_632 > overlap_629_633:
    print(f"   → FR 629 APPARTIENT à PT 632 ✅")
    print(f"   → FR 629 NE DOIT PAS remplacer PT 633 ❌")
else:
    print(f"   → FR 629 APPARTIENT à PT 633 ✅")

# FR 630 avec PT 632, PT 633, et hypothétique PT 634
overlap_630_632 = calculate_intersection(fr_630["start"], fr_630["end"],
                                         pt_632["start"], pt_632["end"])
overlap_630_633 = calculate_intersection(fr_630["start"], fr_630["end"],
                                         pt_633["start"], pt_633["end"])

print("\n📌 FR 630 :")
print(f"   Overlap avec PT 632 (avant)   : {overlap_630_632:.3f}s")
print(f"   Overlap avec PT 633 (current) : {overlap_630_633:.3f}s")

if overlap_630_632 > overlap_630_633:
    print(f"   → FR 630 APPARTIENT à PT 632 ✅")
else:
    print(f"   → FR 630 APPARTIENT à PT 633 ✅")

print("\n" + "="*60)
print("🎯 CONCLUSION AVEC TA SOLUTION :\n")
print("PT 632 devrait être remplacé par : FR 629")
print("PT 633 devrait être remplacé par : FR 630")
print("\n→ Pas de 'gros bloc' FR 629+630")
print("→ Pas d'overlap entre PT 632 et le remplacement de PT 633")
print("→ PAS DE DOUBLE AFFICHAGE ✅")
