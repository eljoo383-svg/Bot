import requests
import logging
from config import WHATSAPP_API_KEY, WHATSAPP_PHONE_ID
from database import Database

logger = logging.getLogger(__name__)
db = Database()

WHATSAPP_API_URL = f"https://graph.instagram.com/v18.0/{WHATSAPP_PHONE_ID}/messages"

def send_linking_code_to_whatsapp(phone_number, linking_code):
    """إرسال كود الربط عبر الواتساب"""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number.replace('+', ''),
        "type": "template",
        "template": {
            "name": "linking_code",
            "language": {
                "code": "ar"
            },
            "parameters": {
                "body": {
                    "parameters": [linking_code]
                }
            }
        }
    }
    
    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
        logger.info(f"تم إرسال كود الربط: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"خطأ في إرسال الكود: {str(e)}")
        return False

def send_message_to_telegram(telegram_id, message):
    """إرسال رسالة من الواتساب إلى التليجرام"""
    # يتم تنفيذه عبر الـ Webhook
    pass

def handle_whatsapp_webhook(data):
    """معالجة رسائل الواتساب الواردة"""
    try:
        # استخراج البيانات من الـ Webhook
        message = data.get('messages', [{}])[0]
        phone_number = message.get('from')
        text = message.get('text', {}).get('body', '')
        
        # البحث عن المستخدم المرتبط
        conn = db.db_path
        # حفظ الرسالة في قاعدة البيانات
        logger.info(f"رسالة من {phone_number}: {text}")
        
        return True
    except Exception as e:
        logger.error(f"خطأ في معالجة الـ Webhook: {str(e)}")
        return False
