import requests
import pymongo
from PURVIMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from pyrogram import filters

# 🔹 MongoDB Connection
MONGO_URI = "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority"  # MongoDB connection string
client = pymongo.MongoClient(MONGO_URI)
db = client["ChatBotDB"]  # Database ka naam
collection = db["responses"]  # Collection ka naam

# 🔹 AI API Config
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# 🔹 Custom Static Responses
custom_responses = {
    "hello": "Heyy! Mai Hinata hoon~ Aapki kya madad kar sakti hoon? 💕",
    "hi": "Hii, kaise ho aap? 😊",
    "hey": "Hey! Aap mujhe yaad kar rahe the? 😘",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? 😍",
    "salam": "Wa Alaikum Assalam! Aap kaise hain? 🤗",
    "namaste": "Namaste ji! Aapki kya seva kar sakti hoon? 🙏"
}

@app.on_message(filters.text & ~filters.bot)
async def chat_gpt(bot, message):
    try:
        query = message.text.strip().lower()  # Text ko clean karein

        # 🔹 Step 1: Check in Custom Responses
        for key in custom_responses:
            if key in query:
                await message.reply_text(custom_responses[key])  # Custom response bheje
                return

        # 🔹 Step 2: MongoDB me check karein
        db_response = collection.find_one({"query": query})
        if db_response:
            await message.reply_text(db_response["response"])  # MongoDB ka reply
            return
        
        # 🔹 Step 3: AI API Call (Agar response MongoDB me bhi nahi mila)
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
            
            # 🔹 Step 4: MongoDB me response store karein (Next time direct use hoga)
            collection.insert_one({"query": query, "response": result})
            
            await message.reply_text(result)  # AI Response
        else:
            await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
    
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
