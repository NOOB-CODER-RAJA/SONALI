import requests
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from SONALI_MUSIC import app  # Ensure this is correctly imported

async def fetch_med_info(client, message, query):
    """API से data fetch करे और reply करे"""
    if not query:
        return  # खाली message का कोई reply नहीं करेगा

    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    api_url = f"https://chatwithai.codesearch.workers.dev/?chat={query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("data", "**sᴏʀʀʏ, ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғᴇᴛᴄʜ ᴛʜᴇ ᴅᴀᴛᴀ.**")
        else:
            reply = "**ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴅᴀᴛᴀ ғʀᴏᴍ ᴛʜᴇ ᴀᴘɪ.**"
    except Exception as e:
        reply = f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :** {e}"

    await message.reply_text(reply)

@app.on_message(filters.text & ~filters.bot)  # Bot खुद से reply ना करे
async def chat_mode(client, message):
    query = message.text
    await fetch_med_info(client, message, query)
