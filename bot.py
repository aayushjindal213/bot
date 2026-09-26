# /start command handler (Updated buttons ke sath)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = (
        "🤖 **Auto Reaction Bot**\n\n"
        "I Automatically React To Every New Post In Your Channel With Emojis.\n\n"
        "**How To Use:**\n"
        "→ 1. Make Me Admin In Your Channel\n"
        "→ 2. Post A Message In Your Channel"
    )

    # Naye links ke sath updated buttons
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
