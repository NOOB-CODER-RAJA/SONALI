import os
import random
import requests
import unicodedata
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from deep_translator import GoogleTranslator

# ✅ Bot Initialization
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
vdb = mongo_client["vDb"]["v"]
chatai_db = mongo_client["Word"]["WordDb"]

bot = Client("chatbot", api_id=12345, api_hash="your_api_hash", bot_token="your_bot_token")

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

# ✅ Bad Words List (Normal & Stylish Fonts Detect)
BAD_WORDS = [
    "sex", "porn", "nude", "nangi", "naked", "xxx", "hentai", "boobs", "nipple", "suck",
    "blowjob", "deepthroat", "69", "hot sex", "erotic", "strip", "masturbate", "orgasm",
    "cum", "pussy", "vagina", "dildo", "anal", "threesome", "gangbang", "bondage", "bdsm",
    "cunnilingus", "rimming", "lick", "creampie", "panty", "bra", "milf", "jiggle", "slut",
    "whore", "escort", "prostitute", "hooker", "incest", "brother sister", "mother son",
    "father daughter", "rape", "pedophile", "child porn", "loli", "futa", "futa porn",
    "gay porn", "lesbian porn", "bisexual porn", "trans porn", "daddy kink", "stepmom",
    "stepsis", "stepbro", "sissy", "crossdress", "fetish", "golden shower", "scat", "piss",
    "fart fetish", "spanking", "submission", "domination", "bdsm porn", "slave", "cock",
    "dick", "penis", "shemale", "ladyboy", "cumshot", "bukkake", "handjob", "nude pic",
    "hot video", "camgirl", "onlyfans", "horny", "wet", "seduce", "sexy", "tits", "ass",
    "butt", "booty", "nudes", "thighs", "busty", "big tits", "big ass", "skinny dipping",
    "strip club", "stripper", "lap dance", "pov porn", "anime porn", "cartoon porn",
    "hentai video", "twerk", "nipple slip", "sex chat", "adult chat", "sugar daddy",
    "sugar baby", "escort service", "camshow", "webcam girl", "snapchat nudes",
    "onlyfans leak", "leaked nudes", "deepfake porn", "pornstar", "erotic novel",
    "hot story", "adult fiction", "roleplay sex", "virtual sex", "phone sex",
    "dirty talk", "moan", "fuck", "fucking", "motherfucker", "bitch", "cunt", "bastard",
    "hoe", "dumbass", "asshole", "shit", "bullshit", "pussylick", "goddamn", "nigga",
    "nigger", "chutiya", "bhosdi", "randi", "gaand", "loda", "lode", "lund", "maaderchod",
    "behnchod", "bsdk", "madarchod", "bc", "mc", "gandu", "rakhail", "jhantu", "chut",
    "laude", "gaand mara", "lavde", "chut ke raja", "suar ki aulad", "kutti", "kuttiya",
    "tera baap", "maa ki chut", "bhen ki chut", "lund choos", "chodu", "bhadwa",
    "sali kutti", "chodna", "kamina", "harami", "bhangi", "gandu saala", "gaand masti",
    "tatti", "chut mar", "suar", "randi ka bacha", "randi ke pille", "lund lund", "lauda"
]

# ✅ Function to Normalize Text (Stylish Font Removal)
def normalize_text(text):
    return ''.join(c for c in unicodedata.normalize("NFKD", text) if unicodedata.category(c) != "Mn").lower()

# ✅ Admin Check Function
async def is_admin(chat_id: int, user_id: int):
    admins = [member.user.id for member in await bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    return user_id in admins

# ✅ Chatbot ON/OFF Commands
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_off(client, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("**Are you sure you're an admin?**")

    if not await vdb.find_one({"chat_id": message.chat.id}):
        await vdb.insert_one({"chat_id": message.chat.id})
        await message.reply_text("**Chatbot disabled successfully! 💔**")
    else:
        await message.reply_text("**Chatbot is already disabled.**")

@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & filters.group)
async def chatbot_on(client, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("**Are you sure you're an admin?**")

    if await vdb.find_one({"chat_id": message.chat.id}):
        await vdb.delete_one({"chat_id": message.chat.id})
        await message.reply_text("**Chatbot enabled successfully! 🥳**")
    else:
        await message.reply_text("**Chatbot is already enabled.**")

# ✅ Main Chatbot Handler
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def handle_messages(client, message: Message):
    chat_id = message.chat.id
    text = message.text or message.caption or ""

    # **Check if Chatbot is Disabled**
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if await vdb.find_one({"chat_id": chat_id}):
            return  

    # **Check for Bad Words**
    if any(bad_word in normalize_text(text) for bad_word in BAD_WORDS):
        await message.delete()
        return
    
    await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)

    # **Custom Responses**
    for key in custom_responses:
        if key in text.lower():
            await message.reply_text(custom_responses[key])
            return  

    # **Check MongoDB for Response**
    responses = [doc['text'] async for doc in chatai_db.find({"word": text})]
    
    if responses:
        response = random.choice(responses)
        is_text = await chatai_db.find_one({"text": response})
        
        if is_text and is_text['check'] == "sticker":
            await message.reply_sticker(response)
        else:
            await message.reply_text(response)
        return

    # **Detect Language & Translate to English**
    lang = GoogleTranslator().detect(text)
    translated_text = GoogleTranslator(source=lang, target="en").translate(text)

    # **AI API Response**
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [{"role": "user", "content": translated_text}]
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)

    if response.status_code == 200 and response.text.strip():
        response_data = response.json()
        
        if "choices" in response_data and response_data["choices"]:
            ai_reply = response_data["choices"][0]["message"]["content"]

            # **Translate Back to User's Language**
            final_reply = GoogleTranslator(source="en", target=lang).translate(ai_reply)
            await message.reply_text(final_reply)
        else:
            await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
    else:
        await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status: {response.status_code}")

# ✅ Auto-Learn Feature (Text & Stickers)
@bot.on_message(filters.reply & ~filters.bot)
async def learn_new_data(client, message: Message):
    if not message.reply_to_message:
        return

    bot_id = (await bot.get_me()).id
    if message.reply_to_message.from_user.id != bot_id:
        if message.sticker:
            is_chat = await chatai_db.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
            if not is_chat:
                await chatai_db.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
        elif message.text:
            is_chat = await chatai_db.find_one({"word": message.reply_to_message.text, "text": message.text})
            if not is_chat:
                await chatai_db.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})
