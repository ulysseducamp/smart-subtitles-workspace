"""
OpenAI API integration for context-aware translation
Supports both OpenAI models (GPT-4.1 Nano) and Google Gemini models (2.0 Flash)
Uses Structured Outputs for guaranteed JSON reliability
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
from openai import OpenAI
import logging
import time

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
    LLM-based translator supporting both OpenAI and Google Gemini models
    Uses Structured Outputs for reliable JSON parsing
    Supports local context (one subtitle per word) for contextual translation
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-nano-2025-04-14",
        timeout: float = 90.0,
        base_url: Optional[str] = None
    ):
        """
        Initialize LLM translator (OpenAI or Gemini)

        Args:
            api_key: API key (OpenAI or Google Gemini)
            model: Model to use (default: gpt-4.1-nano-2025-04-14)
                   For Gemini: use "gemini-2.0-flash" with base_url
            timeout: Request timeout in seconds (default: 90.0)
            base_url: Optional base URL for API endpoint
                      For Gemini: "https://generativelanguage.googleapis.com/v1beta/openai/"
                      For OpenAI: None (uses default)
        """
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
            logger.info(f"✅ LLM Translator initialized with custom base_url: {base_url}")
        else:
            self.client = OpenAI(api_key=api_key, timeout=timeout)
            logger.info(f"✅ LLM Translator initialized with OpenAI endpoint")

        self.model = model
        self.base_url = base_url
        self.cache = {}
        self.request_count = 0

        logger.info(f"   Model: {model}")

    def translate_batch_with_context(
        self,
        word_contexts: Dict[str, str],
        words_to_translate: List[str],
        source_lang: str,
        target_lang: str
    ) -> Dict[str, str]:
        """
        Translate multiple words with LOCAL context (one subtitle per word) in a single API call

        Args:
            word_contexts: Dictionary mapping each word to the subtitle text where it appears
            words_to_translate: List of words to translate
            source_lang: Source language code (e.g., 'PT', 'EN')
            target_lang: Target language code (e.g., 'FR', 'EN')

        Returns:
            Dictionary mapping original words to translations
        """
        # ⏱️ Start global timing
        start_time_global = time.time()
        logger.info(f"🚀 [OPENAI] Starting translation batch")
        logger.info(f"   [OPENAI] Total words requested: {len(words_to_translate)}")

        if not words_to_translate:
            logger.info(f"   [OPENAI] No words to translate, returning empty dict")
            return {}

        # ⏱️ Cache check timing
        start_cache_check = time.time()
        cache_key_prefix = f"{source_lang}_{target_lang}_"
        cached_translations = {}
        uncached_words = []

        for word in words_to_translate:
            cache_key = f"{cache_key_prefix}{word}"
            if cache_key in self.cache:
                cached_translations[word] = self.cache[cache_key]
            else:
                uncached_words.append(word)

        cache_check_duration = time.time() - start_cache_check
        logger.info(f"   [OPENAI] Cache check completed in {cache_check_duration:.3f}s")
        logger.info(f"   [OPENAI] Cached: {len(cached_translations)} words, Uncached: {len(uncached_words)} words")

        # If all words are cached, return immediately
        if not uncached_words:
            total_duration = time.time() - start_time_global
            logger.info(f"✅ [OPENAI] All {len(words_to_translate)} words found in cache (total: {total_duration:.3f}s)")
            return cached_translations

        logger.info(f"🔄 [OPENAI] Translating {len(uncached_words)} words with GPT-4o mini")
        logger.info(f"   [OPENAI] Using LOCAL context: {len(word_contexts)} words with individual subtitle contexts")
        logger.info(f"   [OPENAI] Words to translate: {', '.join(uncached_words[:10])}{'...' if len(uncached_words) > 10 else ''}")

        try:
            # ⏱️ Prompt building timing
            start_prompt_build = time.time()
            prompt = self._build_translation_prompt(
                word_contexts=word_contexts,
                words_to_translate=uncached_words,
                source_lang=source_lang,
                target_lang=target_lang
            )
            prompt_build_duration = time.time() - start_prompt_build
            logger.info(f"   [OPENAI] Prompt built in {prompt_build_duration:.3f}s (length: {len(prompt)} chars)")

            # ⏱️ API call timing
            logger.info(f"   [OPENAI] Sending API request to OpenAI...")
            start_api_call = time.time()

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

            api_call_duration = time.time() - start_api_call
            logger.info(f"   [OPENAI] ✅ API response received in {api_call_duration:.3f}s")

            # ⏱️ Response parsing timing
            start_parsing = time.time()
            parsed_data = response.choices[0].message.parsed
            new_translations = {
                item.word: item.translation
                for item in parsed_data.translations
            }
            parsing_duration = time.time() - start_parsing
            logger.info(f"   [OPENAI] Response parsed in {parsing_duration:.3f}s")

            # ⏱️ Cache update timing
            start_cache_update = time.time()
            for word, translation in new_translations.items():
                cache_key = f"{cache_key_prefix}{word}"
                self.cache[cache_key] = translation
            cache_update_duration = time.time() - start_cache_update
            logger.info(f"   [OPENAI] Cache updated in {cache_update_duration:.3f}s")

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

            # ⏱️ Total timing
            total_duration = time.time() - start_time_global

            logger.info(f"✅ [OPENAI] Translation successful!")
            logger.info(f"   [OPENAI] Words translated: {len(new_translations)} (cached: {len(cached_translations)})")
            logger.info(f"   [OPENAI] Tokens: {input_tokens} input + {output_tokens} output = {total_tokens} total")
            logger.info(f"   [OPENAI] Cost: ${cost:.6f}")
            logger.info(f"   [OPENAI] ⏱️ TIMING BREAKDOWN:")
            logger.info(f"      - Cache check: {cache_check_duration:.3f}s")
            logger.info(f"      - Prompt build: {prompt_build_duration:.3f}s")
            logger.info(f"      - API call: {api_call_duration:.3f}s ⚡")
            logger.info(f"      - Response parsing: {parsing_duration:.3f}s")
            logger.info(f"      - Cache update: {cache_update_duration:.3f}s")
            logger.info(f"      - TOTAL: {total_duration:.3f}s")

            return all_translations

        except Exception as e:
            total_duration = time.time() - start_time_global
            logger.error(f"❌ [OPENAI] Translation failed after {total_duration:.3f}s: {e}")
            raise  # Re-raise to allow fallback handling

    def _build_translation_prompt(
        self,
        word_contexts: Dict[str, str],
        words_to_translate: List[str],
        source_lang: str,
        target_lang: str
    ) -> str:
        """Build optimized translation prompt with LOCAL context (one subtitle per word)"""

        source_name = LANGUAGE_NAMES.get(source_lang.upper(), source_lang)
        target_name = LANGUAGE_NAMES.get(target_lang.upper(), target_lang)

        # Build context list showing each word with its subtitle
        context_lines = []
        for word in words_to_translate:
            if word in word_contexts:
                context_lines.append(f'- "{word}" appears in: "{word_contexts[word]}"')
            else:
                context_lines.append(f'- "{word}" (no context available)')

        contexts_section = "\n".join(context_lines)

        prompt = f"""You are translating subtitles for a language learning application.

TASK: Translate {len(words_to_translate)} {source_name} words to {target_name}.

WORD CONTEXTS (each word with its subtitle):
{contexts_section}

TRANSLATION RULES:
1. Use the subtitle context to understand how the word is used
2. Provide natural translations as a native speaker would say
3. Keep translations concise (1-3 words maximum)
4. Consider the specific context where each word appears
5. Maintain consistency across all translations

Translate each word accurately based on its subtitle context."""

        return prompt

    def get_stats(self) -> Dict[str, any]:
        """Get API usage statistics"""
        return {
            "requestCount": self.request_count,
            "cacheSize": len(self.cache)
        }
