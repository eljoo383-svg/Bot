import threading
from telegram_bot import main as run_telegram_bot
from server import run as run_server
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """تشغيل البوت والسيرفر معاً"""
    
    # تشغيل السيرفر في thread منفصل
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    logger.info("✅ السيرفر بدأ التشغيل...")
    
    # تشغيل بوت التليجرام في thread الرئيسي
    logger.info("✅ بوت التليجرام بدأ التشغيل...")
    run_telegram_bot()

if __name__ == '__main__':
    main()