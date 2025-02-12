from abc import ABC, abstractmethod

from server.models import LanguageEnum


class TextTranslator(ABC):
    @abstractmethod
    async def translate_text(self, text: str, target_language: LanguageEnum = LanguageEnum.EN) -> str:
        """Translates the extracted text into the target language."""
        ...
