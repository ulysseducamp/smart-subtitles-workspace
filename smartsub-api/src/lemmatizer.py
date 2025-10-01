"""
Lemmatization functions - Python implementation
Migrated from TypeScript logic.ts subprocess calls
"""

from typing import List, Optional
import simplemma

def lemmatize_single_line(line: str, lang: str) -> List[str]:
    """
    Lemmatize a single line of text
    Migrated from TypeScript lemmatizeSingleLine function
    Direct Python implementation using simplemma (no subprocess)
    """
    
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

def should_lemmatize_word(word: str, lang: str, frequency_threshold: int = 200) -> bool:
    """
    Determine if a word should be lemmatized based on frequency ranking.
    Words in the top N most frequent words are NOT lemmatized (they're usually already canonical).

    Args:
        word: The word to check
        lang: Language code (e.g., 'pt', 'en', 'fr')
        frequency_threshold: Top N words that should NOT be lemmatized (default: 200)

    Returns:
        True if word should be lemmatized, False if it should remain unchanged
    """
    try:
        from frequency_loader import initialize_frequency_loader, get_frequency_loader

        # Initialize if not already done
        try:
            frequency_loader = get_frequency_loader()
        except RuntimeError:
            initialize_frequency_loader()
            frequency_loader = get_frequency_loader()

        word_rank = frequency_loader.get_word_rank(word.lower(), lang, top_n=frequency_threshold)

        # If word is not found in top N or rank is > threshold, lemmatize it
        # If word is in top N (rank <= threshold), don't lemmatize it
        return word_rank is None or word_rank > frequency_threshold

    except Exception:
        # If frequency lookup fails, default to lemmatizing
        return True

def smart_lemmatize_line(line: str, lang: str, frequency_threshold: int = 200) -> List[str]:
    """
    Smart lemmatization that preserves high-frequency words in their original form.

    Args:
        line: Text line to lemmatize
        lang: Language code
        frequency_threshold: Top N words to preserve (default: 200)

    Returns:
        List of lemmatized words (or original words for high-frequency terms)
    """
    words = line.split()
    result = []

    for word in words:
        if should_lemmatize_word(word, lang, frequency_threshold):
            # Lemmatize normally for less frequent words
            try:
                lemmatized = simplemma.lemmatize(word, lang=lang)
                result.append(lemmatized)
            except Exception as e:
                print(f"Warning: Lemmatization failed for word '{word}' with language '{lang}': {e}")
                result.append(word)
        else:
            # Keep original word for high-frequency terms (no lemmatization)
            result.append(word)

    return result

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
