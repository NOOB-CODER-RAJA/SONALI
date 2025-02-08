from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import os
import re
import requests
import unicodedata
import random

from PURVIMUSIC import app as bot

# ✅ MongoDB Connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
status_db = mongo_client["ChatbotStatus"]["status"]
chatai_db = mongo_client["Word"]["WordDb"]

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
    "sex", "porn", "nude", "fuck", "bitch", "dick", "pussy", "slut", "boobs", "cock", "asshole",
    "रंडी", "चोद", "मादरचोद", "गांड", "लंड", "भोसड़ी", "हिजड़ा", "पागल", "नंगा"
]

stylish_bad_words = [normalize_text(word) for word in bad_words]
bad_word_regex = re.compile(r'\b(' + "|".join(stylish_bad_words) + r')\b', re.IGNORECASE)

# ✅ Custom Responses
custom_responses = {
    "hello": "Hi there! 😊",
    "how are you": "I'm just a bot, but I'm doing great!",
    "who made you": "I was created by a developer who loves coding!",
    "bye": "Goodbye! Have a great day! 😊",
    "love you": "Aww! Love you too ❤️",
}

# ✅ Inline Buttons for Chatbot Control
CHATBOT_ON = [
    [
        InlineKeyboardButton(text="✅ Enable", callback_data="enable_chatbot"),
        InlineKeyboardButton(text="🚫 Disable", callback_data="disable_chatbot"),
    ],
]

# ✅ /chatbot Command with Buttons
@bot.on_message(filters.command("chatbot") & filters.group)
async def chatbot_control(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(chat_id, user_id):
        return await message.reply_text("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!")

    await message.reply_text(
        f"**Chatbot Control Panel**\n\n"
        f"📌 Chat: {message.chat.title}\n"
        f"🛠 Choose an option to Enable/Disable chatbot.",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

# ✅ Callback for Enable/Disable Buttons
@bot.on_callback_query(filters.regex(r"enable_chatbot|disable_chatbot"))
async def chatbot_callback(client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if not await is_admin(chat_id, user_id):
        return await query.answer("❍ You are not an admin!", show_alert=True)

    action = query.data

    if action == "enable_chatbot":
        status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "enabled"}}, upsert=True)
        await query.answer("✅ Chatbot Enabled!", show_alert=True)
        await query.edit_message_text(f"✅ **Chatbot has been enabled in {query.message.chat.title}.**")
    else:
        status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "disabled"}}, upsert=True)
        await query.answer("🚫 Chatbot Disabled!", show_alert=True)
        await query.edit_message_text(f"🚫 **Chatbot has been disabled in {query.message.chat.title}.**")

# ✅ Main Chatbot Handler
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = normalize_text(message.text) if message.text else ""

    # ✅ Check If Chatbot Is OFF
    chat_status = await status_db.find_one({"chat_id": chat_id})
    if chat_status and chat_status.get("status") == "disabled":
        return

    # ✅ Bad Word Filter (Delete Message)
    if bad_word_regex.search(text):
        await message.delete()
        return

    await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)

    # ✅ Check for Custom Responses First
    for key in custom_responses:
        if key in text.lower():
            await message.reply_text(custom_responses[key])
            return

    # ✅ MongoDB Check for Stickers & Text
    response_list = []

    if message.sticker:
        async for x in chatai_db.find({"word": message.sticker.file_unique_id}):
            response_list.append(x['text'])
    else:
        async for x in chatai_db.find({"word": text}):
            response_list.append(x['text'])

    if response_list:
        response = random.choice(response_list)
        is_text = await chatai_db.find_one({"text": response})
        if is_text and is_text['check'] == "sticker":
            await message.reply_sticker(response)
        else:
            await message.reply_text(response)
        return

    # ✅ API Call (Auto-Detect Language)
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
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "❍ API Error!")
            await message.reply_text(result)
        else:
            await message.reply_text(f"❍ API failed. Status: {response.status_code}")

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

