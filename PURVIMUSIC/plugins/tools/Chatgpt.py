from pyrogram import Client, filters, enums
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import os
import re
import requests
import unicodedata
import random
from langdetect import detect  # For language detection

from PURVIMUSIC import app as bot

# ✅ MongoDB Connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
status_db = mongo_client["ChatbotStatus"]["status"]
chatai_db = mongo_client["Word"]["WordDb"]

# ✅ Fix for `vdb` (chatbot status)
vdb = mongo_client["ChatBot"]["ChatStatus"]

# ✅ API Configuration
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# ✅ Helper Function: Check If User Is Admin
async def is_admin(chat_id: int, user_id: int):
    admins = [member.user.id async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    return user_id in admins

# ✅ Fix: Stylish Font Bad Words Detection
def normalize_text(text):
    return unicodedata.normalize("NFKD", text)

bad_words = [
    "sex", "porn", "nude", "fuck", "bitch", "dick", "pussy", "slut", "boobs", "cock", "asshole", "chudai", "rand", "chhinar", "sexy", "hot girl", "land", "lund",
    "रंडी", "चोद", "मादरचोद", "गांड", "लंड", "भोसड़ी", "हिजड़ा", "पागल", "नंगा"
]

stylish_bad_words = [normalize_text(word) for word in bad_words]
bad_word_regex = re.compile(r'\b(' + "|".join(stylish_bad_words) + r')\b', re.IGNORECASE)

# custom response
custom_responses = {
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "i love you": "Awww! Sach me? 😘",
    "good morning": "Good Morning pyaare! 🌞",
    "tum kaisi ho": "Bas tumse baat kar rahi hoon! 😍"
}

# ✅ Main Chatbot Handler (Text & Stickers)
@bot.on_message(filters.text | filters.sticker)
async def chatbot_reply(client, message: Message):
    chat_id = message.chat.id
    text = message.text.strip() if message.text else ""
    bot_username = (await bot.get_me()).username.lower()

    # Typing indicator show karna
    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    # Agar message mein koi bad word ho
    if re.search(bad_word_regex, text):
        await message.delete()
        await message.reply_text("❍ ᴇʀʀᴏʀ: Aapke message mein kuch inappropriate shabdon ka istemal hua hai. Kripya sudhaar karein.")
        return

    # Agar message group mein hai
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:

        # Custom Message Check (Pehle check karna)
        for key in custom_responses:
            if key in text.lower():
                await message.reply_text(custom_responses[key])
                return

        # MongoDB se reply dena (Agar custom response nahi mila)
        K = []
        if message.sticker:
            async for x in chatai_db.find({"word": message.sticker.file_unique_id}):
                K.append(x['text'])
        else:
            async for x in chatai_db.find({"word": text}):
                K.append(x['text'])

        if K:
            response = random.choice(K)
            is_text = await chatai_db.find_one({"text": response})
            if is_text and is_text['check'] == "sticker":
                await message.reply_sticker(response)
            else:
                await message.reply_text(response)
            return

        # Agar koi mention ya bot ka naam ho to API Response dena
        if f"@{bot_username}" in text.lower() or bot_username in text.lower():
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            payload = {"model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "messages": [{"role": "user", "content": text}]}

            response = requests.post(BASE_URL, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "❍ ᴇʀʀᴏʀ: API response missing!")
                await message.reply_text(result)
            else:
                await message.reply_text(f"❍ ᴇʀʀᴏʀ: API failed. Status: {response.status_code}")
        return

    # Agar message private chat mein hai
    elif message.chat.type == enums.ChatType.PRIVATE:

        # Custom Message Check (Pehle check karna)
        for key in custom_responses:
            if key in text.lower():
                await message.reply_text(custom_responses[key])
                return

        # MongoDB se reply dena (Agar custom response nahi mila)
        K = []
        if message.sticker:
            async for x in chatai_db.find({"word": message.sticker.file_unique_id}):
                K.append(x['text'])
        else:
            async for x in chatai_db.find({"word": text}):
                K.append(x['text'])

        if K:
            response = random.choice(K)
            is_text = await chatai_db.find_one({"text": response})
            if is_text and is_text['check'] == "sticker":
                await message.reply_sticker(response)
            else:
                await message.reply_text(response)
            return

        # API Response dena private chat mein (Agar custom response aur MongoDB se reply nahi mila)
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "messages": [{"role": "user", "content": text}]}

        response = requests.post(BASE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "❍ ᴇʀʀᴏʀ: API response missing!")
            await message.reply_text(result)
        else:
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API failed. Status: {response.status_code}")
