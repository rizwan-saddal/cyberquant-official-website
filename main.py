import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

# --- Configuration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
CONTACT_RECIPIENT = "yasir@perpetualworks.net"
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

# --- API Routes ---

@app.route('/api/contact', methods=['POST'])
def contact():
    """Receive contact form submission and email it to the business."""
    try:
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        source = data.get('source', 'website')

        if not name or not email:
            return jsonify({"error": "Name and email are required."}), 400

        # Build email
        subject = f"[CyberQuant] New Contact Request from {name}"
        body_html = f"""
        <html>
        <body style="font-family:Arial,sans-serif;color:#333;">
            <h2 style="color:#0ea5e9;">New Contact Form Submission</h2>
            <table style="border-collapse:collapse;width:100%;max-width:500px;">
                <tr><td style="padding:8px;font-weight:bold;">Name:</td><td style="padding:8px;">{name}</td></tr>
                <tr><td style="padding:8px;font-weight:bold;">Email:</td><td style="padding:8px;"><a href="mailto:{email}">{email}</a></td></tr>
                <tr><td style="padding:8px;font-weight:bold;">Source:</td><td style="padding:8px;">{source}</td></tr>
            </table>
            <p style="margin-top:20px;font-size:12px;color:#999;">Sent automatically from cyberquant.io</p>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER or f"noreply@cyberquant.io"
        msg["To"] = CONTACT_RECIPIENT
        msg["Reply-To"] = email
        msg.attach(MIMEText(body_html, "html"))

        if SMTP_USER and SMTP_PASS:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(msg["From"], [CONTACT_RECIPIENT], msg.as_string())
        else:
            # Log the submission when SMTP is not configured (dev/preview)
            print(f"[CONTACT] SMTP not configured. Name={name}, Email={email}, Source={source}")
            return jsonify({"success": True, "message": "Request received (email delivery pending SMTP configuration)."}), 200

        return jsonify({"success": True, "message": "Your request has been submitted successfully."}), 200

    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
        return jsonify({"error": "Failed to send email. Please try again later."}), 500
    except Exception as e:
        print(f"Contact form error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


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
