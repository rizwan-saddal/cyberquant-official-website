import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

# --- Configuration ---
# Get API Key from Environment Variable (Best Practice)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not set in environment variables.")

# --- API Routes ---

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if not GEMINI_API_KEY:
        return jsonify({"error": "Server configuration error: API Key missing"}), 500

    try:
        data = request.json
        prompt = data.get('prompt')
        history = data.get('history', [])
        
        if not prompt:
             return jsonify({"error": "Prompt is required"}), 400

        # Initialize Model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convert history to Gemini format (optional, simplified here)
        # We start a new chat for simplicity or reconstruction
        chat = model.startChat(history=history)
        
        response = chat.send_message(prompt)
        return jsonify({"text": response.text})

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return jsonify({"error": str(e)}), 500

# --- Static File Serving (Fallback/Local) ---
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Run locally
    app.run(host='0.0.0.0', port=8080, debug=True)
