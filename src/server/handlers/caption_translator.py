from typing import AsyncGenerator

from server.models import LanguageEnum
from server.services.extractors import ScreenCaptionExtractor
from server.services.translators import TextTranslator


class CaptionTranslatorHandler:
    def __init__(self, extractor: ScreenCaptionExtractor, translator: TextTranslator):
        self.extractor = extractor
        self.translator = translator

    async def capture_and_translate(
        self,
        target_language: LanguageEnum = LanguageEnum.EN,
    ) -> AsyncGenerator[str, None]:
        while True:
            frame = await self.extractor.capture_screen()
            extracted_text = await self.extractor.extract_text_from_image(image=frame)
            if extracted_text:
                translated_text = await self.translator.translate_text(
                    text=extracted_text, target_language=target_language
                )
                yield translated_text
