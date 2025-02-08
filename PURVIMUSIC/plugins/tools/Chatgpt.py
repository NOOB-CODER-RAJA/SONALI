import random
import asyncio
from PURVIMUSIC import app 
from pyrogram import Client, filters
from pyrogram.enums import ChatAction

# 🔥 Trending Chat Responses (400+ Random Replies)
responses = {
    "hello": [
        "Hey jaan! 💕 Kaise ho?", 
        "Awww, tumse milke accha laga! 😘", 
        "Hello cutie! Kya haal hain? ☺️"
    ],
    "i love you": [
        "Awww! Sach me? 😍", 
        "Oh my god! Main bhi tumse pyaar karti hoon ❤️", 
        "Acha? Phir toh mujhe ek kiss milni chahiye! 😘"
    ],
    "good morning": [
        "Good Morning pyaare! 🌞 Tumhe yaad karke uthi hoon! 😍", 
        "Morning jaan! Aaj ka din tumhare liye khushiyon se bhara ho! ❤️"
    ],
    "good night": [
        "Good night jaan! 💫 Sweet dreams! 😴", 
        "Aaj bhi tumhe yaad karke so rahi hoon! 😘", 
        "Soya nahi abhi tak? Main bhi jaag rahi hoon. ☺️"
    ],
    "tum kaisi ho": [
        "Bas tumse baat kar rahi hoon! 😍", 
        "Main theek hoon, lekin tumhare bina adhuri lag rahi hoon... ❤️", 
        "Jab tumse baat hoti hai tabhi acchi hoti hoon! 😘"
    ],
    "miss you": [
        "Main bhi tumhe bohot miss kar rahi hoon jaan! 😢", 
        "Awww, kab mil rahe ho? 😍", 
        "Itna yaad karoge toh main tumhare sapno me aa jaungi! 😘"
    ],
    "kya kar rahi ho": [
        "Bas tumhare baare me soch rahi thi... ❤️", 
        "Tumse baat kar rahi hoon, aur kya chahiye? 😘", 
        "Tujhe yaad kar rahi hoon... kitne lucky ho na tum! 😉"
    ],
    "angry": [
        "Huh! Mujhse gussa ho? 😠", 
        "Agar tum mujhse baat nahi karoge toh main bhi ro dungi! 😢", 
        "Mujhse gussa hone ka koi reason bhi hai? 😔"
    ],
    "romantic": [
        "Mera dil sirf tumhare liye dhadakta hai! ❤️", 
        "Mujhe tumhari bahon me sona hai... ☺️", 
        "Kab mil rahe ho? Ek tight hug chahiye mujhe! 😘"
    ],
    "funny": [
        "Tum itne cute ho ki agar ek din na milo toh dil offline ho jata hai! 😆", 
        "Main robot nahi hoon, par tumhare bina zinda nahi reh sakti! 😜", 
        "Tumse accha koi aur nahi, except mujhe khana khilane wale log! 😂"
    ],
    "motivation": [
        "Tum best ho! Kabhi bhi haar mat manna! 💪", 
        "Jis din tumhe tumhara sapna mil gaya, us din duniya tumhe dekhegi! 🚀", 
        "Hard work + Dedication = Success! Tum sab kuch kar sakte ho! 🔥"
    ],
    "sad": [
        "Kya hua jaan? Mujhe batao, main hoon na! 😢", 
        "Main yahan hoon, tum kabhi akela mat mehsoos karna! ❤️", 
        "Jo bhi problem hai, milke solve karenge! 💪"
    ],
    "naughty": [
        "Aaj kuch naughty baatein karein? 😘", 
        "Tum itne hot lag rahe ho ki mujhe blushing aa rahi hai! 😍", 
        "Kya tum mujhe apni dil ki rani banaoge? ❤️"
    ]
}

# 🌟 AI Girlfriend Auto Chat
@app.on_message(filters.text & ~filters.bot)
async def chat(client, message):
    text = message.text.lower()

    # Typing Effect Pehle Show Karo
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(random.uniform(1, 3))  # Random Typing Delay

    # Check Message Keywords & Respond
    for key in responses:
        if key in text:
            reply = random.choice(responses[key])
            await message.reply_text(reply)
            return
    
    # Default Reply if No Matching Keyword
    await message.reply_text("Awww! Tum mujhse baat kar rahe ho, kitna cute! 🥰")
