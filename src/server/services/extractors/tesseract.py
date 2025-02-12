from typing import cast

import cv2
import numpy as np
import pyautogui
import pytesseract
from cv2.typing import MatLike
from PIL.Image import Image

from server.services.mixins import AsyncExecutorMixin

from .base import ScreenCaptionExtractor


class TesseractCaptionExtractor(ScreenCaptionExtractor, AsyncExecutorMixin):
    async def capture_screen(self, region: tuple[int, int, int, int] | None = None) -> MatLike:
        screenshot = await self._run_in_executor(pyautogui.screenshot, region)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    async def extract_text_from_image(self, image: Image | MatLike) -> str:
        text = await self._run_in_executor(pytesseract.image_to_string, image)
        return cast(str, text).strip()
