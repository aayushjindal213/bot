import os
import asyncio
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from pyrogram.raw import functions
from pyrogram.raw.types import ReactionEmoji

# Apni details yahan dalein ya Render ke Environment Variables use karein
API_ID = int(os.environ.get("API_ID", "12345678"))  # Apni API ID
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001234567890"))
WELCOME_TEXT = "Hello! Aapka channel par swagat hai."

# Pyrogram Client initialize karein
app = Client(
    "auto_reaction_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 1. Join Request Handle karne ke liye
@app.on_chat_join_request(filters.chat(CHANNEL_ID))
async def approve_and_welcome(client, request: ChatJoinRequest):
    try:
        await client.approve_chat_join_request(chat_id=request.chat.id, user_id=request.user.id)
        await client.send_message(chat_id=request.user.id, text=WELCOME_TEXT)
        print(f"Approved and welcomed: {request.user.first_name}")
    except Exception as e:
        print(f"Error in join request: {e}")

# 2. Channel post par Auto-Reaction ke liye
@app.on_message(filters.chat(CHANNEL_ID) & filters.incoming)
async def auto_react(client, message):
    try:
        await client.invoke(
            functions.messages.SendReaction(
                peer=await client.resolve_peer(CHANNEL_ID),
                msg_id=message.id,
                reaction=[ReactionEmoji(emoticon="❤️")]
            )
        )
        print(f"Reaction sent to message ID: {message.id}")
    except Exception as e:
        print(f"Error in auto reaction: {e}")

# Render Web Service ke liye Dummy HTTP Server (Port error hatane ke liye)
async def handle(request):
    return web.Response(text="Bot is running 24x7!")

async def web_server():
    web_app = web.Application()
    web_app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await app.start()
    print("Telegram bot successfully start ho gaya hai!")
    await web_server()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
