import requests
import os
from PURVIMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

API key ko environment variable mein store karein
API_KEY = os.environ.get("abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce")

Base URL
BASE_URL = "https://api.together.xyz/v1/chat/completions"

Predefined Custom Responses
custom_responses = {
    "hello": "Heyy! Mai Hinata hoon~ Aapki kya madad kar sakti hoon? ",
    "hi": "Hii, kaise ho aap? ",
    "hey": "Hey! Aap mujhe yaad kar rahe the? ",
    "salam": "Wa Alaikum Assalam! Aap kaise hain? ",
    "namaste": "Namaste ji! Aapki kya seva kar sakti hoon? ",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? ",
    "kya kar rahi ho": "Bas aapka wait kar rahi thi! Aap batao kya kar rahe ho? "
}

API request ko ek separate function mein banayein
def api_request(query):
    try:
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
            return f" ᴇʀʀᴏʀ: API request failed. Status: {response.status_code}"
        
        response_data = response.json()
        
        if "choices" in response_data and len(response_data["choices"]) > 0:
            result = response_data["choices"][0]["message"]["content"]
            return result
        else:
            return " ᴇʀʀᴏʀ: No response from API."
    
    except Exception as e:
        return f"** ᴇʀʀᴏʀ: {e}**"

@app.on_message(filters.text & ~filters.bot)
async def chat_gpt(bot, message):
    try:
        query = message.text.strip().lower()
        
        # Check for custom responses first
        for key in custom_responses:
            if key in query:
                await message.reply_text(custom_responses[key])
                return
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        result = api_request(query)
        await message.reply_text(result)
    
    except Exception as e:
        await message.reply_text(f"** ᴇʀʀᴏʀ: {e}**")
