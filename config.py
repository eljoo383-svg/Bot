import os
from dotenv import load_dotenv

load_dotenv()

# توكن البوت التلجرام
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# الخاص بـ WhatsApp
WHATSAPP_API_KEY = os.getenv('WHATSAPP_API_KEY')
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')

# Webhook URLs
TELEGRAM_WEBHOOK_URL = os.getenv('TELEGRAM_WEBHOOK_URL')  # مثل: https://yourdomain.katabump.com/webhook/telegram
WHATSAPP_WEBHOOK_URL = os.getenv('WHATSAPP_WEBHOOK_URL')  # مثل: https://yourdomain.katabump.com/webhook/whatsapp

# الخادم
SERVER_HOST = '0.0.0.0'
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))

# قاعدة البيانات
DATABASE_PATH = os.getenv('DATABASE_PATH', 'users.db')

# رموز الربط
LINKING_CODE_LENGTH = 6
LINKING_CODE_EXPIRY = 300  # 5 دقائق