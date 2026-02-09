from flask import Flask, request, jsonify
import logging
from config import SERVER_HOST, SERVER_PORT, WHATSAPP_API_KEY
from whatsapp_handler import handle_whatsapp_webhook, send_linking_code_to_whatsapp
from database import Database

app = Flask(__name__)
db = Database()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """نقطة نهاية الـ Webhook للواتساب"""
    if request.method == 'GET':
        # التحقق من الـ token
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if token == WHATSAPP_API_KEY:
            return challenge
        return 'Invalid token', 403
    
    elif request.method == 'POST':
        data = request.get_json()
        handle_whatsapp_webhook(data)
        return jsonify({"status": "ok"}), 200

@app.route('/health', methods=['GET'])
def health():
    """فحص صحة السيرفر"""
    return jsonify({"status": "running"}), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """الحصول على قائمة المستخدمين المرتبطين"""
    conn = db.db_path
    # عرض المستخدمين
    return jsonify({"message": "قائمة المستخدمين"}), 200

def run():
    """تشغيل السيرفر"""
    logger.info(f"السيرفر يعمل على {SERVER_HOST}:{SERVER_PORT}")
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)

if __name__ == '__main__':
    run()