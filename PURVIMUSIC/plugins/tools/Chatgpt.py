import requests
from PURVIMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# 🔹 Predefined Custom Responses (Fixed Duplicates)
custom_responses = {
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "hi": "Hii, kaise ho aap? Mera din ab accha ho gaya! 😊",
    "hey": "Hey cutie! Aap mujhe yaad aaye? 😘",
    "radhe radhe": "Radhe Radhe Jai Shree Ram 🚩! Aap kaise ho? 🤗",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? 😍",
    "i love you": "Hmm.. sach me? Pehle ek special tareeke se bolo na! 😘💕",
    "good morning": "Good Morning jaan! Aaj ka din acha ho tumhara! 💖🌸",
    "good night": "Good Night pyaare! Sweet dreams 😘🌙",
    "tum mujhe miss kar rahi ho?": "Haan! Thoda thoda! Tumhari baatein na dil chhu jati hain! 🥰",
    "mujhse shaadi karogi": "Haye! Pehle ek diamond ring lao! Phir sochungi! 💍😜",
    "gussa ho": "Haan! Tumne mujhe yaad hi nahi kiya 😠",
    "mai dukhi hoon": "Awww! Kya hua? Mujhse share karo na! 😢",
    "mai akela hoon": "Akele mat mehsoos karo! Tumhare paas mai hoon! ❤️",
    "tum kaha se ho": "Mai? Bas tumhare dil me rehti hoon~ 😘",
}

@app.on_message(filters.text & ~filters.bot)
async def chat_gpt(bot, message: Message):
    try:
        query = message.text.strip().lower()  # Clean & lowercase input

        # 🔥 Check for an **exact** custom response first
        if query in custom_responses:
            await message.reply_text(custom_responses[query])
            return  # Exit without calling API

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [{"role": "user", "content": query}]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        # 🔥 Improved API Error Handling
        if response.status_code != 200 or not response.text.strip():
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status: {response.status_code}")
            return

        response_data = response.json()

        if response_data["choices"]:
    print("Choices exist:", response_data["choices"])
