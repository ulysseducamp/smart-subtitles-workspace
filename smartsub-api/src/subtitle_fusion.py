"""
Main subtitle fusion engine - Python implementation
Migrated from TypeScript logic.ts
"""

from typing import List, Set, Dict, Any, Optional
from dataclasses import dataclass
import re
import time
from srt_parser import Subtitle

class SubtitleFusionEngine:
    """
    Main engine for subtitle fusion algorithm
    Migrated from TypeScript logic.ts
    """
    
    def __init__(self):
        # English contractions mapping - migrated from logic.ts
        self.english_contractions = {
            # Personal pronouns + be/have/will/would
            "you're": ["you", "are"],
            "you'll": ["you", "will"], 
            "you've": ["you", "have"],
            "you'd": ["you", "would"],
            "i'm": ["i", "am"],
            "i'll": ["i", "will"],
            "i've": ["i", "have"],
            "i'd": ["i", "would"],
            "we're": ["we", "are"],
            "we'll": ["we", "will"],
            "we've": ["we", "have"],
            "we'd": ["we", "would"],
            "they're": ["they", "are"],
            "they'll": ["they", "will"],
            "they've": ["they", "have"],
            "they'd": ["they", "would"],
            "he's": ["he", "is"],
            "he'll": ["he", "will"],
            "he'd": ["he", "would"],
            "she's": ["she", "is"],
            "she'll": ["she", "will"],
            "she'd": ["she", "would"],
            "it's": ["it", "is"],
            "it'll": ["it", "will"],
            "it'd": ["it", "would"],
            
            # Common verbs with not
            "don't": ["do", "not"],
            "doesn't": ["does", "not"],
            "didn't": ["did", "not"],
            "can't": ["can", "not"],
            "couldn't": ["could", "not"],
            "won't": ["will", "not"],
            "wouldn't": ["would", "not"],
            "shouldn't": ["should", "not"],
            "mustn't": ["must", "not"],
            "haven't": ["have", "not"],
            "hasn't": ["has", "not"],
            "hadn't": ["had", "not"],
            "isn't": ["is", "not"],
            "aren't": ["are", "not"],
            "wasn't": ["was", "not"],
            "weren't": ["were", "not"],
            
            # Demonstratives
            "that's": ["that", "is"],
            "that'll": ["that", "will"],
            "that'd": ["that", "would"],
            "there's": ["there", "is"],
            "there'll": ["there", "will"],
            "there'd": ["there", "would"],
            "here's": ["here", "is"],
            "here'll": ["here", "will"],
            "here'd": ["here", "would"],
            
            # Question words
            "who's": ["who", "is"],
            "who'll": ["who", "will"],
            "who'd": ["who", "would"],
            "what's": ["what", "is"],
            "what'll": ["what", "will"],
            "what'd": ["what", "would"],
            "where's": ["where", "is"],
            "where'll": ["where", "will"],
            "where'd": ["where", "would"],
            "when's": ["when", "is"],
            "when'll": ["when", "will"],
            "when'd": ["when", "would"],
            "why's": ["why", "is"],
            "why'll": ["why", "will"],
            "why'd": ["why", "would"],
            "how's": ["how", "is"],
            "how'll": ["how", "will"],
            "how'd": ["how", "would"],
            
            # Other common contractions
            "let's": ["let", "us"],
            "ma'am": ["madam"],
            "o'clock": ["of", "the", "clock"],
            "y'all": ["you", "all"],
            "gonna": ["going", "to"],
            "wanna": ["want", "to"],
            "gotta": ["got", "to"],
            "lemme": ["let", "me"],
            "gimme": ["give", "me"],
            "outta": ["out", "of"],
            "kinda": ["kind", "of"],
            "sorta": ["sort", "of"],
            "lotta": ["lot", "of"],
            "lotsa": ["lots", "of"],
            "cuppa": ["cup", "of"],
            "ain't": ["am", "not"],
        }
    
    def is_proper_noun(self, word: str, sentence: str, frequency_list: Set[str]) -> bool:
        """
        Determines if a word is a proper noun according to the following rules:
        1. If the word is capitalized and NOT at the beginning of the sentence, it's a proper noun.
        2. If the word is capitalized and IS at the beginning of the sentence:
           - If it exists in the frequency list, it's a normal word.
           - If it does NOT exist in the frequency list, it's a proper noun.
        """
        import re
        
        # Remove HTML tags from the word
        no_html_word = re.sub(r'<[^>]*>', '', word)
        # Remove leading/trailing punctuation from the word
        cleaned_word = re.sub(r'^[^\w]+|[^\w]+$', '', no_html_word)
        if not cleaned_word:
            return False

        # If not capitalized, not a proper noun
        if cleaned_word[0] != cleaned_word[0].upper() or cleaned_word.lower() == cleaned_word:
            return False

        # Find the first word in the sentence (after trimming leading spaces)
        sentence_trimmed = sentence.strip()
        # Split on whitespace, but keep punctuation attached for first word
        first_word_match = re.match(r'^([a-zA-Z0-9\'-]+)', sentence_trimmed)
        first_word = first_word_match.group(1) if first_word_match else ''

        # Is this word at the beginning of the sentence?
        if cleaned_word == first_word:
            # If the word (lowercased) is in the frequency list, it's a normal word
            if cleaned_word.lower() in frequency_list:
                return False
            else:
                return True  # Not in frequency list, treat as proper noun
        else:
            # Not at beginning, capitalized → proper noun
            return True

    def is_word_known(self, word: str, known_words: Set[str], language: str) -> bool:
        """
        Check if a word is known, including checking contractions for English
        """
        word_lower = word.lower()
        
        # First check if the word itself is known
        if word_lower in known_words:
            return True
        
        # For English, check if it's a contraction and if ALL words in the expansion are known
        if language == 'en':
            expansion = self._get_contraction_expansion(word)
            if expansion:
                # Check if ALL words in the expansion are known
                return all(expanded_word.lower() in known_words for expanded_word in expansion)
        
        return False

    def _get_contraction_expansion(self, word: str) -> Optional[List[str]]:
        """Get the expanded form of a contraction for English"""
        word_lower = word.lower()
        expansion = self.english_contractions.get(word_lower)
        if expansion:
            # Preserve the original case of the first letter if it was capitalized
            if word[0] == word[0].upper():
                return [expansion[0].capitalize()] + expansion[1:]
            return expansion
        return None

    def _srt_time_to_ms(self, time: str) -> int:
        """Convert SRT time string to milliseconds"""
        try:
            parts = re.split(r'[:,]', time)
            h = int(parts[0])
            m = int(parts[1])
            s = int(parts[2])
            ms = int(parts[3])
            return h * 3600000 + m * 60000 + s * 1000 + ms
        except (ValueError, IndexError):
            return 0

    def _has_intersection(self, start1: str, end1: str, start2: str, end2: str) -> bool:
        """Check if two time ranges intersect"""
        start1_ms = self._srt_time_to_ms(start1)
        end1_ms = self._srt_time_to_ms(end1)
        start2_ms = self._srt_time_to_ms(start2)
        end2_ms = self._srt_time_to_ms(end2)

        intersection_start = max(start1_ms, start2_ms)
        intersection_end = min(end1_ms, end2_ms)

        return intersection_end - intersection_start > 500

    def fuse_subtitles(self, 
                      target_subs: List[Subtitle],
                      native_subs: List[Subtitle], 
                      known_words: Set[str],
                      lang: str,
                      enable_inline_translation: bool = False,
                      deepl_api: Optional[Any] = None,
                      native_lang: Optional[str] = None) -> Dict[str, Any]:
        """
        Main fusion algorithm - migrated from TypeScript fuseSubtitles function
        """
        import re
        from lemmatizer import lemmatize_single_line
        from srt_parser import normalize_words
        
        replaced_count = 0
        replaced_with_one_unknown = 0
        inline_translation_count = 0
        error_count = 0
        debug_shown = 0
        translated_words = {}
        
        final_subtitles = []
        processed_target_indices = set()
        
        # Helper function to strip HTML tags
        def strip_html(text: str) -> str:
            return re.sub(r'<[^>]*>', '', text)
        
        for i, current_target_sub in enumerate(target_subs):
            if current_target_sub.index in processed_target_indices:
                continue
            
            # Lemmatize this specific subtitle individually
            current_line = ' '.join(normalize_words(strip_html(current_target_sub.text)))
            lemmatized_words = lemmatize_single_line(current_line, lang)
            original_words = strip_html(current_target_sub.text).split()
            
            # Add null check for lemmatized_words
            if not lemmatized_words or not isinstance(lemmatized_words, list):
                print(f"Warning: No lemmatized words found for subtitle {current_target_sub.index}, skipping.")
                final_subtitles.append(current_target_sub)
                processed_target_indices.add(current_target_sub.index)
                continue
            
            # DETAIL FOR FIRST 20 SUBTITLES
            should_show_details = debug_shown < 20
            
            if should_show_details:
                print(f"\nSubtitle analysed: {current_target_sub.index} - \"{current_target_sub.text}\"")
            
            # Analyze each word
            proper_nouns = []
            lemmatized_words_list = []
            unknown_words_list = []
            
            unknown_words = []
            for j, word in enumerate(lemmatized_words):
                orig_word = original_words[j] if j < len(original_words) else word
                is_known = self.is_word_known(word, known_words, lang)
                is_proper = self.is_proper_noun(orig_word, current_target_sub.text, known_words)
                
                # Check if word is a number (consists entirely of digits)
                is_number = word.isdigit()
                
                lemmatized_words_list.append(word)
                
                if is_proper:
                    proper_nouns.append(orig_word)
                elif not is_known and not is_number:
                    unknown_words_list.append(word)
                
                if not is_known and not is_proper and not is_number:
                    unknown_words.append(word)
            
            if should_show_details:
                print(f"Proper nouns: {', '.join(proper_nouns) if proper_nouns else 'none'}")
                print(f"Words lemmatised: {', '.join(lemmatized_words_list)}")
                print(f"Unknown words: {', '.join(unknown_words_list) if unknown_words_list else 'none'}")
            
            if len(unknown_words) == 0:
                if should_show_details:
                    print("Decision: kept in target language")
                    print("Reason: all words are known or proper nouns")
                final_subtitles.append(current_target_sub)
                processed_target_indices.add(current_target_sub.index)
                debug_shown += 1
                continue
            
            # Handle multiple unknown words - replace with native subtitle
            if should_show_details:
                print("Decision: replaced with native subtitle")
                print(f"Reason: {len(unknown_words)} unknown words detected")
            
            # Find intersecting native subtitles
            intersecting_native_subs = [
                native_sub for native_sub in native_subs
                if self._has_intersection(current_target_sub.start, current_target_sub.end, 
                                        native_sub.start, native_sub.end)
            ]
            
            if len(intersecting_native_subs) == 0:
                if should_show_details:
                    print("Decision: kept in target language")
                    print("Reason: no native subtitle found")
                final_subtitles.append(current_target_sub)
                processed_target_indices.add(current_target_sub.index)
                debug_shown += 1
                continue
            
            # Find all target subtitles that overlap with the native subtitle time range
            combined_native_sub = {
                'text': '\n'.join(s.text for s in intersecting_native_subs),
                'start': intersecting_native_subs[0].start,
                'end': intersecting_native_subs[-1].end,
            }
            
            # Find all target subtitles that overlap with this native subtitle
            overlapping_target_subs = [
                sub for sub in target_subs
                if sub.index not in processed_target_indices and 
                self._has_intersection(combined_native_sub['start'], combined_native_sub['end'], 
                                     sub.start, sub.end)
            ]
            
            if len(overlapping_target_subs) == 0:
                if should_show_details:
                    print("Decision: kept in target language")
                    print("Reason: no overlapping target subtitles found")
                final_subtitles.append(current_target_sub)
                processed_target_indices.add(current_target_sub.index)
                debug_shown += 1
                continue
            
            # Create a single replacement subtitle that covers the entire overlapping time range
            replacement_sub = Subtitle(
                index='',  # Will be re-indexed later
                start=overlapping_target_subs[0].start,
                end=overlapping_target_subs[-1].end,
                text=combined_native_sub['text']
            )
            
            if should_show_details:
                print("Decision: replaced with native subtitle")
                print(f"Reason: {len(overlapping_target_subs)} overlapping subtitles replaced")
            
            final_subtitles.append(replacement_sub)
            replaced_count += len(overlapping_target_subs)
            
            # Mark all overlapping target subtitles as processed
            for sub in overlapping_target_subs:
                processed_target_indices.add(sub.index)
            debug_shown += 1
        
        # Re-index the final subtitles
        re_indexed_hybrid = []
        for i, subtitle in enumerate(final_subtitles):
            re_indexed_hybrid.append(Subtitle(
                index=str(i + 1),
                start=subtitle.start,
                end=subtitle.end,
                text=subtitle.text
            ))
        
        return {
            'hybrid': re_indexed_hybrid,
            'replacedCount': replaced_count,
            'replacedWithOneUnknown': replaced_with_one_unknown,
            'inlineTranslationCount': inline_translation_count,
            'errorCount': error_count,
            'translatedWords': translated_words,
            'success': True
        }
