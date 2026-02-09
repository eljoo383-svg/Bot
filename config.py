import os
from dotenv import load_dotenv

load_dotenv()

# توكن البوت التلجرام
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# الخاص بـ WhatsApp
WHATSAPP_API_KEY = os.getenv('WHATSAPP_API_KEY')
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')

# الخادم
SERVER_HOST = '0.0.0.0'
SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))

# قاعدة البيانات
DATABASE_PATH = os.getenv('DATABASE_PATH', 'users.db')

# رموز الربط (صلاحية الاستخدام)
LINKING_CODES = {}  # {code: {phone: xxx, timestamp: xxx}}
LINKING_CODE_LENGTH = 6
LINKING_CODE_EXPIRY = 300  # 5 دقائق