import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest
from pyrogram.raw import functions
from pyrogram.raw.types import ReactionEmoji

# Apni details yahan bharein
API_ID = 12345678  # Apni API ID yahan dalein (Integer)
API_HASH = "your_api_hash_here"
BOT_TOKEN = "8767028136:AAE1ALaRnNwA74IVKiE3O5qohh8IfDEEbj4"
CHANNEL_ID = -1001234567890  # Apne Channel ki ID yahan dalein (Negative hoti hai)
WELCOME_TEXT = "Hello! Aapka channel par swagat hai. Kripya rules padhein."

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
        # User ko channel par approve karein
        await client.approve_chat_join_request(
            chat_id=request.chat.id, 
            user_id=request.user.id
        )
        
        # User ko Personal Message (DM) mein welcome message bhejein
        await client.send_message(
            chat_id=request.user.id,
            text=WELCOME_TEXT
        )
        print(f"Approved and welcomed: {request.user.first_name}")
    except Exception as e:
        print(f"Error in join request: {e}")

# 2. Channel par naye post par Auto-Reaction ke liye
@app.on_message(filters.chat(CHANNEL_ID) & filters.incoming)
async def auto_react(client, message):
    try:
        # Pyrogram raw API ka use karke post par reaction (jaise ❤️ ya 🔥) bhejna
        await client.invoke(
            functions.messages.SendReaction(
                peer=await client.resolve_peer(CHANNEL_ID),
                msg_id=message.id,
                reaction=[ReactionEmoji(emoticon="❤️")]  # Aap yahan koi bhi emoji badal sakte hain
            )
        )
        print(f"Reaction sent to message ID: {message.id}")
    except Exception as e:
        print(f"Error in auto reaction: {e}")

if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
