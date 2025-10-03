"""
OpenAI API integration for context-aware translation
Uses GPT-4o mini with Structured Outputs for guaranteed JSON reliability
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

# Language name mappings for prompts
LANGUAGE_NAMES = {
    'EN': 'English',
    'FR': 'French',
    'PT': 'Portuguese',
    'ES': 'Spanish',
    'DE': 'German',
    'IT': 'Italian',
    'PL': 'Polish',
    'NL': 'Dutch',
    'SV': 'Swedish',
    'DA': 'Danish',
    'CS': 'Czech',
    'JA': 'Japanese',
    'KO': 'Korean'
}

# Pydantic models for Structured Outputs
class WordTranslation(BaseModel):
    """Single word translation result"""
    word: str
    translation: str

class TranslationResponse(BaseModel):
    """Complete translation response with all words"""
    translations: List[WordTranslation]

class OpenAITranslator:
    """
    OpenAI-based translator using GPT-4o mini with Structured Outputs
    Supports full episode context for better translation quality
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini", timeout: float = 15.0):
        """
        Initialize OpenAI translator

        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o-mini)
            timeout: Request timeout in seconds (default: 15.0)
        """
        self.client = OpenAI(api_key=api_key, timeout=timeout)
        self.model = model
        self.cache = {}
        self.request_count = 0

    def translate_batch_with_context(
        self,
        episode_context: str,
        words_to_translate: List[str],
        source_lang: str,
        target_lang: str
    ) -> Dict[str, str]:
        """
        Translate multiple words with full episode context in a single API call

        Args:
            episode_context: Full SRT subtitle file content for context
            words_to_translate: List of words to translate
            source_lang: Source language code (e.g., 'PT', 'EN')
            target_lang: Target language code (e.g., 'FR', 'EN')

        Returns:
            Dictionary mapping original words to translations
        """
        if not words_to_translate:
            return {}

        # Check cache for all words
        cache_key_prefix = f"{source_lang}_{target_lang}_"
        cached_translations = {}
        uncached_words = []

        for word in words_to_translate:
            cache_key = f"{cache_key_prefix}{word}"
            if cache_key in self.cache:
                cached_translations[word] = self.cache[cache_key]
            else:
                uncached_words.append(word)

        # If all words are cached, return immediately
        if not uncached_words:
            logger.info(f"✅ All {len(words_to_translate)} words found in cache")
            return cached_translations

        logger.info(f"🔄 Translating {len(uncached_words)} words with OpenAI (GPT-4o mini)")
        logger.info(f"   Context size: {len(episode_context)} characters")

        try:
            # Build optimized prompt with episode context
            prompt = self._build_translation_prompt(
                episode_context=episode_context,
                words_to_translate=uncached_words,
                source_lang=source_lang,
                target_lang=target_lang
            )

            # Call OpenAI with Structured Outputs (guarantees JSON format)
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator for language learning subtitles. Provide accurate, natural translations using the episode context."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format=TranslationResponse,
                temperature=0.3  # Low temperature for consistent translations
            )

            # Extract translations from structured response
            # The parsed data is in response.choices[0].message.parsed
            parsed_data = response.choices[0].message.parsed
            new_translations = {
                item.word: item.translation
                for item in parsed_data.translations
            }

            # Cache new translations
            for word, translation in new_translations.items():
                cache_key = f"{cache_key_prefix}{word}"
                self.cache[cache_key] = translation

            # Combine cached and new translations
            all_translations = {**cached_translations, **new_translations}

            self.request_count += 1

            # Log usage stats
            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens

            # Calculate cost (GPT-4o mini pricing: $0.150/1M input, $0.600/1M output)
            cost = (input_tokens * 0.150 / 1_000_000) + (output_tokens * 0.600 / 1_000_000)

            logger.info(f"✅ OpenAI translation successful!")
            logger.info(f"   Words translated: {len(new_translations)} (cached: {len(cached_translations)})")
            logger.info(f"   Tokens: {input_tokens} input + {output_tokens} output = {total_tokens} total")
            logger.info(f"   Cost: ${cost:.6f}")

            return all_translations

        except Exception as e:
            logger.error(f"❌ OpenAI translation failed: {e}")
            raise  # Re-raise to allow fallback handling

    def _build_translation_prompt(
        self,
        episode_context: str,
        words_to_translate: List[str],
        source_lang: str,
        target_lang: str
    ) -> str:
        """Build optimized translation prompt with episode context"""

        source_name = LANGUAGE_NAMES.get(source_lang.upper(), source_lang)
        target_name = LANGUAGE_NAMES.get(target_lang.upper(), target_lang)

        # Create word list for prompt
        words_list = ", ".join(f'"{word}"' for word in words_to_translate)

        prompt = f"""You are translating subtitles for a language learning application.

TASK: Translate {len(words_to_translate)} {source_name} words to {target_name}.

EPISODE CONTEXT (full subtitles):
{episode_context}

WORDS TO TRANSLATE:
{words_list}

TRANSLATION RULES:
1. Use the episode context to understand the narrative, characters, and tone
2. Provide natural translations as a native speaker would say
3. Keep translations concise (1-3 words maximum)
4. Consider the specific context where each word appears
5. Maintain consistency across all translations

Translate each word accurately based on the full episode context."""

        return prompt

    def get_stats(self) -> Dict[str, any]:
        """Get API usage statistics"""
        return {
            "requestCount": self.request_count,
            "cacheSize": len(self.cache)
        }
