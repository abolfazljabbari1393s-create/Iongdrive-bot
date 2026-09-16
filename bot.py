import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@Game_Station_1"

# -------------------------
# پورت برای Render
# -------------------------

web = Flask(__name__)

@web.route("/")
def home():
    return "Long Drive Game Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)


# -------------------------
# دستور /start
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

        if member.status in ["member", "administrator", "creator"]:

            await query.message.reply_text(
                "✅ عضویت تأیید شد!\n\n"
                "🎮 حالا می‌توانیم فایل APK بازی را ارسال کنیم."
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
        raise ValueError("BOT_TOKEN تنظیم نشده است.")

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

    print("🤖 Long Drive Game Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
