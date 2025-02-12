from asyncio import Future, get_running_loop
from typing import Any, AsyncGenerator, Callable, cast

import cv2
import numpy as np
import pyautogui
import pytesseract
from googletrans import Translator
from PIL.Image import Image

from server.models import LanguageEnum


class CaptionTranslator:
    def __init__(self, translator: Translator, language: LanguageEnum):
        self.translator = translator
        self.language = language

    async def capture_and_translate(self) -> AsyncGenerator[str, None]:
        """Capture Google Meet captions and translate them in real-time."""
        while True:
            frame = await self.capture_screen()
            extracted_text = await self.extract_text_from_image(frame)

            if extracted_text:
                yield await self.translate_text(extracted_text, target_language=self.language)

    async def capture_screen(self, region: tuple[int, int, int, int] | None = None) -> Image:
        """Captures a screenshot of the given region."""
        screenshot = await self._run_in_executor(pyautogui.screenshot, region)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    async def extract_text_from_image(self, image: Image) -> str:
        """Extracts text from the given image using Tesseract OCR."""
        text = await self._run_in_executor(pytesseract.image_to_string, image)
        return cast(str, text).strip()

    async def translate_text(self, text: str, target_language: LanguageEnum = LanguageEnum.EN) -> str:
        """Translates the extracted text into the target language."""
        translated = await self._run_in_executor(self.translator.translate, text, target_language.value)
        return cast(str, translated.text) if translated.text is not None else ""

    async def _run_in_executor(self, func: Callable[..., Any], *args: Any) -> Future[Any]:
        """Run a blocking function in an async executor."""
        return await get_running_loop().run_in_executor(None, func, *args)
