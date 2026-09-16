import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# تنظیمات ربات
# =========================

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL = "@Game_Station_1"


# =========================
# دستور /start
# =========================

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

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎮 سلام!\n\n"
        "برای دریافت فایل بازی Long Drive ابتدا در کانال عضو شو.\n\n"
        "بعد از عضویت روی «بررسی عضویت» بزن 👇",
        reply_markup=reply_markup
    )


# =========================
# بررسی عضویت
# =========================

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                "✅ عضویت شما تأیید شد!\n\n"
                "🎮 فایل بازی Long Drive به‌زودی ارسال می‌شود."
            )

            # فعلاً اینجا فایل APK را اضافه می‌کنیم
            # بعداً روش ارسال APK را قرار می‌دهیم.

        else:
            await query.message.reply_text(
                "❌ هنوز عضو کانال نیستی!\n\n"
                "اول عضو کانال شو و دوباره «بررسی عضویت» رو بزن."
            )

    except Exception:
        await query.message.reply_text(
            "⚠️ نتونستم عضویت رو بررسی کنم.\n"
            "مطمئن شو ربات در کانال ادمین است."
        )


# =========================
# اجرای ربات
# =========================

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_membership, pattern="^check$"))

    print("🤖 Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
