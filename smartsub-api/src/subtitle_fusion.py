"""
Main subtitle fusion engine - Python implementation
Migrated from TypeScript logic.ts
"""

from typing import List, Set, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import re
import time
import logging
import string
from srt_parser import Subtitle
from frequency_loader import get_frequency_loader

@dataclass
class TokenMapping:
    """Mapping pour maintenir l'alignement entre mots originaux et traités"""
    original_index: int      # Index dans le texte original
    original_word: str       # Mot original avec ponctuation
    normalized_word: str     # Mot après normalisation (vide si filtré)
    lemmatized_word: str     # Mot après lemmatisation (vide si filtré)
    is_filtered: bool        # True si supprimé par normalize_words

# Configure logger
logger = logging.getLogger(__name__)

def clean_word_for_translation(word: str) -> str:
    """
    Nettoie un mot pour traduction selon best practices NLP
    - Enlève ponctuation de début/fin (leading/trailing uniquement)
    - Préserve ponctuation interne (traits d'union, apostrophes)

    Exemples:
        "tensão]" → "tensão"
        "[ofegando]" → "ofegando"
        "motor." → "motor"
        "pré-lavagem" → "pré-lavagem" (garde trait d'union)
        "d'água" → "d'água" (garde apostrophe)
        "—Olá!" → "Olá" (tiret dialogue Unicode)
    """
    # Ponctuation étendue : ASCII + caractères Unicode courants
    extended_punctuation = string.punctuation + '—–…''""«»'
    return word.strip(extended_punctuation)

def extract_trailing_punctuation(word: str) -> str:
    """
    Extrait la ponctuation à la fin du mot

    Exemples:
        "motor." → "."
        "tensão]" → "]"
        "banco" → ""
        "uísque?!" → "?!"
    """
    # Ponctuation étendue : ASCII + caractères Unicode courants
    extended_punctuation = string.punctuation + '—–…''""«»'
    clean = word.rstrip(extended_punctuation)
    return word[len(clean):]

def apply_translation(subtitle_text: str, word: str, translation: str) -> str:
    """
    Applique une traduction inline avec regex + word boundaries.

    Cette fonction utilise regex avec word boundaries (\b) et le flag IGNORECASE
    pour trouver toutes les occurrences du mot dans le texte original et ajouter
    la traduction inline.

    Args:
        subtitle_text: Texte original du sous-titre
        word: Mot normalisé à chercher (sans ponctuation, lowercase)
        translation: Traduction à insérer

    Returns:
        Texte avec traduction inline: "word (translation)"

    Exemples:
        apply_translation("Il mange du pain.", "mange", "eats")
        → "Il mange (eats) du pain."

        apply_translation("Mange ton repas!", "mange", "eat")
        → "Mange (eat) ton repas!"

        apply_translation("mange, mange!", "mange", "eat")
        → "mange (eat), mange (eat)!"
    """
    # Escape le mot pour regex (caractères spéciaux comme ., ?, +, etc.)
    escaped_word = re.escape(word)

    # Pattern avec word boundaries + case insensitive
    # \b assure qu'on matche uniquement le mot entier, pas une partie d'un autre mot
    pattern = re.compile(r'\b' + escaped_word + r'\b', re.IGNORECASE)

    # Remplace avec traduction inline
    # On utilise une fonction lambda pour préserver la casse originale du mot matché
    def replacement(match):
        original_word = match.group(0)
        return f"{original_word} ({translation})"

    new_text = pattern.sub(replacement, subtitle_text)

    return new_text

