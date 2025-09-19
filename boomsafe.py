from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import re
import asyncio

# Predefined seed format (64-character hexadecimal)
SEED_PATTERN = r"^[a-f0-9]{64}$"

# Mini-App URL
MINI_APP_URL = "https://boommini.vercel.app/"

# Access Keys
ACCESS_KEY_1 = "83fa2c20mxlp9zr0k"
ACCESS_KEY_2 = "9g3b2c7d5g6e2j9g"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗠𝗘𝗦𝗔𝗚𝗘"""
    await update.message.reply_text(
        "WELCOME TO Dr .Stake (Free BOT)\n\n"
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

    # Create mine selection buttons (1–24)
    buttons = []
    for i in range(1, 25):
        buttons.append(InlineKeyboardButton(f"{i} [𝗩𝗜𝗣]💣", callback_data=f"mines_{i}"))

    # Split buttons into rows of 3
    keyboard = [buttons[i:i+3] for i in range(0, len(buttons), 3)]

    await query.message.reply_text(
        "💣𝗦𝗘𝗟𝗘𝗖𝗧 𝗡𝗨𝗠𝗕𝗘𝗥 𝗢𝗙 𝗠𝗜𝗡𝗘𝗦⬇️:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- INDIVIDUAL MINE CALLBACKS ---------------- #

async def mine_selected(update: Update, context: ContextTypes.DEFAULT_TYPE, mine_number: int):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        f"✅ You selected **{mine_number} Mines**.\n\n"
        f"🔑 Use one of the access keys below to continue:\n\n"
        f"1. `{ACCESS_KEY_1}`\n"
        f"2. `{ACCESS_KEY_2}`\n\n"
        "Then open the mini-app below 👇",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Open Mini App", web_app=WebAppInfo(url=MINI_APP_URL))]
        ]),
        parse_mode="Markdown"
    )

# Create 24 separate handler functions
for i in range(1, 25):
    exec(f"""
async def mines_{i}(update, context):
    await mine_selected(update, context, {i})
""")


def main():
    app = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    # Start command
    app.add_handler(CommandHandler("start", start))

    # Begin process
    app.add_handler(CallbackQueryHandler(begin_process, pattern="begin_process"))

    # Add handlers for each mine (1–24)
    for i in range(1, 25):
        app.add_handler(CallbackQueryHandler(globals()[f"mines_{i}"], pattern=f"mines_{i}"))

    app.run_polling()


if __name__ == "__main__":
    main()
