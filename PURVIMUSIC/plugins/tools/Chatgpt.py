from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import random
import os
import re
import requests
import unicodedata
from PURVIMUSIC import app as bot
from pyrogram import idle

# ✅ MongoDB Connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
vdb = mongo_client["vDb"]["v"]
chatai_db = mongo_client["Word"]["WordDb"]

# ✅ API Configuration
API_KEY = "YOUR_OPENAI_API_KEY"
BASE_URL = "https://api.openai.com/v1/chat/completions"

# ✅ Helper Function: Check If User Is Admin
async def is_admins(chat_id: int):
    admins = [member.user.id async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    return admins

# ✅ Custom Responses
custom_responses = {
    "hello": "Hi there! 😊",
    "how are you": "I'm just a bot, but I'm doing great!",
    "who made you": "I was created by a developer who loves coding!",
    "bye": "Goodbye! Have a great day! 😊",
    "love you": "Aww! Love you too ❤️",
}

# ✅ Bad Word List (Stylish & Normal)
bad_words = [
    "sex", "porn", "nude", "fuck", "bitch", "dick", "pussy", "slut", "boobs", "cock", "asshole",
    "रंडी", "चोद", "मादरचोद", "गांड", "लंड", "भोसड़ी", "हिजड़ा", "पागल", "नंगा"
]
stylish_bad_words = [unicodedata.normalize("NFKD", word) for word in bad_words]
bad_word_regex = re.compile(r'\b(' + "|".join(stylish_bad_words) + r')\b', re.IGNORECASE)

# ✅ Command to Turn Chatbot OFF
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_off(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!")

    is_v = await vdb.find_one({"chat_id": chat_id})
    if not is_v:
        await vdb.insert_one({"chat_id": chat_id})
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ!")
    else:
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴏғғ!")

# ✅ Command to Turn Chatbot ON
@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_on(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!")

    is_v = await vdb.find_one({"chat_id": chat_id})
    if is_v:
        await vdb.delete_one({"chat_id": chat_id})
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ!")
    else:
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴏɴ!")

# ✅ Main Chatbot Handler (Text & Stickers)
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = message.text if message.text else ""

    # ✅ Check If Chatbot Is OFF
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if await vdb.find_one({"chat_id": chat_id}):
            return

    # ✅ Bad Word Filter (Delete Message)
    if bad_word_regex.search(text):
        await message.delete()
        return

    # ✅ Check for Custom Responses
    for key in custom_responses:
        if key in text.lower():
            await message.reply_text(custom_responses[key])
            return

    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    # ✅ MongoDB Check for Stickers & Text
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

    # ✅ API Response with Auto-Language Detection
    if text:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [{"role": "user", "content": text}]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                result = response_data["choices"][0]["message"]["content"]
                await message.reply_text(result)
            else:
                await message.reply_text("❍ ᴇʀʀᴏʀ: API response missing!")
        else:
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API failed. Status: {response.status_code}")

# ✅ Auto-Learn Messages & Stickers
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
