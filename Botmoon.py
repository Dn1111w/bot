from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.ext import MessageHandler, filters

# کانال‌های شما (باید درست پر کنید)
CHANNELS = ["@dntxt", "@anamoon2007"]

WELCOME_TEXT = """
🎧 خوش اومدی به آرشیو رسمی آهنگ‌های من! 🎶

✨ اینجا جاییه که می‌تونی مستقیم و بدون واسطه، همه‌ی ترک‌هامو بشنوی یا دانلود کنی.

🔥 فقط موزیک‌های خودم اینجاست — خالص، بی‌سانسور و مستقیم از دلِ من 🎙️

👇 از دکمه‌های زیر یکی رو بزن و وارد دنیای صدام شو:

🎵 با عشق ساخته شده، با تو شنیده میشه 💖
"""

SONGS = {
    "song_0": ("🎵 لێرە نیت", "CQACAgQAAxkBAAMdaDtmtUBQMSZtB9V-mc_BTmeBGcEAAx0AArMd4VEaFavEb6uGAzYE"),
    "song_1": ("🎵 ئەگەر هاتیتەو", "CQACAgIAAxkBAAMoaDto7gPVi8tB3wzFzKAEVWY2X0EAAr1yAAKHVsFJH21Fm-M08qo2BA"),
    "song_3": ("🎵 ئەگەر هاتیتەو ئێدامە", "CQACAgIAAxkBAAM4aDtrrO2TZSZAb23nrQHYyJaU0u8AAr9yAAKHVsFJYdBjkWASmhg2BA"),
    "song_2": ("🎵 تورا نبخشیدم", "CQACAgIAAxkBAAMkaDto7udca4dbVM8q0yfdYNuG9OoAAoR6AALIOLlJYsgNmK7W-sY2BA"),
    "song_3": ("🎵 خداحافظ", "CQACAgIAAxkBAAM2aDtqPE2Tu-2TEzWGrZN4KxdXX28AArRyAAKHVsFJv8vM_fg_wtk2BA"),
    "song_4": ("🎵 خاموش", "CQACAgIAAxkBAAMnaDto7qDNKHxKl0cx26A29dl2rsUAArlyAAKHVsFJe_1z72_aRGI2BA"),
    "song_6": ("🎵 Bukê", "CQACAgIAAxkBAAMpaDto7lM78JHZCxQwCTGd2v3vmxEAAsJyAAKHVsFJDSIfNnr7pAs2BA"),
    "song_7": ("🎵 بێ دەنگ بێ باکانە", "CQACAgQAAxkBAAM-aDtyVpqFAAG2TslvzLX-csszWkAMAAIrHQACsx3hUfGLegkuH0kSNgQ"),
    "song_8": ("🎵 پیری مەیخانە", "CQACAgQAAxkBAANAaDtzBcIcWuurShifGaXaPL7xJo8AAiwdAAKzHeFRZQORmS1VXzQ2BA"),
    "song_9": ("🎵 عربی", "CQACAgQAAxkBAAM8aDtx-injgeCxK9W5jCX-58ZFZowAAiodAAKzHeFR_JoBBFGssOM2BA"),
    "song_10": ("🎵 ته‌مه‌ن", "CQACAgQAAxkBAANEaDtz6lchTzZX3iheddCcRowtB3AAAi4dAAKzHeFRA7pIciI4tjY2BA"),
    "song_11": ("🎵 بارون", "CQACAgQAAxkBAANCaDtzpbCHu90gsS60q4zQQk90Fz0AAi0dAAKzHeFRckNwoJmGtX02BA"),
    "song_12": ("🎵 مگه میگذره ادم از اونی که زندگیشه", "CQACAgQAAxkBAANIaDt1Oi7Oa2SZ7FtEOL0c035ilrkAAjEdAAKzHeFR12ID_IJOQkk2BA"),
    "song_13": ("🎵 لێم ببوره", "CQACAgQAAxkBAANGaDt0YpA9S68WGKFxC0ZVg4lVDbgAAjAdAAKzHeFRuelud8ibK642BA"),
    "song_14": ("🎵 آب از سرو", "CQACAgIAAxkBAAMlaDto7tDxN86AZ61YCxUI1AWmcXgAAod6AALIOLlJlSus8N5s0eU2BA"),
}

async def is_user_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_member(update, context):
        keyboard = [
            [InlineKeyboardButton("کانال  1  📥" , url=f"https://t.me/{CHANNELS[0][1:]}")],
            [InlineKeyboardButton("کانال  2  📥", url=f"https://t.me/{CHANNELS[1][1:]}")],
            [InlineKeyboardButton("تایید عضویت ✅", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            " لطفا اول عضو کانال‌های ما شو تا بتونی از ربات استفاده کنی.\n"
            "برای ادامه، روی دکمه تایید عضویت بزن تا وضعیت عضویتت چک بشه.",
            reply_markup=reply_markup
        )
        return

    keyboard = []
    for key, (label, _) in SONGS.items():
        keyboard.append([InlineKeyboardButton(label, callback_data=key)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

# کد گرفتن file_id آهنگ
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = update.message.audio
    if audio:
        await update.message.reply_text(f"🎧 file_id این آهنگ:\n`{audio.file_id}`", parse_mode="Markdown")



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check_membership":
        if await is_user_member(update, context):
            keyboard = []
            for key, (label, _) in SONGS.items():
                keyboard.append([InlineKeyboardButton(label, callback_data=key)])
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.message.edit_text(WELCOME_TEXT, reply_markup=reply_markup)
        else:
            await query.message.answer(
                "❌ هنوز عضو کانال‌ها نیستی.\nلطفا ابتدا عضو شو و سپس تایید کن."
            )
    else:
        data = query.data
        if data in SONGS:
            title, file_id = SONGS[data]
            await query.message.reply_audio(audio=file_id, caption=title)
        else:
            await query.message.reply_text("⚠️ آهنگ پیدا نشد!")

if __name__ == "__main__":
    TOKEN = "7974362441:AAElQCA8RBqr8CVR_7uOujW5TcZxsqBlsik"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))

    print("Bot is running...")
    app.run_polling()
