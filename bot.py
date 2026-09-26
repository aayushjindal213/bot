import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, filters, ContextTypes
import logging

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Environment variables se token aur channel ID lena
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", -1001234567890))
WELCOME_TEXT = "Hello! Aapka channel par swagat hai."

# 1. Join Request aane par approve karke DM mein welcome message bhejna
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.chat_join_request.from_user.id
    chat_id = update.chat_join_request.chat.id
    first_name = update.chat_join_request.from_user.first_name

    if chat_id == CHANNEL_ID:
        try:
            await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
            await context.bot.send_message(chat_id=user_id, text=f"{first_name}, {WELCOME_TEXT}")
            print(f"Approved and welcomed: {first_name}")
        except Exception as e:
            print(f"Error handling join request: {e}")

# 2. Channel par naye post par action (reply/notification) ke liye
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.channel_post.chat.id
    if chat_id == CHANNEL_ID:
        try:
            message_id = update.channel_post.message_id
            # Bot channel post par comment/reply bhej sakta hai
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text="New post published!",
                reply_to_message_id=message_id
            )
            print(f"Responded to post ID: {message_id}")
        except Exception as e:
            print(f"Error in channel post: {e}")

# Render ke liye Dummy Web Server (Port error hatane ke liye)
async def handle(request):
    return web.Response(text="Bot is running 24x7!")

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

    print("Bot start ho raha hai...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Web server start karein
    await start_web_server()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
