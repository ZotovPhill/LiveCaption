from abc import ABC, abstractmethod

from cv2.typing import MatLike
from PIL.Image import Image


class ScreenCaptionExtractor(ABC):
    @abstractmethod
    async def capture_screen(self, region: tuple[int, int, int, int] | None = None) -> Image | MatLike:
        """Captures a screenshot of the given region."""
        ...

    @abstractmethod
    async def extract_text_from_image(self, image: Image | MatLike) -> str:
        """Extracts text from the given image using Tesseract OCR."""
        ...
