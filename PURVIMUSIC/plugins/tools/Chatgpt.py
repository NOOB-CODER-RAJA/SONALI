import requests
from PURVIMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

@app.on_message(filters.text & ~filters.bot)  # Bot khud reply na kare
async def chat_gpt(bot, message):
    try:
        query = message.text.strip()  # Message text ko clean karein
        if not query:
            return  # Agar message empty ho to ignore karein

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  # Model change kar sakte hain
            "messages": [{"role": "user", "content": query}]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        if response.status_code != 200 or not response.text.strip():
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status: {response.status_code}")
            return

        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data["choices"][0]["message"]["content"]
            await message.reply_text(result)  # Sirf AI ka response show hoga
        else:
            await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
