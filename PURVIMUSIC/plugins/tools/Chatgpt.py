from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.enums import ChatAction
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
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# ✅ Helper Function: Check If User Is Admin
async def is_admins(chat_id: int):
    return [member.user.id async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]

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

# ✅ Fix: Stylish Font Bad Words Detection
def normalize_text(text):
    return unicodedata.normalize("NFKD", text)

stylish_bad_words = [normalize_text(word) for word in bad_words]
bad_word_regex = re.compile(r'\b(' + "|".join(stylish_bad_words) + r')\b', re.IGNORECASE)

# ✅ New Command: /chatbot (Guidelines for ON/OFF)
@bot.on_message(filters.command("chatbot", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_help(client, message: Message):
    help_text = """❍ **Chatbot Guide** ❍
    
✔ **Enable Chatbot**  
   `/chatbot on` - Enables chatbot (Admin only)  

✔ **Disable Chatbot**  
   `/chatbot off` - Disables chatbot (Admin only)  

✔ **Auto Learning**  
   - Reply to bot messages with text/sticker to teach new responses.  
   - Bot will reply based on learned responses.  

✔ **Bad Words Filter**  
   - Bot **deletes** messages containing inappropriate words.  

🔹 *Developed for Smart Group Conversations!*  
"""
    await message.reply_text(help_text)

# ✅ Command to Turn Chatbot OFF
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_off(client, message: Message):
    chat_id = message.chat.id

    if message.from_user.id not in await is_admins(chat_id):
        return await message.reply_text("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!")

    if not await vdb.find_one({"chat_id": chat_id}):
        await vdb.insert_one({"chat_id": chat_id})
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ!")
    else:
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴏғғ!")

# ✅ Command to Turn Chatbot ON
@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_on(client, message: Message):
    chat_id = message.chat.id

    if message.from_user.id not in await is_admins(chat_id):
        return await message.reply_text("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ!")

    if await vdb.find_one({"chat_id": chat_id}):
        await vdb.delete_one({"chat_id": chat_id})
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ!")
    else:
        await message.reply_text("❍ ᴄʜᴀᴛʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴏɴ!")

# ✅ Main Chatbot Handler with Priority Fix
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = normalize_text(message.text) if message.text else ""

    # ✅ Check If Chatbot Is OFF
    if await vdb.find_one({"chat_id": chat_id}):
        return

    # ✅ Bad Word Filter (Delete Message)
    if bad_word_regex.search(text):
        await message.delete()
        return

    # ✅ 1st Priority: Custom Responses
    for key in custom_responses:
        if key in text.lower():
            await message.reply_text(custom_responses[key])
            return

    # ✅ 2nd Priority: MongoDB Check
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

    # ✅ 3rd Priority: API Call
    if text:
        await bot.send_chat_action(chat_id, ChatAction.TYPING)
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

# ✅ Start the bot
idle()
