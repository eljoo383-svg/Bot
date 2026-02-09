from flask import Flask, request, jsonify
import logging
from config import SERVER_HOST, SERVER_PORT, WHATSAPP_API_KEY, TELEGRAM_BOT_TOKEN
from whatsapp_handler import handle_whatsapp_webhook
from database import Database
from telegram import Bot

app = Flask(__name__)
db = Database()
bot = Bot(token=TELEGRAM_BOT_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    """نقطة نهاية الـ Webhook للواتساب"""
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if token == WHATSAPP_API_KEY:
            return challenge
        return 'Invalid token', 403
    
    elif request.method == 'POST':
        data = request.get_json()
        handle_whatsapp_webhook(data)
        return jsonify({"status": "ok"}), 200

@app.route('/webhook/telegram', methods=['POST'])
def telegram_webhook():
    """نقطة نهاية الـ Webhook للتليجرام"""
    try:
        data = request.get_json()
        update = data
        logger.info(f"تليجرام: {update}")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"خطأ في الـ Webhook: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """فحص صحة السيرفر"""
    return jsonify({"status": "running"}), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """الحصول على قائمة المستخدمين المرتبطين"""
    return jsonify({"message": "قائمة المستخدمين"}), 200

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)