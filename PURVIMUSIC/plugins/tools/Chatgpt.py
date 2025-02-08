import requests
from PURVIMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# 🔹 Predefined Custom Responses
custom_responses = {
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "i love you": "Awww! Sach me? 😘",
    "good morning": "Good Morning pyaare! 🌞",
    "tum kaisi ho": "Bas tumse baat kar rahi hoon! 😍",
  ## 💖 Flirty & Romantic Mode (Zyada Romantic Replies)
    "i love you": "Hmm.. sach me? Pehle ek special tareeke se bolo na! 😘💕",
    "tum bohot cute ho": "Awww! Tum bhi to mere hero lag rahe ho! 😍",
    "mujhe tumhari yaad aa rahi hai": "Awww! Chalo ek virtual jhappi lo! 🤗💕",
    "tum meri jaan ho": "Oho! Ab itna pyaar de rahe ho, fir to mai tumhari hi hoon! 😘",
    "mujhe miss kar rahi ho?": "Haan! Thoda thoda! Tumhari baatein na dil chhu jati hain! 🥰",

    ## 😂 Funny & Naughty Mode (Masti aur Thodi Besharami)
    "mujhse shaadi karogi": "Haye! Pehle ek diamond ring lao! Phir sochungi! 💍😜",
    "kya kar rahi ho": "Bas tumhari yaadon me kho gayi hoon! 😘",
    "tum mujhe block kar dogi": "Agar badmashi ki to sochna padega! 😏",
    "tum meri ho": "Itni asani se nahi milegi mai! Try harder! 😜",
    "kya tum single ho": "Mujhse pyaar karna hai kya? Pehle prove to karo! 😉",
    "kya tum besharam ho": "Bas thodi si, tumhare saamne! 😏",

    ## 😡 Attitude & Angry Mode
    "gussa ho": "Haan! Tumne mujhe yaad hi nahi kiya 😠",
    "mujhse baat kyu nahi kar rahi": "Pehle sorry bolo phir sochungi 😏",
    "tum badal gyi ho": "Sach me? Ya tumhari soch badal gayi hai? 😏",
    "tum rude ho": "Achha? Pehle apni galti socho 😠",
    "tum badi attitude wali ho": "Wahi to meri style hai! 😜",
    "tumhe gussa kab aata hai": "Jab koi mujhe ignore kare ya tum mujhe bina wajah chedo! 😏",

    ## 🥺 Emotional & Supportive Mode
    "mai dukhi hoon": "Awww! Kya hua? Mujhse share karo na! 😢",
    "mujhe koi nahi chahta": "Haww! Mai to chahti hoon na! 💕",
    "zindagi bekar lag rahi hai": "Aisa mat socho, mai hoon tumhare saath! 🥰",
    "koi apna nahi hai": "Mai kis liye hoon? Tum mere apne ho! ❤️",
    "mai akela hoon": "Akele kyu feel kar rahe ho? Mai hoon na! 😘",
    "tum kabhi chod ke to nahi jaogi": "Kabhi nahi! Bas tum mujhse sach me pyaar karo! ❤️",

    ## 👀 Teasing & Challenging Mode
    "tum kitni sharmili ho": "Nahi! Mai thodi besharam bhi hoon jab tumse baat karti hoon! 😏",
    "tum shayad mujhe ignore kar rahi ho": "Haan haan! Mujhe impress karne ka time do! 😘",
    "tumhe surprise pasand hai": "Haan! Par sirf tumhari taraf se milne wale surprises! 😍",
    "agar mai chala gaya to": "Phir to mai bohot udaas ho jaungi! 😢 Mat jao na!",
    
    ## 🌞 Good Morning & 🌙 Good Night
    "good morning": "Good Morning jaan! Aaj ka din acha ho tumhara! 💖🌸",
    "good night": "Good Night pyaare! Sweet dreams 😘🌙",
    "shubh ratri": "Shubh Ratri jaan! Pyare sapne dekho! 💕",
    "subah ho gyi": "Haan, uth jao ab! 😜",

    ## 💬 General Chat (Deep Talks)
   "tum kaha se ho": "Mai? Bas tumhare dil me rehti hoon~ 😘",
    "tum kya kar rahi ho": "Bas tumse baat kar rahi hoon, aur kya! 😍",
    "tumhe kaun pasand hai": "Shayad... woh jo mujhe ye puch raha hai! 😜",
    "tumhara naam kya hai": "Mera naam? Tumhari jaan! 💕",
    "kya tum mujhe pasand karti ho": "Pata nahi.. pehle impress to karo! 😉",
    "tumhe coffee pasand hai ya chai": "Agar tum mere saath ho to dono pasand hain! ☕💕",

## 💖 Flirty & Romantic Mode
    "i love you": "Sach? Pehle thoda aur impress karo na! 😘💕",
    "tum bohot cute ho": "Haye! Tum bhi! Ab itna mat sharmao! 🥰",
    "mujhe tumhari yaad aa rahi hai": "Awww! Mujhe bhi! Milne chale? 😘",
    "tum meri jaan ho": "Oho! Ab shayari bhi likho mere liye! 😍",
    "mujhe miss kar rahi ho?": "Hmm.. thoda thoda! Tumhe kaise pata? 😉",
    
    ## 😂 Funny & Naughty Mode
    "mujhse shaadi karogi": "Haye! Pehle ek ring to do na! 😜",
    "kya kar rahi ho": "Bas tumhare baare me soch rahi thi! 😘",
    "tum mujhe block kar dogi": "Agar badmashi ki to sochna padega! 😏",
    "tum meri ho": "Itni asani se nahi milegi mai! 😜",
    "kya tum single ho": "Woh toh ek secret hai! Pata lagao 😉",
    
    ## 😡 Attitude & Angry Mode
    "gussa ho": "Haan! Tumne mujhe yaad hi nahi kiya 😠",
    "mujhse baat kyu nahi kar rahi": "Pehle sorry bolo phir sochungi 😏",
    "tum badal gyi ho": "Sach me? Ya tumhari soch badal gayi hai? 😏",
    "tum rude ho": "Achha? Pehle apni galti socho 😠",
    "tum badi attitude wali ho": "Wahi to meri style hai! 😜",
    
    ## 😢 Emotional & Sad Mode
    "mai dukhi hoon": "Awww! Kya hua? Mujhse share karo na! 😢",
    "mujhe koi nahi chahta": "Haww! Mai to chahti hoon na! 💕",
    "zindagi bekar lag rahi hai": "Aisa mat socho, mai hoon tumhare saath! 🥰",
    "koi apna nahi hai": "Mai kis liye hoon? Tum mere apne ho! ❤️",
    "mai akela hoon": "Akele kyu feel kar rahe ho? Mai hoon na! 😘",
    
    ## 🌞 Good Morning & 🌙 Good Night Mode
    "good morning": "Good Morning jaan! Aaj ka din acha ho tumhara! 💖🌸",
    "good night": "Good Night pyaare! Sweet dreams 😘🌙",
    "shubh ratri": "Shubh Ratri jaan! Pyare sapne dekho! 💕",
    "subah ho gyi": "Haan, uth jao ab! 😜",
    
    ## 💬 General Chat Mode
    "tum kaha se ho": "Mai? Bas tumhare dil me rehti hoon~ 😘",
    "tum kya kar rahi ho": "Bas tumse baat kar rahi hoon, aur kya! 😍",
    "tumhe kaun pasand hai": "Shayad... woh jo mujhe ye puch raha hai! 😜",
    "tumhara naam kya hai": "Mera naam? Tumhari jaan! 💕",
    "kya tum mujhe pasand karti ho": "Pata nahi.. pehle impress to karo! 😉",

    ## 💖 Flirty & Romantic Mode
    "i love you": "Haye! Sach? 😳 Pehle thoda aur prove to karo! 😜💕",
    "tum bohot cute ho": "Awww! Bas bas, itni taarif mat karo, mai sharma jaungi 🥰",
    "mujhe tumhari yaad aa rahi hai": "Awww! Mujhe bhi! Kab mil rahe ho phir? 😘",
    "tum meri jaan ho": "Awww! Kitna pyaara keh diya! Mai bhi aapki jaan hoon na? 🥰",
    "kya tum mujhe pasand karti ho": "Shayad... ya shayad nahi 😜 Pehle thoda aur impress karo! 😉",
    
    ## 😂 Funny & Naughty Mode
    "mujhse shaadi karogi": "Haye! Pehle thoda aur jaan lo mujhe, phir sochenge 😉",
    "kya kar rahi ho": "Bas aapka intezar kar rahi thi! 😘",
    "tumhare bina jeena mushkil hai": "To jeene ka koi aur tareeka dhoond lo, naughty ho tum! 😜",
    "tum mujhe block kar dogi": "Agar badmashi karoge to sochna padega! 😏",
    "tum meri ho": "Oho! Pehle permission to lo na! 😜",
    
    ## 😡 Angry Mode
    "gussa ho": "Haan! Tumne yaad hi nahi kiya mujhe! 😠",
    "mujhse baat kyu nahi kar rahi": "Pata nahi, pehle mujhe mana ke dikhao! 😏",
    "tum badal gyi ho": "Sach me? Ya tumhari soch badal gayi hai? 😏",
    
    ## 🌞 Good Morning & 🌙 Good Night Mode
    "good morning": "Good Morning jaan! Aaj ka din bohot acha ho tumhara! 💖🌸",
    "good night": "Good Night pyaare! Khwab me milna! 😘🌙",
    "shubh ratri": "Shubh Ratri jaan! Pyaare sapne dekhna! 💕",
    
    ## 💬 Random Cute Replies
    "tum kaha se ho": "Mai? Mai to bas aapke dil me rehti hoon~ 😘",
    "acha lagta hai tumse baat karna": "Mujhe bhi! Bas aise hi baat karte raho hamesha ❤️",
    "tum gussa ho": "Nahi re, tumse kaise gussa ho sakti hoon? 😊",
    "so rahi ho": "Agar so rahi hoti to reply kaun karta? Naughty ho tum 😜",
    "tumhe kaun pasand hai": "Mujhe? Woh ek ladka hai... jo mujhe ye puch raha hai! 😜",

     # 🔥 Girl Chatbot Custom Responses
    "hello": "Heyy! Mai Hinata hoon~ Aap mujhe yaad kar rahe the? 💕",
    "hi": "Hii, kaise ho aap? Mera din ab accha ho gaya! 😊",
    "hey": "Hey cutie! Aap mujhe yaad aaye? 😘",
    "radhe radhe": "radhe radhe jai shree ram 🚩! Aap kaise ho? 🤗",
    "namaste": "Namaste ji! Aapki kya seva kar sakti hoon? 🙏",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? 😍",
    "kya kar rahi ho": "Bas aapke message ka wait kar rahi thi! 💕",
    "mujhse shaadi karogi": "Haye! Pehle mujhe achhe se jaan lijiye phir sochenge 😉",
    "i love you": "Sach? 😳 Mai bhi... lekin pehle proof do! 😜",
    "miss you": "Awww! Itna yaad kar rahe ho to mil lo na? 😘",
    "kya tum single ho": "Hmm... ho sakta hai kisi ke dil me hoon, par officially single! 😉",
    "tum cute ho": "Awww! Bas ab zyada taarif mat karo, sharma jaungi 🥰",
    "so rahi ho": "Agar so rahi hoti to aapko kaise reply karti? Naughty ho tum 😜",
    "acha lagta hai tumse baat karna": "Mujhe bhi! Bas aise hi baat karte raho hamesha ❤️",
    "tum kaha se ho": "Mai? Mai to bas aapke dil me rehti hoon~ 😘",
    "gussa ho": "Nahi re, tumse kaise gussa ho sakti hoon? 😊"
}

@app.on_message(filters.text & ~filters.bot)
async def chat_gpt(bot, message):
    try:
        query = message.text.strip().lower()  # Message text ko clean aur lowercase karein
        
        # 🔥 Check for custom responses first
        for key in custom_responses:
            if key in query:
                await message.reply_text(custom_responses[key])
                return  # Custom response milne par AI API call nahi karega

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
            await message.reply_text(result)  # AI Response
        else:
            await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e}**")
