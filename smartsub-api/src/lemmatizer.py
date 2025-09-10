"""
Lemmatization functions - Python implementation
Migrated from TypeScript logic.ts subprocess calls
"""

from typing import List
import simplemma

def lemmatize_single_line(line: str, lang: str) -> List[str]:
    """
    Lemmatize a single line of text
    Migrated from TypeScript lemmatizeSingleLine function
    Direct Python implementation using simplemma (no subprocess)
    """
    # No language mapping needed - use language code directly
    
    words = line.split()
    lemmatized_words = []
    
    for word in words:
        try:
            # Use simplemma to lemmatize each word
            lemmatized = simplemma.lemmatize(word, lang=lang)
            lemmatized_words.append(lemmatized)
        except Exception as e:
            # If lemmatization fails, use the original word
            print(f"Warning: Lemmatization failed for word '{word}' with language '{lang}': {e}")
            lemmatized_words.append(word)
    
    return lemmatized_words

def batch_lemmatize(lines: List[str], lang: str) -> List[List[str]]:
    """
    Batch lemmatization for efficiency
    Migrated from TypeScript batchLemmatize function
    """
    results = []
    for line in lines:
        lemmatized_line = lemmatize_single_line(line, lang)
        results.append(lemmatized_line)
    return results
