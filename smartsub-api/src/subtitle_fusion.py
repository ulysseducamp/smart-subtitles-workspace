"""
Main subtitle fusion engine - Python implementation
Migrated from TypeScript logic.ts
"""

from typing import List, Set, Dict, Any, Optional
from dataclasses import dataclass
import re
import time
import logging
from srt_parser import Subtitle
from frequency_loader import get_frequency_loader

# Configure logger
logger = logging.getLogger(__name__)

class SubtitleFusionEngine:
    """
    Main engine for subtitle fusion algorithm
    Migrated from TypeScript logic.ts
    """
    
    def __init__(self):
        # English contractions mapping - migrated from logic.ts
        # Debug logs storage for ordered display
        self._debug_logs = []
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

    def _format_words_with_ranks(self, words: List[str], language: str, top_n: int = 2000) -> str:
        """
        Format words with their frequency ranks for logging.
        
        Args:
            words: List of words to format
            language: Language code for ranking lookup
            top_n: Number of top words to consider
            
        Returns:
            Formatted string with words and their ranks
        """
        if not words:
            return "none"
        
        try:
            frequency_loader = get_frequency_loader()
            formatted_words = []
            
            for word in words:
                rank = frequency_loader.get_word_rank(word, language, top_n)
                if rank is not None:
                    formatted_words.append(f"{word} → rang {rank}/{top_n} (connu)")
                else:
                    formatted_words.append(f"{word} → inconnu (hors des {top_n} premiers)")
            
            return ", ".join(formatted_words)
            
        except Exception as e:
            # Fallback to simple format if ranking fails
            logger.warning(f"Failed to get word ranks: {e}")
            return ", ".join(words)

    def _log_subtitle_details(self, subtitle_index: str, original_text: str, proper_nouns: List[str], 
                             words_ranks: str, unknown_words: List[str], decision: str, 
                             reason: str, final_text: str) -> None:
        """
        Helper function pour stocker les détails d'un sous-titre pour affichage ordonné.
        Les logs seront affichés à la fin dans l'ordre correct des sous-titres.
        
        Args:
            subtitle_index: Index du sous-titre
            original_text: Texte original du sous-titre
            proper_nouns: Liste des noms propres détectés
            words_ranks: Mots analysés avec leurs rangs
            unknown_words: Liste des mots inconnus
            decision: Décision prise (kept, replaced, inline translation)
            reason: Raison de la décision
            final_text: Texte final du sous-titre
        """
        # Stocker les infos de debug pour affichage ordonné plus tard
        self._debug_logs.append({
            'index': subtitle_index,
            'original_text': original_text,
            'proper_nouns': proper_nouns,
            'words_ranks': words_ranks,
            'unknown_words': unknown_words,
            'decision': decision,
            'reason': reason,
            'final_text': final_text
        })

    def _display_ordered_logs(self, final_subtitles: List[Subtitle]) -> None:
        """
        Affiche les logs de debug dans l'ordre correct des sous-titres finaux.
        
        Args:
            final_subtitles: Liste des sous-titres finaux dans l'ordre correct
        """
        # Créer un dictionnaire pour un accès rapide aux logs par index
        logs_by_index = {log['index']: log for log in self._debug_logs}
        
        # Afficher les logs dans l'ordre des sous-titres finaux
        for subtitle in final_subtitles:
            if subtitle.index in logs_by_index:
                log_entry = logs_by_index[subtitle.index]
                
                # Afficher le log de manière atomique
                logger.info(f"=== SUBTITLE {log_entry['index']} ===")
                logger.info(f"Original: \"{log_entry['original_text']}\"")
                logger.info(f"Proper nouns: {', '.join(log_entry['proper_nouns']) if log_entry['proper_nouns'] else 'none'}")
                logger.info(f"Mots analysés: {log_entry['words_ranks']}")
                logger.info(f"Unknown words: {', '.join(log_entry['unknown_words']) if log_entry['unknown_words'] else 'none'}")
                logger.info(f"Decision: {log_entry['decision']}")
                logger.info(f"Reason: {log_entry['reason']}")
                logger.info(f"Final subtitle: \"{log_entry['final_text']}\"")
                logger.info("")

    def fuse_subtitles(self, 
                      target_subs: List[Subtitle],
                      native_subs: List[Subtitle], 
                      known_words: Set[str],
                      lang: str,
                      enable_inline_translation: bool = False,
                      deepl_api: Optional[Any] = None,
                      native_lang: Optional[str] = None,
                      top_n: int = 2000) -> Dict[str, Any]:
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
        
        # Batch translation: collect words to translate instead of translating immediately
        unknown_words_to_translate = []  # Use list to preserve order
        word_to_subtitle_mapping = {}  # Map word -> subtitle for later integration
        
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
                logger.warning(f"No lemmatized words found for subtitle {current_target_sub.index}, skipping.")
                final_subtitles.append(current_target_sub)
                processed_target_indices.add(current_target_sub.index)
                continue
            
            # DETAIL FOR FIRST 20 SUBTITLES
            should_show_details = debug_shown < 20
            
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
            
            if len(unknown_words) == 0:
                if should_show_details:
                    # Format words with ranks for better debugging
                    words_with_ranks = self._format_words_with_ranks(lemmatized_words_list, lang, top_n)
                    
                    # Use helper function for atomic logging
                    self._log_subtitle_details(
                        subtitle_index=current_target_sub.index,
                        original_text=current_target_sub.text,
                        proper_nouns=proper_nouns,
                        words_ranks=words_with_ranks,
                        unknown_words=unknown_words_list,
                        decision="kept in target language",
                        reason="all words are known or proper nouns",
                        final_text=current_target_sub.text
                    )
                final_subtitles.append(current_target_sub)
                processed_target_indices.add(current_target_sub.index)
                debug_shown += 1
                continue
            
            # Handle single unknown word with inline translation
            if len(unknown_words) == 1 and enable_inline_translation and native_lang:
                # Find the original word corresponding to the lemmatized unknown word
                try:
                    lemma_index = lemmatized_words.index(unknown_words[0])
                    original_word = original_words[lemma_index]
                except (ValueError, IndexError):
                    # Fallback: use the lemmatized word as original if mapping fails
                    original_word = unknown_words[0]
                
                # BATCH TRANSLATION: Collect word for batch translation instead of translating immediately
                if original_word not in unknown_words_to_translate:
                    unknown_words_to_translate.append(original_word)
                word_to_subtitle_mapping[original_word] = current_target_sub
                
                if should_show_details:
                    # Format words with ranks for better debugging
                    words_with_ranks = self._format_words_with_ranks(lemmatized_words_list, lang, top_n)
                    
                    # Use helper function for atomic logging
                    self._log_subtitle_details(
                        subtitle_index=current_target_sub.index,
                        original_text=current_target_sub.text,
                        proper_nouns=proper_nouns,
                        words_ranks=words_with_ranks,
                        unknown_words=unknown_words_list,
                        decision="inline translation for single unknown word (COLLECTED FOR BATCH)",
                        reason=f"1 unknown word detected, collecting original word '{original_word}' (lemmatized: '{unknown_words[0]}') for batch translation",
                        final_text=current_target_sub.text
                    )
                
                # Skip processing for now - will be handled in batch translation phase
                continue
            
            # Handle multiple unknown words - replace with native subtitle
            # Find intersecting native subtitles
            intersecting_native_subs = [
                native_sub for native_sub in native_subs
                if self._has_intersection(current_target_sub.start, current_target_sub.end, 
                                        native_sub.start, native_sub.end)
            ]
            
            if len(intersecting_native_subs) == 0:
                if should_show_details:
                    # Format words with ranks for better debugging
                    words_with_ranks = self._format_words_with_ranks(lemmatized_words_list, lang, top_n)
                    
                    # Use helper function for atomic logging
                    self._log_subtitle_details(
                        subtitle_index=current_target_sub.index,
                        original_text=current_target_sub.text,
                        proper_nouns=proper_nouns,
                        words_ranks=words_with_ranks,
                        unknown_words=unknown_words_list,
                        decision="kept in target language",
                        reason="no native subtitle found",
                        final_text=current_target_sub.text
                    )
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
                    # Format words with ranks for better debugging
                    words_with_ranks = self._format_words_with_ranks(lemmatized_words_list, lang, top_n)
                    
                    # Use helper function for atomic logging
                    self._log_subtitle_details(
                        subtitle_index=current_target_sub.index,
                        original_text=current_target_sub.text,
                        proper_nouns=proper_nouns,
                        words_ranks=words_with_ranks,
                        unknown_words=unknown_words_list,
                        decision="kept in target language",
                        reason="no overlapping target subtitles found",
                        final_text=current_target_sub.text
                    )
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
                # Format words with ranks for better debugging
                words_with_ranks = self._format_words_with_ranks(lemmatized_words_list, lang, top_n)
                
                # Use helper function for atomic logging
                self._log_subtitle_details(
                    subtitle_index=current_target_sub.index,
                    original_text=current_target_sub.text,
                    proper_nouns=proper_nouns,
                    words_ranks=words_with_ranks,
                    unknown_words=unknown_words_list,
                    decision="replaced with native subtitle",
                    reason=f"{len(overlapping_target_subs)} overlapping subtitles replaced",
                    final_text=combined_native_sub['text']
                )
            
            final_subtitles.append(replacement_sub)
            replaced_count += len(overlapping_target_subs)
            
            # Mark all overlapping target subtitles as processed
            for sub in overlapping_target_subs:
                processed_target_indices.add(sub.index)
            debug_shown += 1
        
        # Re-index the final subtitles
        # BATCH TRANSLATION: Translate all collected words in a single API call
        if unknown_words_to_translate and enable_inline_translation and deepl_api and native_lang:
            logger.info(f"\n🔄 BATCH TRANSLATION: Translating {len(unknown_words_to_translate)} words in a single API call...")
            
            try:
                # Convert set to list for batch translation
                words_list = list(unknown_words_to_translate)
                
                # Translate all words in a single batch request
                translated_words_batch = deepl_api.translate_batch(words_list, lang, native_lang)
                
                # Create mapping of original words to translations
                word_translations = dict(zip(words_list, translated_words_batch))
                
                logger.info(f"✅ Batch translation successful! Translated {len(word_translations)} words")
                
                # Apply translations to subtitles
                for original_word, translation in word_translations.items():
                    subtitle = word_to_subtitle_mapping[original_word]
                    
                    # Replace the word in the subtitle text
                    original_text = subtitle.text
                    pattern = re.compile(re.escape(original_word), re.IGNORECASE)
                    new_text = pattern.sub(f"{original_word} ({translation})", original_text)
                    
                    # Create new subtitle with inline translation
                    translated_sub = Subtitle(
                        index=subtitle.index,
                        start=subtitle.start,
                        end=subtitle.end,
                        text=new_text
                    )
                    
                    final_subtitles.append(translated_sub)
                    inline_translation_count += 1
                    
                    logger.info(f"  📝 '{original_word}' → '{translation}' applied to subtitle {subtitle.index}")
                
            except Exception as e:
                logger.error(f"❌ Batch translation failed: {e}")
                logger.info("🔄 Falling back to original subtitles without inline translations")
                # Add original subtitles without translations
                for original_word in unknown_words_to_translate:
                    subtitle = word_to_subtitle_mapping[original_word]
                    final_subtitles.append(subtitle)
        else:
            # No DeepL API available - add original subtitles without translations
            if unknown_words_to_translate:
                logger.info(f"🔄 No DeepL API available - adding {len(unknown_words_to_translate)} original subtitles without translations")
                for original_word in unknown_words_to_translate:
                    subtitle = word_to_subtitle_mapping[original_word]
                    final_subtitles.append(subtitle)
        
        # Afficher les logs de debug dans l'ordre correct des sous-titres finaux
        # IMPORTANT: Doit être fait APRÈS que final_subtitles soit complètement construit
        if self._debug_logs:
            self._display_ordered_logs(final_subtitles)
            # Nettoyer la liste temporaire pour éviter les fuites mémoire
            self._debug_logs.clear()
        
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
