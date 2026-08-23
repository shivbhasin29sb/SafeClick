# 🛡️ SafeClick

SafeClick is a preventative anti-phishing tool built on a decoupled Client-Server architecture. It allows users to scan suspicious links and plain-text URLs directly from their browser without ever left-clicking or opening the malicious payload.

## 🚀 Features

* **"Right-Click, Don't Left-Click" Defense:** Natively injects a "Scan link with SafeClick" option into the Google Chrome context menu.
* **Text Selection Scanning:** Can analyze raw, unlinked URL text highlighted inside webmail clients (like Gmail or Outlook Web).
* **Independent Microservice Backend:** Powered by a Python Flask API running securely on a local server, completely isolated from the browser frontend.
* **Server-Side Rate Limiting:** The API is mathematically hardened against brute-force attacks using `flask-limiter`, capping requests strictly at the server level.
* **Custom Threat Heuristics:**
  * Detects insecure HTTP connections.
  * Flags high-risk social engineering phrasing (e.g., 'urgent', 'login', 'pay now').
  * Identifies suspicious IP address routing lacking real domain names.
  * **Targeted Spoofing Protection:** Includes a custom rule to detect fake university domains (specifically verifying official `chitkara.edu.in` links against spoofed Chitkara portals).

## 🛠️ Tech Stack

* **Frontend:** Google Chrome Extension (Manifest V3), JavaScript, HTML/CSS
* **Backend:** Python, Flask, Flask-CORS, Flask-Limiter
* **Version Control:** Git & GitHub

## ⚙️ How to Run Locally

### 1. Start the Engine (Backend)
1. Ensure Python 3 is installed.
2. Navigate to the project directory in your terminal.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the server:
   `python app.py`
5. The API will now be listening securely on `http://127.0.0.1:5000`.

### 2. Install the Extension (Frontend)
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked** in the top left corner.
4. Select the main `SafeClick` repository folder.
5. Highlight any URL or right-click any link on a webpage to generate a real-time Threat Score!