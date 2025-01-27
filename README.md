# AI Q&A Platform

A multilingual document Q&A platform that uses state-of-the-art AI models (Llama and DeepSeek) to answer questions about uploaded documents. The platform supports automatic language detection and maintains a history of all Q&A interactions.

## Features

- Document upload and processing
- Support for multiple AI models (Llama and DeepSeek)
- Automatic language detection
- Real-time Q&A functionality
- History logging in SQLite database
- Responsive web interface
- Cross-browser compatibility

## Technical Stack

- Backend: Python with Flask
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- AI Models: Hugging Face Transformers
- Language Detection: langdetect

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Batter10/AI-QA-Platform-2025.git
cd AI-QA-Platform-2025
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python backend.py
```

4. Open index.html in your web browser

## Usage

1. Upload a document using the file upload button
2. Select your preferred AI model (Llama or DeepSeek)
3. Type your question in any language
4. Click "Ask Question" to get an answer

## API Endpoints

- POST `/upload`: Upload a document
- POST `/ask`: Ask a question about an uploaded document

## Testing

Test results are available in `test_results.txt`. The platform has been tested with:
- Multiple document formats
- Various languages
- Different browsers and devices
- Performance and load testing

## Screenshots

![Frontend Interface](screenshots/frontend.png)
![Test Results](screenshots/test_results.png)

## Development

A feature branch `feature/frontend-styling` is available with enhanced UI improvements. To contribute:

1. Create a new branch
2. Make your changes
3. Submit a pull request

## License

MIT License