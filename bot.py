import os
import asyncio
from aiohttp import web
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, filters, ContextTypes
import logging

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Sirf Bot Token ki zarurat hai
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")

# 1. Kisi bhi channel par Join Request aane par approve karke stylish welcome message aur button bhejna
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.chat_join_request.from_user.id
    chat_id = update.chat_join_request.chat.id
    first_name = update.chat_join_request.from_user.first_name

    try:
        # Join request approve karein
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
        
        # Screenshot ke jaisa exact message text
        welcome_message = (
            f"✅ **Hello {first_name}** 🎉\n"
            f"**You Are A PremiuM UseR Now 🧡**\n\n"
            f"Loss Recovery :- Join Now\n\n"
            f"Join Here 📌 (EXPIRE IN 5 MINUTES)"
        )

        # Inline Button with Channel Link
        keyboard = [
            [InlineKeyboardButton("📌 Join Channel Now", url="https://t.me/+g6b-NJx0d8BhMjU1")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # User ko DM mein message bhejein (parse_mode mein string use ki hai)
        await context.bot.send_message(
            chat_id=user_id, 
            text=welcome_message, 
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        print(f"Approved and welcomed {first_name} with custom button in channel ID: {chat_id}")
        
    except Exception as e:
        print(f"Error handling join request: {e}")

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
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers add karein
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))

    print("Multi-channel bot start ho raha hai...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Web server start karein
    await start_web_server()
    
    # Bot ko band hone se bachane ke liye
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
