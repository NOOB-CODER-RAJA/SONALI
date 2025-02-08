from pyrogram import Client, filters, enums
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import random
import os
from PURVIMUSIC import app as bot
from pyrogram import idle

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
vdb = mongo_client["vDb"]["v"]
chatai_db = mongo_client["Word"]["WordDb"]

# Helper function to check if user is an admin
async def is_admins(chat_id: int):
    admins = [member.user.id for member in await bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    return admins

# Command to turn chatbot off (Groups Only)
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_off(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("**Are you sure you're an admin?**")

    is_v = await vdb.find_one({"chat_id": chat_id})
    if not is_v:
        await vdb.insert_one({"chat_id": chat_id})
        await message.reply_text("**Chatbot disabled successfully! 💔**")
    else:
        await message.reply_text("**Chatbot is already disabled.**")

# Command to turn chatbot on (Groups Only)
@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_on(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("**Are you sure you're an admin?**")

    is_v = await vdb.find_one({"chat_id": chat_id})
    if is_v:
        await vdb.delete_one({"chat_id": chat_id})
        await message.reply_text("**Chatbot enabled successfully! 🥳**")
    else:
        await message.reply_text("**Chatbot is already enabled.**")

# Command to display chatbot usage info
@bot.on_message(filters.command("chatbot", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_usage(client, message: Message):
    await message.reply_text("**Usage: /chatbot [on/off] only for groups.**")

# Main Chatbot Handler (For Both Private & Group)
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id

    # If in group, check if chatbot is disabled
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        is_v = await vdb.find_one({"chat_id": chat_id})
        if is_v:
            return  # Chatbot is off, do nothing

    await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)
    K = []
    is_chat = chatai_db.find({"word": message.text})  # AsyncIOMotorCursor

    k = await chatai_db.find_one({"word": message.text})
    if k:
        async for x in is_chat:
            K.append(x['text'])
        response = random.choice(K)
        is_text = await chatai_db.find_one({"text": response})
        
        if is_text and is_text['check'] == "sticker":
            await message.reply_sticker(response)
        else:
            await message.reply_text(response)

# Learn New Messages & Stickers (Auto-Learn Feature)
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

# Start the bot
idle()
