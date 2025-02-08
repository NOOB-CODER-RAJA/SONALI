import openai
import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from PURVIMUSIC import app  # Ensure this is correctly imported

# 🔑 Yahan apni OpenAI API key daalein
openai.api_key = "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"

async def chat_with_gpt(prompt):
    """OpenAI API se response fetch kare"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ya "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"**API Error:** {e}"

@app.on_message(filters.text & ~filters.bot)  # Bot khud se reply na kare
async def chat_mode(client, message):
    query = message.text.strip()
    if not query:
        return  # Empty message ignore karega

    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    reply = await chat_with_gpt(query)
    await message.reply_text(reply)
