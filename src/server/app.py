import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from googletrans import Translator

from server.handlers.caption_translator import CaptionTranslatorHandler
from server.models import LanguageEnum, Settings
from server.services.extractors import TesseractCaptionExtractor
from server.services.translators import GoogleTranslateTextTranslator

app: FastAPI = FastAPI()

# Set a default language in the app state (for instance, "en" for English)
app.state.language = LanguageEnum.EN.value

translator: Translator = Translator()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        extractor = TesseractCaptionExtractor()
        text_translator = GoogleTranslateTextTranslator(translator=translator)
        translator_service = CaptionTranslatorHandler(extractor=extractor, translator=text_translator)
        async for translated_text in translator_service.capture_and_translate(target_language=app.state.language):
            await websocket.send_text(translated_text)
    except WebSocketDisconnect:
        print("Client disconnected")


@app.post("/settings")
async def update_settings(settings: Settings) -> dict[str, str]:
    """Update the translation settings by changing the application's language."""

    app.state.language = settings.language
    return {"message": f"Language updated to {settings.language}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
