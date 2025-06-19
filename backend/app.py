
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import threading
import time
from instagrapi import Client

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Instagram credentials
USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

# Store subscribers
subscribers = set()

# Login to Instagram
if not USERNAME or not PASSWORD:
    print("❌ Instagram login failed: IG_USERNAME or IG_PASSWORD missing from .env")
else:
    try:
        cl = Client()
        cl.login(USERNAME, PASSWORD)
        print("✅ Logged in to Instagram successfully")
    except Exception as e:
        print("❌ Instagram login failed:", e)

# Serve frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# PayPal webhook to store subscriber email
@app.route('/webhook/paypal', methods=['POST'])
def paypal_webhook():
    data = request.json
    payer_email = data.get('resource', {}).get('subscriber', {}).get('email_address')

    if payer_email:
        subscribers.add(payer_email)
        print(f"✅ New subscriber: {payer_email}")
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'failed'}), 400

# Check if email is subscribed
@app.route('/check-subscription', methods=['POST'])
def check_subscription():
    data = request.get_json()
    email = data.get('email')
    return jsonify({'access': 'granted' if email in subscribers else 'denied'})

# Instagram Auto-Post Function (basic version)
def auto_post_to_instagram():
    while True:
        try:
            caption = "🔥 Get roasted daily at https://yourdomain.com 🔥"
            media_path = "../frontend/roast.jpg"  # Replace with dynamic content path
            cl.photo_upload(media_path, caption)
            print("✅ Auto-posted to Instagram.")
        except Exception as e:
            print("❌ Auto-post failed:", e)
        time.sleep(3600 * 6)  # Every 6 hours

# Start auto-posting in background
threading.Thread(target=auto_post_to_instagram, daemon=True).start()

# Start Flask server
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
