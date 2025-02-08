import requests
import random
import os
import regex as re
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from PURVIMUSIC import app as bot  # Bot instance
from pyrogram import idle

# ✅ MongoDB Connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
vdb = mongo_client["vDb"]["v"]
chatai_db = mongo_client["Word"]["WordDb"]

# ✅ API Configuration
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# ✅ Custom Responses
custom_responses = {
    "hello": "Heyy! Mai Hinata hoon~ Aapki kya madad kar sakti hoon? 💕",
    "hi": "Hii, kaise ho aap? 😊",
    "hey": "Hey! Aap mujhe yaad kar rahe the? 😘",
    "salam": "Wa Alaikum Assalam! Aap kaise hain? 🤗",
    "namaste": "Namaste ji! Aapki kya seva kar sakti hoon? 🙏",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? 😍",
    "kya kar rahi ho": "Bas aapka wait kar rahi thi! Aap batao kya kar rahe ho? 😉"
}

# ✅ Bad Words List (Normal + Stylish fonts)
BAD_WORDS = [
    "sex", "nude", "porn", "xxx", "s3x", "hentai", "fuck", "bitch", "slut", "dick", "pussy", "boobs",
    "cock", "asshole", "cum", "orgasm", "rape", "horny", "masturbate", "sεx", "fυck", "bιtch", "dιck"
]
BAD_WORDS_REGEX = re.compile(r"|".join(BAD_WORDS), re.IGNORECASE)

# ✅ Helper function: Check if user is admin
async def is_admins(chat_id: int):
    admins = [member.user.id for member in await bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    return admins

# ✅ Chatbot OFF Command (Fix applied)
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_off(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("❍ **You are not an admin!**")

    await vdb.update_one({"chat_id": chat_id}, {"$set": {"disabled": True}}, upsert=True)
    await message.reply_text("❍ **Chatbot disabled successfully! 💔**")

# ✅ Chatbot ON Command (Fix applied)
@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_on(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("❍ **You are not an admin!**")

    await vdb.update_one({"chat_id": chat_id}, {"$set": {"disabled": False}}, upsert=True)
    await message.reply_text("❍ **Chatbot enabled successfully! 🥳**")

# ✅ Main Chatbot Handler
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = message.text or ""

    # 🚨 Bad Word Check
    if BAD_WORDS_REGEX.search(text):
        await message.delete()
        return

    # 🚀 Check if chatbot is OFF in groups
    chat_status = await vdb.find_one({"chat_id": chat_id})
    if chat_status and chat_status.get("disabled", False):
        return  # Chatbot is off, do nothing

    # ✅ Typing Indicator
    await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)

    # ✅ Check for Custom Response first
    for key in custom_responses:
        if key in text:
            await message.reply_text(custom_responses[key])
            return

    # ✅ Try fetching reply from MongoDB
    K = []
    is_chat = chatai_db.find({"word": text})

    k = await chatai_db.find_one({"word": text})
    if k:
        async for x in is_chat:
            K.append(x['text'])
        response = random.choice(K)
        is_text = await chatai_db.find_one({"text": response})

        if is_text and is_text['check'] == "sticker":
            await message.reply_sticker(response)
        else:
            await message.reply_text(response)
        return  # Stop here if MongoDB has reply

    # ✅ If no MongoDB reply, call API (Language Matching)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [{"role": "user", "content": text}]
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)

    if response.status_code != 200 or not response.text.strip():
        await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status: {response.status_code}")
        return

    response_data = response.json()
    if "choices" in response_data and len(response_data["choices"]) > 0:
        result = response_data["choices"][0]["message"]["content"]
        await message.reply_text(result)
    else:
        await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")

# ✅ Learn New Messages & Stickers (Auto-Learn Feature)
@bot.on_message(filters.reply & ~filters.bot)
async def learn_new_data(client, message: Message):
    if not message.reply_to_message:
        return

    bot_id = (await bot.get_me()).id
    if message.reply_to_message.from_user.id != bot_id:
        if message.sticker:
            is_chat = await chatai_db.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
            if not is_chat:
                await chatai_db.insert_one({
                    "word": message.reply_to_message.text,
                    "text": message.sticker.file_id,
                    "check": "sticker",
                    "id": message.sticker.file_unique_id
                })
        elif message.text:
            is_chat = await chatai_db.find_one({"word": message.reply_to_message.text, "text": message.text})
            if not is_chat:
                await chatai_db.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})

# ✅ Start the bot
idle()
