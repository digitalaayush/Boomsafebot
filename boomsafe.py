from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import re
import asyncio

# Predefined seed format (64-character hexadecimal)
SEED_PATTERN = r"^[a-f0-9]{64}$"

# Mini-App URL (Updated ✅)
MINI_APP_URL = "https://boommini.vercel.app/"

# Access Keys:
# Key 1: Displays a simple verification message.
# Key 2: Unlocks the Mini-App.
ACCESS_KEY_1 = "83fa2c20mxlp9zr0k"
ACCESS_KEY_2 = "9g3b2c7d5g6e2j9g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗠𝗘𝗦𝗔𝗚𝗘"""
    await update.message.reply_text(
        "WELCOME TO BOOMSAFE BOT\n\n"
        "𝗖𝗟𝗜𝗖𝗞 𝗧𝗛𝗘 𝗕𝗨𝗧𝗧𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 𝗧𝗢 𝗚𝗘𝗧 𝗦𝗧𝗔𝗥𝗧𝗘𝗗:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⏰𝗦𝗧𝗔𝗥𝗧", callback_data="begin_process")]
        ])
    )

async def begin_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """💣𝗦𝗘𝗟𝗘𝗖𝗧 𝗡𝗨𝗠𝗕𝗘𝗥 𝗢𝗙 𝗠𝗜𝗡𝗘𝗦⬇️"""
    query = update.callback_query
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(
        "💣𝗦𝗘𝗟𝗘𝗖𝗧 𝗡𝗨𝗠𝗕𝗘𝗥 𝗢𝗙 𝗠𝗜𝗡𝗘𝗦⬇️:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{i} [𝗩𝗜𝗣]💣", callback_data=f"mines_{i}")] for i in range(1, 11)
        ])
    )

