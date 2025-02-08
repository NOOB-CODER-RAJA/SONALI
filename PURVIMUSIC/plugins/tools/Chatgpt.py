import requests
import random
import os
import re
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from PURVIMUSIC import app as bot

# ✅ MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
vdb = mongo_client["vDb"]["v"]
chatai_db = mongo_client["Word"]["WordDb"]

# ✅ Together API Setup
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

# ✅ Bad Words List (Stylish Fonts + Normal)
bad_words = [
    "sex", "porn", "nude", "xxx", "b00bs", "boobs", "ass", "slut", "fuck", "bitch", "dick",
    "s3x", "p0rn", "hentai", "69", "horny", "chut", "lund", "gand", "randi", "chod", "suck",
    "pussy", "fuckoff", "muth", "masturbate", "virgin", "bj", "naked"
]
bad_words_regex = re.compile(r"\b(" + "|".join(bad_words) + r")\b", re.IGNORECASE)

# ✅ Admin Check Helper Function
async def is_admins(chat_id: int):
    admins = []
    async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(member.user.id)
    return admins

# ✅ Chatbot ON/OFF Commands
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_off(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("❍ **You are not an admin!**")

    await vdb.update_one({"chat_id": chat_id}, {"$set": {"disabled": True}}, upsert=True)
    await message.reply_text("❍ **Chatbot disabled successfully! 💔**")

@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_on(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("❍ **You are not an admin!**")

    await vdb.update_one({"chat_id": chat_id}, {"$set": {"disabled": False}}, upsert=True)
    await message.reply_text("❍ **Chatbot enabled successfully! 🥳**")

# ✅ Main Chatbot Handler (Text + Sticker)
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id

    # ✅ If in group, check if chatbot is disabled
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        is_v = await vdb.find_one({"chat_id": chat_id})
        if is_v and is_v.get("disabled"):
            return  

    await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)

    # ✅ Check for Bad Words & Delete if Found
    if bad_words_regex.search(message.text or ""):
        await message.delete()
        return

    # ✅ Custom Response Handling
    query = message.text.strip().lower()
    for key in custom_responses:
        if key in query:
            await message.reply_text(custom_responses[key])
            return

    # ✅ MongoDB Reply Handling
    K = []
    is_chat = chatai_db.find({"word": message.text})
    async for x in is_chat:
        K.append(x['text'])
    
    if K:
        response = random.choice(K)
        is_text = await chatai_db.find_one({"text": response})

        if is_text and is_text.get("check") == "sticker":
            await message.reply_sticker(response)
        else:
            await message.reply_text(response)
        return

    # ✅ AI Response with Same Language
    detected_lang = detect_language(message.text)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [{"role": "user", "content": message.text}],
        "response_format": {"type": detected_lang}
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
        await message.reply_text("❍ ᴇʀʀᴏʀ: API request failed. Status: " + str(response.status_code))
