from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def analyze_threat(text):
    reasons = []
    score = 0

    url_match = re.search(r'https?://[^\s]+', text)
    url = url_match.group(0) if url_match else ""
    
    if 'urgent' in text.lower():
        score += 20
        reasons.append({"tag": "⚠️", "text": "Contains high-risk phishing phrasing: 'urgent'"})

    if url:
        if url.startswith('http://'):
            score += 30
            reasons.append({"tag": "🚨", "text": "Insecure connection (HTTP instead of encrypted HTTPS)"})
    
    return {
        "risk_score": score,  
        "url": url,           
        "reasons": reasons if reasons else [{"tag": "✅", "text": "Standard link format detected."}]
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