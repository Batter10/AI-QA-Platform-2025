import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from langdetect import detect
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('qa_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS qa_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  document_name TEXT,
                  question TEXT,
                  answer TEXT,
                  language TEXT,
                  model TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Initialize AI models
models = {
    'llama': pipeline('question-answering', model='meta-llama/Llama-2-7b-chat-hf'),
    'deepseek': pipeline('question-answering', model='deepseek-ai/deepseek-llm-7b-chat')
}

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'en'  # Default to English if detection fails

def log_qa(document_name, question, answer, language, model):
    conn = sqlite3.connect('qa_history.db')
    c = conn.cursor()
    c.execute('''INSERT INTO qa_logs (document_name, question, answer, language, model)
                 VALUES (?, ?, ?, ?, ?)''',
              (document_name, question, answer, language, model))
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save the file temporarily
        upload_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(upload_path)
        
        return jsonify({'message': 'File uploaded successfully',
                       'filename': file.filename}), 200
    
    except Exception as e:
        logger.error(f"Error in upload_document: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question')
        document_name = data.get('document_name')
        model_name = data.get('model', 'llama').lower()
        
        if not all([question, document_name]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Detect question language
        language = detect_language(question)
        
        # Load document content
        with open(os.path.join('uploads', document_name), 'r') as f:
            context = f.read()
        
        # Get answer from selected model
        model = models.get(model_name)
        if not model:
            return jsonify({'error': 'Invalid model selection'}), 400
        
        result = model(question=question, context=context)
        answer = result['answer']
        
        # Log the Q&A
        log_qa(document_name, question, answer, language, model_name)
        
        return jsonify({
            'answer': answer,
            'language': language,
            'model': model_name
        }), 200
    
    except Exception as e:
        logger.error(f"Error in ask_question: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)