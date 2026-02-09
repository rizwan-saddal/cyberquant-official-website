import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

# --- Configuration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

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

        # Construct the payload for the REST API
        # The history from frontend is [{"role": "user", "parts": [...]}, ...]
        # We need to append the new prompt
        
        contents = history + [{"role": "user", "parts": [{"text": prompt}]}]
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": contents}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            error_msg = f"Gemini API Error: {response.text}"
            print(error_msg)
            return jsonify({"error": error_msg}), response.status_code
            
        response_json = response.json()
        
        # Extract text from response
        # Structure: candidates[0].content.parts[0].text
        try:
            text = response_json['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"text": text})
        except (KeyError, IndexError) as e:
            # Handle empty response (e.g., safety block)
            print(f"Error parsing Gemini response: {response_json}")
            return jsonify({"text": "I unable to generate a response for that prompt due to safety filters."})

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
