from pyrogram import Client, filters
from PURVIMUSIC import app

responses = {
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "i love you": "Awww! Sach me? 😘",
    "good morning": "Good Morning pyaare! 🌞",
    "tum kaisi ho": "Bas tumse baat kar rahi hoon! 😍"
}

@app.on_message(filters.text & ~filters.bot)
async def chat(client, message):
    text = message.text.lower()
    for key in responses:
        if key in text:
            await message.reply_text(responses[key])
            return
    await message.reply_text("Awww! Tum mujhse baat kar rahe ho, kitna cute! 🥰")