def create_alignment_mapping(text: str, lang: str) -> List[TokenMapping]:
    """
    Crée un mapping complet avec alignement préservé entre mots originaux et traités

    Args:
        text: Texte du sous-titre (sans HTML)
        lang: Code de langue pour la lemmatisation

    Returns:
        Liste des TokenMapping avec alignement préservé
    """
    from lemmatizer import smart_lemmatize_line
    from srt_parser import normalize_words
    import re

    # 1. Extraire les mots originaux
    original_words = text.split()

    # 2. Normaliser et lemmatiser intelligemment
    normalized_words = normalize_words(text)
    normalized_line = ' '.join(normalized_words)
    lemmatized_words = smart_lemmatize_line(normalized_line, lang) if normalized_words else []

    # 3. Créer le mapping avec alignement
    mappings = []
    normalized_idx = 0

    for orig_idx, original_word in enumerate(original_words):
        # Normaliser ce mot individuellement pour vérifier s'il est filtré
        single_word_normalized = normalize_words(original_word)

        if single_word_normalized:  # Mot non filtré
            normalized_word = single_word_normalized[0] if single_word_normalized else ""
            lemmatized_word = lemmatized_words[normalized_idx] if normalized_idx < len(lemmatized_words) else ""

            mappings.append(TokenMapping(
                original_index=orig_idx,
                original_word=original_word,
                normalized_word=normalized_word,
                lemmatized_word=lemmatized_word,
                is_filtered=False
            ))
            normalized_idx += 1
        else:  # Mot filtré
            mappings.append(TokenMapping(
                original_index=orig_idx,
                original_word=original_word,
                normalized_word="",
                lemmatized_word="",
                is_filtered=True
            ))

    return mappings

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
    
    def _analyze_subtitle_words(self, subtitle_text: str, lang: str, known_words: Set[str], full_frequency_list: Set[str]) -> Dict[str, Any]:
        """
        Analyse les mots d'un sous-titre selon le flow en 2 phases.

        Returns dict avec:
        - normalized_words: liste des mots normalisés (lowercase, pas ponctuation)
        - lemmatized_words: liste des lemmes (même longueur que normalized_words)
        - word_statuses: liste des statuts ("known", "unknown", "proper_noun")
        - proper_nouns: liste des noms propres détectés
        - unknown_words: liste des mots inconnus (à traduire)
        """
        from lemmatizer import lemmatize_single_line

        # a. Enlever HTML tags
        text = re.sub(r'<[^>]*>', '', subtitle_text)

        # b. Enlever ponctuation (garder capitales)
        text_no_punct = re.sub(r'[^\w\s]', ' ', text)

        # c. Split en mots
        words_with_caps = text_no_punct.split()

        # d. Filtrer mots courts (< 2 lettres)
        words_with_caps = [w for w in words_with_caps if len(w) >= 2]

        if not words_with_caps:
            return {
                'normalized_words': [],
                'lemmatized_words': [],
                'word_statuses': [],
                'proper_nouns': [],
                'unknown_words': []
            }

        # e. PHASE 1 - Marquage basé sur capitalisation
        word_categories = []  # "confirmed_proper", "potential_proper", "normal"

        for i, word in enumerate(words_with_caps):
            if word[0].isupper():
                if i == 0:
                    # Premier mot avec majuscule → potentiel
                    word_categories.append("potential_proper")
                else:
                    # Majuscule au milieu → confirmé nom propre
                    word_categories.append("confirmed_proper")
            else:
                word_categories.append("normal")

        # f. Convertir TOUS les mots en minuscules
        normalized_words = [w.lower() for w in words_with_caps]

        # g. Lemmatiser sélectivement
        lemmatized_words = []
        for i, norm_word in enumerate(normalized_words):
            category = word_categories[i]

            if category == "confirmed_proper":
                # Ne PAS lemmatiser les noms propres confirmés
                lemmatized_words.append(norm_word)
            else:
                # Lemmatiser les autres (potentiel + normal)
                # lemmatize_single_line retourne une liste, prendre le premier élément
                lemmas = lemmatize_single_line(norm_word, lang)
                lemma = lemmas[0] if lemmas else norm_word
                lemmatized_words.append(lemma)

        # h. PHASE 2 - Vérification et analyse
        word_statuses = []
        proper_nouns = []
        unknown_words = []

        for i in range(len(normalized_words)):
            norm_word = normalized_words[i]
            lemma = lemmatized_words[i]
            category = word_categories[i]

            # Check if number
            if lemma.isdigit():
                word_statuses.append("known")
                continue

            if category == "confirmed_proper":
                # Nom propre confirmé → CONNU
                word_statuses.append("known")
                proper_nouns.append(norm_word)

            elif category == "potential_proper":
                # Nom propre potentiel → vérifier
                if lemma in known_words:
                    # Dans top N → mot commun CONNU
                    word_statuses.append("known")
                elif lemma in full_frequency_list:
                    # Dans liste complète mais pas top N → mot INCONNU
                    word_statuses.append("unknown")
                    unknown_words.append(norm_word)
                else:
                    # Pas dans liste du tout → NOM PROPRE
                    word_statuses.append("known")
                    proper_nouns.append(norm_word)

            else:  # category == "normal"
                # Mot normal
                if lemma in known_words:
                    word_statuses.append("known")
                else:
                    word_statuses.append("unknown")
                    unknown_words.append(norm_word)

        return {
            'normalized_words': normalized_words,
            'lemmatized_words': lemmatized_words,
            'word_statuses': word_statuses,
            'proper_nouns': proper_nouns,
            'unknown_words': unknown_words
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

    def is_word_known(self, word: str, known_words: Set[str], language: str, original_word: str = None, subtitle_index: str = None) -> bool:
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
                all_known = all(expanded_word.lower() in known_words for expanded_word in expansion)
                return all_known

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

    def _calculate_intersection_duration(self, sub1: Subtitle, sub2: Subtitle) -> float:
        """
        Calculate the duration of intersection between two subtitles in seconds.

        Args:
            sub1: First subtitle
            sub2: Second subtitle

        Returns:
            Duration of intersection in seconds (0 if no intersection)
        """
        start1_ms = self._srt_time_to_ms(sub1.start)
        end1_ms = self._srt_time_to_ms(sub1.end)
        start2_ms = self._srt_time_to_ms(sub2.start)
        end2_ms = self._srt_time_to_ms(sub2.end)

        intersection_start = max(start1_ms, start2_ms)
        intersection_end = min(end1_ms, end2_ms)

        if intersection_end <= intersection_start:
            return 0.0

        return (intersection_end - intersection_start) / 1000.0  # Convert to seconds

    def _get_next_native_subtitle(self, current_native_index: int, native_subs: List[Subtitle]) -> Optional[Subtitle]:
        """
        Get the next native subtitle after the current one.

        Args:
            current_native_index: Index position in native_subs list
            native_subs: List of all native subtitles

        Returns:
            Next native subtitle or None if current is the last one
        """
        if current_native_index + 1 < len(native_subs):
            return native_subs[current_native_index + 1]
        return None

    def _get_previous_target_subtitle(self, current_target_index: int, target_subs: List[Subtitle]) -> Optional[Subtitle]:
        """
        Get the previous target subtitle before the current one.

        Args:
            current_target_index: Index position in target_subs list
            target_subs: List of all target subtitles

        Returns:
            Previous target subtitle or None if current is the first one
        """
        if current_target_index > 0:
            return target_subs[current_target_index - 1]
        return None

    def _should_include_in_replacement(self, target_sub: Subtitle, current_native: Subtitle,
                                       next_native: Optional[Subtitle]) -> bool:
        """
        Determine if a target subtitle should be included in the current replacement.

        Logic: If the target subtitle overlaps MORE with the next native subtitle,
        it belongs to the next replacement, so exclude it from the current one.

        Args:
            target_sub: Target subtitle to evaluate
            current_native: Current native subtitle being processed
            next_native: Next native subtitle (or None if last)

        Returns:
            True if should include, False if should exclude
        """
        current_overlap = self._calculate_intersection_duration(target_sub, current_native)

        # If no next native subtitle, include (last subtitle of episode)
        if not next_native:
            # INCLUDE LOGIC DEBUG LOGS DISABLED - Uncomment to re-enable specific subtitle debugging
            # logger.info(f"   [Include Logic] PT {target_sub.index}: No next FR → INCLUDE (end of episode)")
            return True

        next_overlap = self._calculate_intersection_duration(target_sub, next_native)

        # If overlaps more with next, exclude from current replacement
        should_include = next_overlap <= current_overlap

        # Log decision
        # if target_sub.index in ["496", "764", "763"]:  # Debug specific cases
        #     logger.info(f"   [Include Logic] PT {target_sub.index}:")
        #     logger.info(f"      Current FR overlap: {current_overlap:.3f}s")
        #     logger.info(f"      Next FR overlap: {next_overlap:.3f}s")
        #     logger.info(f"      Decision: {'INCLUDE' if should_include else 'EXCLUDE (belongs to next FR)'}")

        return should_include

    def _find_best_native_match(
        self,
        target_sub: Subtitle,
        target_index: int,
        target_subs: List[Subtitle],
        native_subs: List[Subtitle],
        processed_indices: set
    ) -> Optional[Subtitle]:
        """
        Find the best matching native subtitle for a target subtitle.
        Extracts and reuses logic from the "2+ unknown words" replacement flow.

        Args:
            target_sub: Target subtitle to find match for
            target_index: Index of target_sub in target_subs list
            target_subs: Full list of target subtitles
            native_subs: Full list of native subtitles
            processed_indices: Set of already processed target subtitle indices

        Returns:
            Replacement subtitle object if match found, None otherwise
        """
        # Find intersecting native subtitles
        intersecting_native_subs = [
            native_sub for native_sub in native_subs
            if self._has_intersection(target_sub.start, target_sub.end,
                                    native_sub.start, native_sub.end)
        ]

        # Apply avalanche filter (compare with previous PT subtitle)
        previous_target_sub = self._get_previous_target_subtitle(target_index, target_subs)

        if previous_target_sub:
            filtered_native_subs = []
            for native_sub in intersecting_native_subs:
                current_overlap = self._calculate_intersection_duration(
                    Subtitle(index='', start=native_sub.start, end=native_sub.end, text=''),
                    target_sub
                )
                previous_overlap = self._calculate_intersection_duration(
                    Subtitle(index='', start=native_sub.start, end=native_sub.end, text=''),
                    previous_target_sub
                )

                # Exclude if better match with previous target
                if previous_overlap > current_overlap:
                    continue

                filtered_native_subs.append(native_sub)

            intersecting_native_subs = filtered_native_subs

        # No matching native subtitles found
        if len(intersecting_native_subs) == 0:
            return None

        # Combine intersecting native subtitles
        combined_native_sub_obj = Subtitle(
            index='',
            start=intersecting_native_subs[0].start,
            end=intersecting_native_subs[-1].end,
            text='\n'.join(s.text for s in intersecting_native_subs)
        )

        # Find next native subtitle for filtering logic
        try:
            first_native_index = native_subs.index(intersecting_native_subs[0])
            next_native_sub = self._get_next_native_subtitle(first_native_index, native_subs)
        except ValueError:
            next_native_sub = None

        # Find all target subtitles that should be replaced by this native subtitle
        candidate_target_subs = [
            sub for sub in target_subs
            if sub.index not in processed_indices and
            self._has_intersection(combined_native_sub_obj.start, combined_native_sub_obj.end,
                                 sub.start, sub.end)
        ]

        # Filter candidates based on "compare with next FR" logic
        overlapping_target_subs = [
            sub for sub in candidate_target_subs
            if self._should_include_in_replacement(sub, combined_native_sub_obj, next_native_sub)
        ]

        # No overlapping target subtitles found
        if len(overlapping_target_subs) == 0:
            return None

        # Create replacement subtitle
        replacement_sub = Subtitle(
            index='',  # Will be re-indexed later
            start=overlapping_target_subs[0].start,
            end=overlapping_target_subs[-1].end,
            text=combined_native_sub_obj.text
        )

        return replacement_sub

    def _apply_native_fallback(
        self,
        target_sub: Subtitle,
        target_index: int,
        target_subs: List[Subtitle],
        native_subs: List[Subtitle],
        processed_indices: set,
        original_word: str,
        native_lang: str,
        target_lang: str
    ) -> Tuple[Subtitle, bool]:
        """
        Apply native subtitle fallback when translation fails.

        Args:
            target_sub: Target subtitle with failed translation
            target_index: Index of target_sub in target_subs list
            target_subs: Full list of target subtitles
            native_subs: Full list of native subtitles
            processed_indices: Set of already processed target subtitle indices
            original_word: The word that failed translation
            native_lang: Native language code (e.g., 'fr', 'en', 'es')
            target_lang: Target language code (e.g., 'pt', 'en', 'es')

        Returns:
            Tuple of (subtitle to use, fallback_applied boolean)
        """
        logger.info(f"   🔄 Attempting {native_lang.upper()} fallback for '{original_word}' in subtitle {target_sub.index}")

        # Try to find matching native subtitle
        replacement_sub = self._find_best_native_match(
            target_sub=target_sub,
            target_index=target_index,
            target_subs=target_subs,
            native_subs=native_subs,
            processed_indices=processed_indices
        )

        if replacement_sub:
            logger.info(f"   ✅ {native_lang.upper()} fallback applied: \"{replacement_sub.text[:80]}{'...' if len(replacement_sub.text) > 80 else ''}\"")
            return replacement_sub, True
        else:
            logger.warning(f"   ⚠️  No {native_lang.upper()} fallback found - keeping original {target_lang.upper()} subtitle")
            return target_sub, False

    def _generate_episode_context(self, subtitles: List[Subtitle]) -> str:
        """
        Generate full episode context in SRT format for LLM translation.

        Args:
            subtitles: List of subtitles to convert to SRT format

        Returns:
            Full SRT formatted string of all subtitles
        """
        srt_lines = []
        for sub in subtitles:
            srt_lines.append(str(sub.index))
            srt_lines.append(f"{sub.start} --> {sub.end}")
            srt_lines.append(sub.text)
            srt_lines.append("")  # Empty line between subtitles

        return "\n".join(srt_lines)

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
        # NOTE: l'affichage effectif est centralisé dans `_display_ordered_logs()`
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

    def _safe_int_conversion(self, index_str: str) -> int:
        """
        Convertit un index string en int de manière sécurisée.
        
        Args:
            index_str: String contenant l'index du sous-titre
            
        Returns:
            int: Index converti, ou 0 si la conversion échoue
        """
        try:
            return int(index_str)
        except (ValueError, TypeError):
            # Si conversion échoue, retourner 0 pour placer en premier à l'affichage uniquement
            return 0

    def _display_ordered_logs(self, final_subtitles: List[Subtitle]) -> None:
        """
        Affiche les logs de debug dans l'ordre correct des sous-titres finaux.
        RESPONSABILITÉ UNIQUE d'affichage des logs détaillés collectés durant le traitement.
        
        Args:
            final_subtitles: Liste des sous-titres finaux dans l'ordre correct
        """
        # Créer un dictionnaire pour un accès rapide aux logs par index
        logs_by_index = {log['index']: log for log in self._debug_logs}
        
        # Trier les sous-titres par index numérique pour affichage ordonné
        # Utiliser la conversion sécurisée pour éviter les erreurs 500 si l'index n'est pas numérique
        sorted_subtitles = sorted(final_subtitles, key=lambda s: self._safe_int_conversion(s.index))
        
        # Afficher les logs dans l'ordre numérique correct
        for subtitle in sorted_subtitles:
            if subtitle.index in logs_by_index:
                log_entry = logs_by_index[subtitle.index]

                # VERBOSE LOGS DISABLED - Uncomment to re-enable detailed subtitle debugging
                # Afficher le log de manière atomique
                # logger.info(f"=== SUBTITLE {log_entry['index']} ===")
                # logger.info(f"Original: \"{log_entry['original_text']}\"")
                # logger.info(f"Proper nouns: {', '.join(log_entry['proper_nouns']) if log_entry['proper_nouns'] else 'none'}")
                # logger.info(f"Mots analysés: {log_entry['words_ranks']}")
                # logger.info(f"Unknown words: {', '.join(log_entry['unknown_words']) if log_entry['unknown_words'] else 'none'}")
                # logger.info(f"Decision: {log_entry['decision']}")
                # logger.info(f"Reason: {log_entry['reason']}")
                # logger.info(f"Final subtitle: \"{log_entry['final_text']}\"")
                # logger.info("")
                pass

    async def fuse_subtitles(self,
                      target_subs: List[Subtitle],
                      native_subs: List[Subtitle],
                      known_words: Set[str],
                      full_frequency_list: Set[str],
                      lang: str,
                      enable_inline_translation: bool = False,
                      deepl_api: Optional[Any] = None,
                      openai_translator: Optional[Any] = None,
                      native_lang: Optional[str] = None,
                      top_n: int = 2000,
                      max_concurrent: int = 5) -> Dict[str, Any]:
        """
        Main fusion algorithm - migrated from TypeScript fuseSubtitles function
        """
        import re
        from lemmatizer import lemmatize_single_line
        from srt_parser import normalize_words
        
        replaced_count = 0
        replaced_with_one_unknown = 0
        inline_translation_count = 0
        fallback_count = 0
        error_count = 0
        debug_shown = 0
        translated_words = {}

        # Batch translation: collect subtitles to translate (no deduplication to prevent subtitle loss)
        # Each tuple contains (original_word, subtitle) - duplicates preserved intentionally
        subtitles_to_translate = []  # List of (word, subtitle) tuples

        final_subtitles = []
        processed_target_indices = set()
        
        # Helper function to strip HTML tags
        def strip_html(text: str) -> str:
            return re.sub(r'<[^>]*>', '', text)
        
        for i, current_target_sub in enumerate(target_subs):
            if current_target_sub.index in processed_target_indices:
                continue

            # NEW: Analyze subtitle words using 2-phase proper noun detection
            analysis = self._analyze_subtitle_words(
                current_target_sub.text,
                lang,
                known_words,
                full_frequency_list
            )

            # Extract results from analysis
            normalized_words = analysis['normalized_words']
            lemmatized_words_list = analysis['lemmatized_words']
            word_statuses = analysis['word_statuses']
            proper_nouns = analysis['proper_nouns']
            unknown_words = analysis['unknown_words']

            # Add null check for empty analysis
            if not normalized_words:
                logger.warning(f"No words found in subtitle {current_target_sub.index}, skipping.")
                final_subtitles.append(current_target_sub)
                processed_target_indices.add(current_target_sub.index)
                continue

            # DETAIL FOR FIRST 20 SUBTITLES
            should_show_details = debug_shown < 20

            # DECISION FINALE LOG: Récapitulatif de la décision pour ce sous-titre
            total_words = len(lemmatized_words_list)
            unknown_count = len(unknown_words)
            proper_count = len(proper_nouns)
            known_count = total_words - unknown_count - proper_count

            # For logging compatibility: create unknown_words_list with lemmas
            unknown_words_list = [lemmatized_words_list[i] for i, word in enumerate(normalized_words) if word in unknown_words]

            # Disabled verbose logging - only log critical decisions
            # logger.info(f"DECISION_FINALE[{current_target_sub.index}]: total_mots={total_words}, connus={known_count}, inconnus={unknown_count}, noms_propres={proper_count}")

            if len(unknown_words) == 0:
                # logger.info(f"DECISION_FINALE[{current_target_sub.index}]: GARDÉ_EN_LANGUE_CIBLE (tous mots connus/noms propres)")
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
                # logger.info(f"DECISION_FINALE[{current_target_sub.index}]: TRADUCTION_INLINE (1 mot inconnu)")
                # NEW: Directly use the normalized unknown word (no alignment mapping needed)
                unknown_word = unknown_words[0]  # Already normalized (no punctuation, lowercase)

                # BATCH TRANSLATION: Collect (word, subtitle) tuple for batch translation
                # No deduplication - if same word appears in 10 subtitles, we translate 10 times
                # This prevents subtitle loss (Bug #1 fix)
                subtitles_to_translate.append((unknown_word, current_target_sub))
                
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
                        reason=f"1 unknown word detected, collecting normalized word '{unknown_word}' for batch translation",
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

            # Filter out native subtitles that match BETTER with the previous target subtitle
            # This prevents "avalanche" effect where a native sub incorrectly replaces multiple targets
            previous_target_sub = self._get_previous_target_subtitle(i, target_subs)

            # AVALANCHE DEBUG LOGS DISABLED - Uncomment to re-enable specific subtitle debugging
            # Log for debug cases
            # if current_target_sub.index in ["632", "633", "234", "235"]:
            #     logger.info(f"\n🔍 [Previous Filter] PT {current_target_sub.index}:")
            #     logger.info(f"   Initial FR candidates: {[s.index for s in intersecting_native_subs]}")
            #     if previous_target_sub:
            #         logger.info(f"   Previous PT: {previous_target_sub.index} ({previous_target_sub.start} → {previous_target_sub.end})")

            if previous_target_sub:
                filtered_native_subs = []
                for native_sub in intersecting_native_subs:
                    current_overlap = self._calculate_intersection_duration(
                        Subtitle(index='', start=native_sub.start, end=native_sub.end, text=''),
                        current_target_sub
                    )
                    previous_overlap = self._calculate_intersection_duration(
                        Subtitle(index='', start=native_sub.start, end=native_sub.end, text=''),
                        previous_target_sub
                    )

                    # If this native sub overlaps MORE with the previous target, exclude it
                    if previous_overlap > current_overlap:
                        # logger.info(f"   [Filter] Excluding FR {native_sub.index}: better match with PT {previous_target_sub.index} ({previous_overlap:.3f}s) than PT {current_target_sub.index} ({current_overlap:.3f}s)")
                        continue

                    filtered_native_subs.append(native_sub)

                intersecting_native_subs = filtered_native_subs

                # Log after filtering for debug cases
                # if current_target_sub.index in ["632", "633", "234", "235"]:
                #     logger.info(f"   After previous filter: {[s.index for s in intersecting_native_subs]}")

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

            # Create a Subtitle object for combined_native_sub (for helper functions)
            combined_native_sub_obj = Subtitle(
                index='',
                start=combined_native_sub['start'],
                end=combined_native_sub['end'],
                text=combined_native_sub['text']
            )

            # Find the index of the first intersecting native subtitle in the native_subs list
            try:
                first_native_index = native_subs.index(intersecting_native_subs[0])
                next_native_sub = self._get_next_native_subtitle(first_native_index, native_subs)
            except ValueError:
                # Fallback: if not found in list, assume no next subtitle
                next_native_sub = None

            # REPLACEMENT LOGIC DEBUG LOGS DISABLED - Uncomment to re-enable specific subtitle debugging
            # Log for debugging
            # if current_target_sub.index in ["496", "764", "763"]:
            #     logger.info(f"\n🔍 [Replacement Logic] Processing PT {current_target_sub.index}")
            #     logger.info(f"   Current FR range: {combined_native_sub['start']} → {combined_native_sub['end']}")
            #     if next_native_sub:
            #         logger.info(f"   Next FR: {next_native_sub.index} ({next_native_sub.start} → {next_native_sub.end})")
            #     else:
            #         logger.info(f"   Next FR: None (end of episode)")

            # Find all target subtitles that overlap with this native subtitle
            # STEP 1: Find all candidates (overlap > 0.5s)
            candidate_target_subs = [
                sub for sub in target_subs
                if sub.index not in processed_target_indices and
                self._has_intersection(combined_native_sub['start'], combined_native_sub['end'],
                                     sub.start, sub.end)
            ]

            # Log candidates
            # if current_target_sub.index in ["496", "764", "763"]:
            #     logger.info(f"   Candidate PT subs (overlap > 0.5s): {[s.index for s in candidate_target_subs]}")

            # STEP 2: Filter candidates based on "compare with next FR" logic
            overlapping_target_subs = [
                sub for sub in candidate_target_subs
                if self._should_include_in_replacement(sub, combined_native_sub_obj, next_native_sub)
            ]

            # Log final decision
            # if current_target_sub.index in ["496", "764", "763"]:
            #     logger.info(f"   Final PT subs to replace: {[s.index for s in overlapping_target_subs]}")

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

            # logger.info(f"DECISION_FINALE[{current_target_sub.index}]: REMPLACÉ_PAR_NATIF ({len(unknown_words)} mots inconnus)")
            
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
        
        # BATCH TRANSLATION: Translate each subtitle with its unique context (perfect quality)
        if subtitles_to_translate and enable_inline_translation and native_lang:
            logger.info(f"\n🔄 BATCH TRANSLATION: Processing {len(subtitles_to_translate)} subtitles with unique contexts...")

            # Build list of (word, context) tuples for translation
            # NEW: Words are already normalized (no punctuation), no cleaning needed
            words_with_contexts = []

            for word, subtitle in subtitles_to_translate:
                # Send normalized word directly to OpenAI with context
                words_with_contexts.append((word, strip_html(subtitle.text)))

            # Log unique words vs duplicates
            unique_words = set(word for word, _ in words_with_contexts)
            logger.info(f"   📊 Translation stats: {len(words_with_contexts)} total words, {len(unique_words)} unique words ({len(words_with_contexts) - len(unique_words)} duplicates)")

            # Log first 10 words with context for debugging
            logger.info(f"   📝 First 10 words with context:")
            for idx, (word, context) in enumerate(words_with_contexts[:10]):
                logger.info(f"      [{idx+1}] '{word}' in: \"{context[:80]}{'...' if len(context) > 80 else ''}\"")

            translations = {}

            # Strategy 1: Try OpenAI with PARALLEL translation
            if openai_translator:
                try:
                    logger.info(f"🤖 Using OpenAI GPT-4.1 Nano with PARALLEL translation...")

                    # Translate with OpenAI using parallel execution
                    translations = await openai_translator.translate_batch_parallel(
                        words_with_contexts=words_with_contexts,
                        source_lang=lang,
                        target_lang=native_lang,
                        max_concurrent=max_concurrent
                    )

                    logger.info(f"✅ OpenAI parallel translation successful! Translated {len(translations)} subtitles")

                except Exception as e:
                    logger.error(f"❌ OpenAI translation failed: {e}")
                    logger.info(f"🔄 Falling back to DeepL...")
                    translations = {}

            # Strategy 2: Fallback to DeepL (without context)
            if not translations and deepl_api:
                try:
                    logger.info(f"🔄 Using DeepL fallback (no context)...")

                    # Extract words for DeepL translation (already normalized)
                    words_only = [word for word, _ in subtitles_to_translate]
                    translations = deepl_api.translate_batch(words_only, lang, native_lang)

                    logger.info(f"✅ DeepL fallback successful! Translated {len(translations)} subtitles")

                except Exception as e:
                    logger.error(f"❌ DeepL translation failed: {e}")
                    logger.info("🔄 Falling back to original subtitles without translations")
                    translations = {}

            # Apply translations to each subtitle (matched by word)
            # Note: Check 'is not None' instead of truthiness to handle empty dict {}
            # When translations = {}, we still need to enter loop to apply fallback
            if translations is not None:
                # DIAGNOSTIC: Log before applying translations
                logger.info(f"   [FUSION] 🔧 Applying translations: {len(subtitles_to_translate)} words, {len(translations)} translations available")

                for word, subtitle in subtitles_to_translate:
                    # NEW: Word is already normalized (no punctuation, lowercase)
                    # Check if we have a translation for this normalized word
                    if word in translations:
                        translation = translations[word]

                        # DIAGNOSTIC: Log every translation application
                        logger.info(f"   [FUSION]    '{word}' → '{translation}' (subtitle {subtitle.index})")

                        # NEW: Use apply_translation() with regex + word boundaries
                        # Finds all occurrences of the normalized word in the original text
                        # and adds inline translation: "word (translation)"
                        # Word boundaries ensure we don't replace inside other words (e.g., "et" in "Antoinette")
                        new_text = apply_translation(subtitle.text, word, translation)

                        # Create new subtitle with inline translation
                        translated_sub = Subtitle(
                            index=subtitle.index,
                            start=subtitle.start,
                            end=subtitle.end,
                            text=new_text
                        )

                        final_subtitles.append(translated_sub)
                        inline_translation_count += 1
                    else:
                        # No translation available for this word - Try native fallback
                        logger.warning(f"⚠️  TRANSLATION FAILED for word '{word}' in subtitle {subtitle.index}")
                        logger.warning(f"   📝 Context: \"{subtitle.text}\"")

                        # Find the index of this subtitle in target_subs
                        target_index = next((i for i, sub in enumerate(target_subs) if sub.index == subtitle.index), None)

                        if target_index is not None:
                            # Apply native fallback
                            result_sub, fallback_applied = self._apply_native_fallback(
                                target_sub=subtitle,
                                target_index=target_index,
                                target_subs=target_subs,
                                native_subs=native_subs,
                                processed_indices=processed_target_indices,
                                original_word=word,
                                native_lang=native_lang,
                                target_lang=lang
                            )
                            final_subtitles.append(result_sub)
                            if fallback_applied:
                                fallback_count += 1
                        else:
                            # Fallback: couldn't find subtitle in target_subs, keep original
                            logger.error(f"   ❌ Could not find subtitle {subtitle.index} in target_subs list")
                            final_subtitles.append(subtitle)

                    # Mark as processed to prevent double-processing
                    processed_target_indices.add(subtitle.index)
            else:
                # No translation service available - add all original subtitles
                logger.info(f"⚠️  No translation service available - adding {len(subtitles_to_translate)} original subtitles")
                for word, subtitle in subtitles_to_translate:
                    final_subtitles.append(subtitle)
                    processed_target_indices.add(subtitle.index)
        else:
            # Translation disabled - add all original subtitles
            if subtitles_to_translate:
                logger.info(f"🔄 Translation disabled - adding {len(subtitles_to_translate)} original subtitles")
                for word, subtitle in subtitles_to_translate:
                    final_subtitles.append(subtitle)
                    processed_target_indices.add(subtitle.index)
        
        # Afficher les logs de debug dans l'ordre correct des sous-titres finaux
        # IMPORTANT: Doit être fait APRÈS que final_subtitles soit complètement construit
        if self._debug_logs:
            self._display_ordered_logs(final_subtitles)
            # Nettoyer la liste temporaire pour éviter les fuites mémoire
            self._debug_logs.clear()

        # CRITICAL FIX: Sort final_subtitles by timestamp BEFORE re-indexing
        # This ensures chronological order regardless of when subtitles were added to the list
        # (e.g., inline translation subtitles are added after the main loop)
        final_subtitles_sorted = sorted(final_subtitles, key=lambda s: self._srt_time_to_ms(s.start))

        re_indexed_hybrid = []
        for i, subtitle in enumerate(final_subtitles_sorted):
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
            'fallbackCount': fallback_count,
            'errorCount': error_count,
            'translatedWords': translated_words,
            'success': True
        }
