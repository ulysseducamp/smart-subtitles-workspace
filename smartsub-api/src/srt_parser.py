"""
SRT parsing and generation functions
Migrated from TypeScript logic.ts
"""

from typing import List
from dataclasses import dataclass
import re

@dataclass
class Subtitle:
    """Represents a single subtitle entry"""
    index: str
    start: str
    end: str
    text: str

def parse_srt(srt_content: str) -> List[Subtitle]:
    """
    Parse SRT content into list of Subtitle objects
    Migrated from TypeScript parseSRT function
    """
    import re
    
    # Split by double newlines (subtitle blocks)
    blocks = re.split(r'\r?\n\r?\n', srt_content.strip())
    subtitles = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        lines = block.split('\n')
        if len(lines) < 3:
            continue
            
        index = lines[0].strip()
        time_line = lines[1].strip()
        
        # Parse time line (format: "00:00:06,000 --> 00:00:08,800")
        if ' --> ' not in time_line:
            continue
            
        start, end = time_line.split(' --> ', 1)
        text = '\n'.join(lines[2:])
        
        # Only add if all required fields are present
        if index and start and end:
            subtitles.append(Subtitle(
                index=index,
                start=start.strip(),
                end=end.strip(),
                text=text
            ))
    
    return subtitles

def generate_srt(subtitles: List[Subtitle]) -> str:
    """
    Generate SRT content from list of Subtitle objects
    Migrated from TypeScript generateSRT function
    """
    result = []
    for subtitle in subtitles:
        result.append(f"{subtitle.index}\n{subtitle.start} --> {subtitle.end}\n{subtitle.text}\n")
    return '\n'.join(result)

def normalize_words(text: str) -> List[str]:
    """
    Normalize text by removing ALL punctuation (including apostrophes, hyphens, etc.)
    and converting to lowercase.

    Simplified version: treats all punctuation uniformly - no special handling needed
    for apostrophes or hyphens as they're all replaced with spaces.

    Examples:
        "l'école"                 -> ["école"]
        "Marie-Antoinette"        -> ["marie", "antoinette"]
        "C'est Marie-Antoinette!" -> ["est", "marie", "antoinette"]
        "a-t-il"                  -> ["il"]  (a, t filtered as single letters)
    """
    import re

    # Remove HTML tags first
    text = re.sub(r'<[^>]*>', '', text)

    # Replace ALL punctuation with spaces (apostrophes, hyphens, commas, periods, etc.)
    # Use \w to support Unicode characters (accents, etc.)
    text = re.sub(r'[^\w\s]', ' ', text)

    # Convert to lowercase and split by whitespace
    words = text.lower().split()

    # Filter out single letters and empty strings
    return [word for word in words if len(word) > 1]
