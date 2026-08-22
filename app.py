from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re
app = Flask(__name__)
CORS(app)
def analyze_threat(text):
    reasons = []
    score = 0
    url_match = re.search(r'https?://[^\s]+', text)
    url = url_match.group(0).lower() if url_match else ""
    
    text_lower = text.lower()
    suspicious_keywords = ['urgent', 'pay now', 'verify', 'suspended', 'login']
    found_keywords = [word for word in suspicious_keywords if word in text_lower]
    
    if found_keywords:
        score += (20 * len(found_keywords))
        reasons.append({"tag": "⚠️", "text": f"Contains high-risk phrasing: {', '.join(found_keywords)}"})

    if url:
        if url.startswith('http://'):
            score += 30
            reasons.append({"tag": "🚨", "text": "Insecure connection (HTTP instead of encrypted HTTPS)"})
        if 'chitkara' in url and 'chitkara.edu.in' not in url:
            score += 50
            reasons.append({"tag": "🚨", "text": "WARNING: Spoofed university domain detected!"})

        if re.search(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            score += 40
            reasons.append({"tag": "🚨", "text": "Suspicious IP address routing (No real domain name)"})
        shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl']
        if any(shortener in url for shortener in shorteners):
            score += 25
            reasons.append({"tag": "⚠️", "text": "URL shortener detected (Destination is hidden)"})
            
    if score > 100:
        score = 100

    return {
        "risk_score": score,  
        "url": url,           
        "reasons": reasons if reasons else [{"tag": "✅", "text": "Standard link format detected. No immediate red flags."}]
    }

@app.route('/')
def home():
    return render_template('cypher.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json() or {}
    input_text = data.get('text', '')
    result = analyze_threat(input_text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)