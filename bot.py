import os
import asyncio
from aiohttp import web
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ChatMemberHandler, MessageHandler, filters, ContextTypes
import logging

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Bot Token environment variable se liya jayega
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")

# /start command handler (Photo, Updated buttons aur Caption ke sath)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = (
        "🤖 **Auto Reaction Bot**\n\n"
        "I Automatically React To Every New Post In Your Channel With Emojis.\n\n"
        "**How To Use:**\n"
        "→ 1. Make Me Admin In Your Channel\n"
        "→ 2. Post A Message In Your Channel"
    )

    # Updated buttons with correct links
    keyboard = [
        [
            InlineKeyboardButton("✚ 𝗔𝗱𝗱 𝗧𝗼 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", url="https://t.me/AayushReactionBot?startchannel=true&admin=post_messages+edit_messages+delete_messages+invite_users+manage_chat+change_info"),
            InlineKeyboardButton("✚ 𝗔𝗱𝗱 𝗧𝗼 𝗚𝗿𝗼𝘂𝗽", url="https://t.me/AayushReactionBot?startgroup=true&admin=post_messages+edit_messages+delete_messages+invite_users+manage_chat+change_info")
        ],
        [
            InlineKeyboardButton("👤 𝗢𝘄𝗻𝗲𝗿", url="https://t.me/aayushjindal32")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # photo.jpg file ke sath message bhejne ke liye
        with open("photo.jpg", "rb") as photo_file:
            await update.message.reply_photo(
                photo=photo_file,
                caption=start_text,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Photo load karne mein error aayi: {e}")
        # Agar photo na mile toh fallback keval text bhej dega
        await update.message.reply_text(
            text=start_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# 1. Join Request aane par APPROVE NAHI HOGA, sirf user ko welcome message aur button jayega
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_join_request = update.chat_join_request
    if chat_join_request:
        user_id = chat_join_request.from_user.id
        first_name = chat_join_request.from_user.first_name
        chat_id = chat_join_request.chat.id

        try:
            welcome_message = (
                f"✅ **Hello {first_name}** 🎉\n"
                f"**You Are A PremiuM UseR Now 🧡**\n\n"
                f"Loss Recovery :- Join Now\n\n"
                f"Join Here 📌 (EXPIRE IN 5 MINUTES)"
            )

            keyboard = [
                [InlineKeyboardButton("📌 Join Channel Now", url="https://t.me/+g6b-NJx0d8BhMjU1")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # User ko personal message bheja jayega bina request approve kiye
            await context.bot.send_message(
                chat_id=user_id, 
                text=welcome_message, 
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            print(f"Sent welcome message to user {first_name} for join request in channel ID: {chat_id}")
            
        except Exception as e:
            print(f"Error sending welcome message on join request: {e}")

# 2. Bot jis bhi channel mein admin ho, wahan nayi post par Auto-Reaction (❤️) dena
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    if message:
        try:
            await message.set_reaction(reaction=ReactionTypeEmoji("❤️"))
            print(f"Reaction sent to post ID {message.message_id} in channel ID: {message.chat.id}")
        except Exception as e:
            print(f"Error sending reaction: {e}")

# Render ke liye Dummy Web Server
async def handle(request):
    return web.Response(text="Multi-channel bot is running 24x7!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers add karein (Auto-approve function yahan se hata diya gaya hai)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))

    print("Multi-channel bot start ho raha hai...")
    
    # Web server aur bot dono ko ek sath start karein
    await start_web_server()
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Bot ko band hone se bachane ke liye infinite event loop
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
