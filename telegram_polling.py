import logging
import random
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN, LINKING_CODE_LENGTH, LINKING_CODE_EXPIRY
from database import Database
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبا! 👋\n\n"
        "أنا بوت ربط الواتساب. استخدمني لربط حسابك.\n\n"
        "الأوامر المتاحة:\n"
        "/link - لربط الواتساب\n"
        "/verify - للتحقق من الكود\n"
        "/status - لحالتك الحالية"
    )

async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    await update.message.reply_text(
        "برجاء أرسل رقم هاتفك (بصيغة دولية مثل: +201234567890)\n"
        "في سطر واحد فقط:"
    )
    
    context.user_data['waiting_for_phone'] = True

async def handle_phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('waiting_for_phone'):
        return
    
    user_id = update.effective_user.id
    phone_number = update.message.text.strip()
    
    if not phone_number.startswith('+') or not phone_number[1:].isdigit():
        await update.message.reply_text("❌ صيغة الرقم خاطئة. استخدم الصيغة: +201234567890")
        return
    
    linking_code = ''.join(random.choices(string.digits, k=LINKING_CODE_LENGTH))
    
    db.save_linking_code(linking_code, user_id, phone_number, int(time.time()))
    
    context.user_data['waiting_for_phone'] = False
    context.user_data['phone_number'] = phone_number
    context.user_data['linking_code'] = linking_code
    
    await update.message.reply_text(
        f"✅ تم توليد كود الربط!\n\n"
        f"📱 رقمك: {phone_number}\n"
        f"🔐 كودك: `{{linking_code}}`\n\n"
        f"⏰ الكود صالح لمدة 5 دقائق فقط\n\n"
        f"الآن قم بتقديم هذا الكود في تطبيق الواتساب للتحقق.",
        parse_mode="Markdown"
    )

async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('linking_code'):
        await update.message.reply_text("❌ لم تطلب كود ربط بعد. استخدم /link أولاً")
        return
    
    await update.message.reply_text("أرسل الكود الذي استقبلته على الواتساب:")
    context.user_data['waiting_for_code'] = True

async def handle_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('waiting_for_code'):
        return
    
    user_id = update.effective_user.id
    received_code = update.message.text.strip()
    original_code = context.user_data.get('linking_code')
    
    if received_code == original_code:
        db.link_user(user_id, context.user_data['phone_number'])
        await update.message.reply_text("✅ تم ربط الواتساب بنجاح! الآن يمكنك استقبال الرسائل.")
        context.user_data['waiting_for_code'] = False
    else:
        await update.message.reply_text("❌ الكود خاطئ. حاول مجدداً.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    status = db.get_user_status(user_id)
    
    if status['linked']:
        await update.message.reply_text(
            f"✅ حالتك: مرتبط\n"
            f"📱 رقمك: {status['phone']}"
        )
    else:
        await update.message.reply_text("❌ حالتك: غير مرتبط. استخدم /link للربط")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("link", link_command))
    app.add_handler(CommandHandler("verify", verify_command))
    app.add_handler(CommandHandler("status", status_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_input))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code_input))
    
    logger.info("✅ بوت التليجرام بدأ التشغيل...")
    app.run_polling()

if __name__ == '__main__':
    main()