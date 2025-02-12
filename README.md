# LIVE CAPTIONS

## Overview

Live Captions is a real-time captioning and translation application built using FastAPI. The application captures on-screen captions (for example, from a Google Meet session) using OCR (Tesseract) and translates the extracted text to a target language using the Google Translate API. A WebSocket endpoint streams the translated captions to connected clients in real time.

**Key Features:**
- Real-time screen capture and OCR text extraction using pyautogui, OpenCV, and pytesseract.
- Translation of extracted captions with Googletrans.
- Live updates through a WebSocket connection.
- Configurable target language via a REST endpoint.
- Containerization support with Docker.
- Pre-configured development environment with linting (Ruff), formatting, testing (pytest), and pre-commit hooks.

## Project Structure

```
live-captions/
├── .dockerfile                  # Docker configuration for building and running in production
├── .gitignore                   # Git ignore rules for Python, VSCode, etc.
├── .pre-commit-config.yaml      # Pre-commit hook configuration for code formatting and linting using Ruff
├── Makefile                     # Commands for installing dependencies, testing, linting, formatting, docker build, etc.
├── pyproject.toml               # Project meta-data, dependencies, and tool configuration (Uvicorn, Ruff, UV dev dependencies)
└── src/
    ├── client/
    │   └── websocket.js         # WebSocket client connecting to the server to receive translated captions
    └── server/
        ├── app.py               # Main FastAPI application with WebSocket and settings endpoints
        ├── models/              # Data models and enumerations
        │   ├── dtos/
        │   │   └── language.py  # Pydantic DTO for updating application settings
        │   └── enums/
        │       └── language.py  # Enumeration listing supported languages (EN, ES, FR, DE, RU)
        └── services/
            ├── caption_translator.py  # Service that handles screen capture, OCR text extraction, and translation
            └── __init__.py            # Exports the CaptionTranslator service
```

## Installation & Setup

1. **Prerequisites:**
   - Python 3.12 (or compatible)
   - pip (via uv pip in this project’s context)
   - Required tools:
     - uvicorn (ASGI server)
     - docker (if running in container)
     - ruff (for linting)
     - pytest (for testing)
     - pre-commit (for hooks)

2. **Clone the repository and navigate to the project directory:**
   ```
   git clone https://github.com/your-username/live-captions.git
   cd live-captions
   ```

3. **Install dependencies (production and development):**
   ```
   make install
   ```
   This command installs the project along with the extras required for development (linting, testing, etc.).

## Usage and Endpoints

### Starting the Server

Run the FastAPI application locally using Uvicorn:
```
make run
```
This will start the server on http://0.0.0.0:8000

### WebSocket Endpoint

**URL:** ws://localhost:8000/ws

Clients (e.g., the sample JavaScript client in src/client/websocket.js) can connect to this endpoint to receive a live stream of translated captions. For example, the client code:

```js
const socket = new WebSocket("ws://localhost:8000/ws");
socket.onmessage = (event) => console.log("Translated:", event.data);
```

### Updating Translation Settings

**Endpoint:** POST /settings

**Payload:**
```json
{
    "language": "en"  // Change "en" to any other supported language code (es, fr, de, ru)
}
```
This endpoint allows you to change the default target language for translation. The application state gets updated accordingly.

## Development Workflow

The project is set up with several helpful Makefile targets:

- `make check-tools` – Verifies that all required tools (ruff, uvicorn, docker, etc.) are installed.
- `make install` – Installs production and development dependencies.
- `make lint` – Runs linting on the codebase using Ruff.
- `make format` – Automatically fixes lint issues using Ruff’s formatting capabilities.
- `make test` – Executes the test suite with pytest.
- `make pre-commit` – Installs pre-commit hooks to enforce code quality.

Before committing your changes, ensure that you run pre-commit hooks:
```
make pre-commit
```

## Docker & Deployment

The Dockerfile is configured for both build and production stages. To build and run the container:

1. **Build the Docker image:**
   ```
   make build
   ```

2. **Run the Docker container:**
   ```
   make run-docker
   ```
   This exposes the application on port 8000. Adjust host and port configurations as needed.

## How It Works

### Caption Translator Service (src/server/services/caption_translator.py)

- Continuously captures screenshots from a designated screen region (default uses the full application screen via pyautogui).
- Converts the screenshot to grayscale for improved OCR performance.
- Uses pytesseract to extract text (captions) from the image.
- Translates the extracted text using the Google Translate API (via googletrans package) into the set target language.
- Streams the translated text through the WebSocket endpoint to connected clients.

Configuration is centralized in the FastAPI app state:
- Default language is set in the app state (initially “en” for English)
- The update /settings endpoint allows modifying this language dynamically.

## Contributing

Contributions are welcome! If you have improvements, bug fixes, or feature requests, please open an issue or submit a pull request.

Before committing:
- Ensure the code passes linting and all tests.
- Follow the pre-commit hooks to maintain a consistent code style.

## License

This project is licensed under the terms specified in the LICENSE file.

## Contact

For any questions or support, please contact:

Your Name <your.email@example.com>

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Googletrans Documentation](https://py-googletrans.readthedocs.io/)

Happy Coding!
