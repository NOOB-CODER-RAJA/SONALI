import requests
from PURVIMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from pyrogram import filters
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import os
import random

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://bikash:bikash@bikash.3jkvhp7.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
chatai_db = mongo_client["Word"]["WordDb"]

# Together API Details
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# 🔹 Predefined Custom Responses
custom_responses = {
    "hello": "Heyy! Mai Hinata hoon~ Aapki kya madad kar sakti hoon? 💕",
    "hi": "Hii, kaise ho aap? 😊",
    "hey": "Hey! Aap mujhe yaad kar rahe the? 😘",
    "salam": "Wa Alaikum Assalam! Aap kaise hain? 🤗",
    "namaste": "Namaste ji! Aapki kya seva kar sakti hoon? 🙏",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? 😍",
    "kya kar rahi ho": "Bas aapka wait kar rahi thi! Aap batao kya kar rahe ho? 😉"
}

@app.on_message(filters.text | filters.sticker & ~filters.bot)
async def chat_gpt(bot, message: Message):
    try:
        query = message.text.strip().lower() if message.text else None  # Message text clean aur lowercase karein
        sticker_id = message.sticker.file_unique_id if message.sticker else None  # Sticker ID store karein

        # Bot Typing Indicator ON
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        # 1️⃣ **Check for Custom Responses First**
        if query:
            for key in custom_responses:
                if key in query:
                    reply_text = custom_responses[key]
                    await message.reply_text(reply_text)
                    
                    # **MongoDB me Save Karo**
                    await chatai_db.insert_one({"word": query, "text": reply_text, "check": "none"})
                    return  # Agar custom response mil gaya, toh yahin return ho jaye

        # 2️⃣ **Check MongoDB for Stored Replies**
        K = []

        if query:
            is_chat = chatai_db.find({"word": query})  # AsyncIOMotorCursor
            k = await chatai_db.find_one({"word": query})
        elif sticker_id:
            k = await chatai_db.find_one({"text": sticker_id, "check": "sticker"})  # Sticker check

        if k:
            if query:
                async for x in is_chat:
                    K.append(x['text'])
                response = random.choice(K)
            else:
                response = k['word']  # Sticker ke liye response word me store hoga
            
            is_text = await chatai_db.find_one({"text": response})

            if is_text and is_text['check'] == "sticker":
                await message.reply_sticker(is_text["text"])  # Sticker ID se reply karein
            else:
                await message.reply_text(response)
            
            return  # Agar MongoDB me mil gaya toh API call nahi hoga

        # 3️⃣ **AI API Call (if no custom or MongoDB response)**
        if not query:  # Sticker ka AI response nahi chahiye
            return

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

        if response.status_code != 200 or not response.text.strip():
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status: {response.status_code}")
            return

        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data["choices"][0]["message"]["content"]
            await message.reply_text(result)  # AI Response

            # **MongoDB me AI ka response Save Karo**
            await chatai_db.insert_one({"word": query, "text": result, "check": "none"})

        else:
            await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
