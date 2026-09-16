import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@Game_Station_1"

# بعداً file_id فایل APK را اینجا از Environment Variable می‌گیریم
APK_FILE_ID = os.getenv("APK_FILE_ID")

# -------------------------
# پورت Render
# -------------------------

web = Flask(__name__)

@web.route("/")
def home():
    return "Long Drive Game Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)


# -------------------------
# /start
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 عضویت در کانال",
                url="https://t.me/Game_Station_1"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ بررسی عضویت",
                callback_data="check"
            )
        ]
    ]

    await update.message.reply_text(
        "🎮 سلام!\n\n"
        "برای دریافت بازی Long Drive ابتدا در کانال عضو شو.\n\n"
        "بعد از عضویت روی «بررسی عضویت» بزن 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# -------------------------
# دریافت APK
# -------------------------

async def receive_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document:
        return

    filename = document.file_name or ""

    if filename.lower().endswith(".apk"):

        file_id = document.file_id

        print("\n==============================")
        print("APK RECEIVED")
        print("FILE NAME:", filename)
        print("FILE ID:", file_id)
        print("==============================\n")

        await update.message.reply_text(
            "✅ فایل APK دریافت شد.\n\n"
            "File ID در Logs ربات نمایش داده شد."
        )

    else:
        await update.message.reply_text(
            "❌ لطفاً فقط فایل APK ارسال کن."
        )


# -------------------------
# بررسی عضویت
# -------------------------

async def check_membership(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL,
            user_id=user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:

            if APK_FILE_ID:

                await query.message.reply_document(
                    document=APK_FILE_ID,
                    caption="🎮 بازی Long Drive\n\n"
                            "عضویت شما تأیید شد ✅"
                )

            else:

                await query.message.reply_text(
                    "✅ عضویت شما تأیید شد!\n\n"
                    "⚠️ فایل APK هنوز به ربات اضافه نشده."
                )

        else:

            await query.message.reply_text(
                "❌ هنوز عضو کانال نیستی.\n\n"
                "اول عضو کانال شو و دوباره بررسی کن."
            )

    except Exception as error:

        print("Membership error:", error)

        await query.message.reply_text(
            "⚠️ خطا در بررسی عضویت.\n"
            "مطمئن شو ربات در کانال ادمین است."
        )


# -------------------------
# اجرای ربات
# -------------------------

def main():

    if not TOKEN:
        raise ValueError(
            "BOT_TOKEN تنظیم نشده است."
        )

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(
            check_membership,
            pattern="^check$"
        )
    )

    # دریافت فایل‌های APK
    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            receive_apk
        )
    )

    print(
        "🤖 Long Drive Game Bot is running..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()