async def select_mines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗬𝗢𝗨 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗠𝗜𝗡𝗘𝗦"""
    query = update.callback_query
    await query.answer()
    selected_mines = query.data.split("_")[1]
    await query.message.reply_text(
        f"𝗬𝗢𝗨 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 {selected_mines} [𝗩𝗜𝗣]💣\n\n"
        "𝗖𝗟𝗜𝗖𝗞 𝗧𝗛𝗘 𝗕𝗨𝗧𝗧𝗢𝗡 𝗕𝗘𝗟𝗢𝗪 𝗧𝗢 𝗖𝗢𝗡𝗧𝗜𝗡𝗨𝗘👇:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀𝗦𝗧𝗔𝗥𝗧", callback_data="start_process")]
        ])
    )

async def process_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗣𝗥𝗢𝗩𝗜𝗗𝗘 𝗬𝗢𝗨𝗥 𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗🪄"""
    query = update.callback_query
    await query.answer()
    await query.message.reply_photo(
        photo="https://i.imgur.com/r6nv6qp.jpg",
        caption="𝗙𝗜𝗡𝗗 𝗬𝗢𝗨𝗥 (𝗔𝗖𝗧𝗜𝗩𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗) 𝗮𝗻𝗱 𝗣𝗔𝗦𝗧𝗘 𝗜𝗧 𝗛𝗘𝗥𝗘: ⬇️⬇️",
        parse_mode="Markdown"
    )
    context.user_data['waiting_for_seed'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗛𝗔𝗡𝗗𝗟𝗘 𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗 𝗮𝗻𝗱 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬 𝗜𝗡𝗣𝗨𝗧"""
    if context.user_data.get('waiting_for_seed'):
        server_seed = update.message.text.strip()
        analyzing_message = await update.message.reply_text("🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗...", parse_mode="Markdown")
        animation_frames = ["🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚. ", "🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚.. ", "🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚... "]
        for _ in range(2):
            for frame in animation_frames:
                await asyncio.sleep(0.5)
                await analyzing_message.edit_text(frame, parse_mode="Markdown")
        await asyncio.sleep(1)
        if re.match(SEED_PATTERN, server_seed):
            await analyzing_message.edit_text("✅ 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗", parse_mode="Markdown")
            await asyncio.sleep(2)
            await analyzing_message.edit_text(
                "🔐 𝗘𝗡𝗧𝗘𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬 𝗢𝗥 𝗕𝗨𝗬 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔑𝗘𝗡𝗧𝗘𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬", callback_data="enter_access_key")],
                    [InlineKeyboardButton("👉𝗕𝗨𝗬 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬", web_app=WebAppInfo(url=MINI_APP_URL))]  # ✅ updated
                ])
            )
        else:
            await analyzing_message.edit_text("🚨𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗, 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡. /start", parse_mode="Markdown")
        context.user_data['waiting_for_seed'] = False

    elif context.user_data.get('awaiting_key'):
        key_entered = update.message.text.strip()
        context.user_data['awaiting_key'] = False
        if key_entered in (ACCESS_KEY_1, ACCESS_KEY_2):
            anim_msg = await update.message.reply_text("🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚 𝗬𝗢𝗨𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬...", parse_mode="Markdown")
            animation_frames = ["🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚. ", "🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚.. ", "🔍 𝗔𝗡𝗔𝗟𝗬𝗭𝗜𝗡𝗚... "]
            for _ in range(2):
                for frame in animation_frames:
                    await asyncio.sleep(0.5)
                    await anim_msg.edit_text(frame, parse_mode="Markdown")
            await asyncio.sleep(1)
            if key_entered == ACCESS_KEY_1:
                await anim_msg.edit_text("✅𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗. 𝗡𝗢𝗪 𝗚𝗢 𝗧𝗢 𝗦𝗧𝗔𝗞𝗘 & 𝗣𝗟𝗔𝗖𝗘 𝗔 𝗕𝗘𝗧🚀.", parse_mode="Markdown")
            else:
                await anim_msg.edit_text(
                    "✅𝗞𝗘𝗬 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗!\n\n🔗 𝗢𝗣𝗘𝗡𝗜𝗡𝗚 𝗠𝗜𝗡𝗜 𝗔𝗣𝗣...",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 𝗢𝗣𝗘𝗡 𝗠𝗜𝗡𝗜 𝗔𝗣𝗣", web_app=WebAppInfo(url=MINI_APP_URL))]
                    ])
                )
        else:
            msg = await update.message.reply_text("❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬, 𝗧𝗥𝗬 𝗔𝗚𝗔𝗜𝗡.", parse_mode="Markdown")
            await asyncio.sleep(1)
            await msg.delete()
            await update.message.reply_text(
                "🔑𝗣𝗟𝗘𝗔𝗦𝗘 𝗘𝗡𝗧𝗘𝗥 𝗬𝗢𝗨𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬 𝗛𝗘𝗥𝗘👇",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔑𝗘𝗡𝗧𝗘𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬", callback_data="enter_access_key")],
                    [InlineKeyboardButton("👉𝗕𝗨𝗬 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬", web_app=WebAppInfo(url=MINI_APP_URL))]  # ✅ updated
                ])
            )

async def wait_for_key_timeout(chat_id, message_id, context: ContextTypes.DEFAULT_TYPE):
    """If no access key is entered within 15 seconds, re-display the access key options."""
    await asyncio.sleep(15)
    if context.user_data.get("awaiting_key"):
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="🔑𝗣𝗟𝗘𝗔𝗦𝗘 𝗘𝗡𝗧𝗘𝗥 𝗬𝗢𝗨𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬 𝗛𝗘𝗥𝗘👇",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔑𝗘𝗡𝗧𝗘𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬", callback_data="enter_access_key")],
                    [InlineKeyboardButton("👉𝗕𝗨𝗬 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬", web_app=WebAppInfo(url=MINI_APP_URL))]  # ✅ updated
                ])
            )
        except Exception as e:
            print(e)

async def access_key_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the access key option callbacks."""
    query = update.callback_query
    await query.answer()
    if query.data == "enter_access_key":
        msg = await query.message.edit_text(
            "🔑𝗣𝗟𝗘𝗔𝗦𝗘 𝗘𝗡𝗧𝗘𝗥 𝗬𝗢𝗨𝗥 𝗔𝗖𝗖𝗘𝗦𝗦 𝗞𝗘𝗬 𝗛𝗘𝗥𝗘👇",
            parse_mode="Markdown"
        )
        context.user_data["awaiting_key"] = True
        asyncio.create_task(wait_for_key_timeout(query.message.chat_id, msg.message_id, context))

def main():
    """Run the bot."""
    application = ApplicationBuilder().token("7589471338:AAHveBfc0HyxSrkQ-dwWHhJx8RHyJMrNxYM").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(begin_process, pattern="^begin_process$"))
    application.add_handler(CallbackQueryHandler(select_mines, pattern="^mines_"))
    application.add_handler(CallbackQueryHandler(process_start_callback, pattern="^start_process$"))
    application.add_handler(CallbackQueryHandler(access_key_options, pattern="^enter_access_key$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
   
if __name__ == "__main__":
    main()
