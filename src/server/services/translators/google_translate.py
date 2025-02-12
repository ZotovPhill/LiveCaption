from typing import cast

from googletrans import Translator

from server.models import LanguageEnum
from server.services.mixins import AsyncExecutorMixin

from .base import TextTranslator


class GoogleTranslateTextTranslator(TextTranslator, AsyncExecutorMixin):
    def __init__(self, translator: Translator):
        self.translator = translator

    async def translate_text(self, text: str, target_language: LanguageEnum = LanguageEnum.EN) -> str:
        translated = await self._run_in_executor(self.translator.translate, text, target_language.value)
        return cast(str, translated.text) if translated.text is not None else ""
