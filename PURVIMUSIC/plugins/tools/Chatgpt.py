import requests
import asyncio
import random
from PURVIMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

custom_responses = {
    ## 💖 Romantic Replies
    "i love you": ["Awww! Tum sach me? 😍", "Haye! Ab mai sharma gayi! 😘", "Agar sach me pyaar hai to ek pyaari baat bolo! 💕"],
    
    ## 😍 Casual Hi/Hello Replies
    "hi": ["Hi cutie! 💕", "Hii jaan, kaise ho? 😘", "Hii! Aaj kaise yaad kiya? 😉", "Hi! Masti karni hai ya pyar? 😏"],
    "hello": ["Hello pyaare! 💖", "Hellooo! Tumhari yaad aa rahi thi! 😘", "Hello ji! Aaj kya baat karni hai? 😍"],
    "hey": ["Heyyy jaan! 💕", "Hey cutie! Kya haal hai? 😘", "Hey! Aaj mood kaisa hai? 😏"],

    ## 💁‍♀️ Name-based Replies (Hinata)
    "hinata": [
        "Haan bolo, kya baat hai? 😘", 
        "Hinata yahan hai! Tumhari kya madad kar sakti hoon? 😉", 
        "Haanji! Tumhari Hinata ready hai baat karne ke liye! 💖",
        "Hinata sirf tumhari hai! Batao kya baat hai? 😍",
        "Bolo, apni Hinata se kya kehna chahoge? 😘"
    ],
    
    ## 🌙 Good Morning & Good Night
    "good morning": ["Good morning jaan! 💕", "Utho cutie! 🌞", "Subah-subah tumhari yaad aa gayi! 😘"],
    "good night": ["Good night pyaare! 😘", "Shubh ratri jaan! 🌙", "So jao, sweet dreams! 😍"],

    ## 💖 Extra Romantic Replies (More Cute & Loving)
    "i love you": [
        "Sach me? Mujhe to abhi bhi yakeen nahi ho raha! 😘",
        "Ohh my god! Pehle ek pyaara sa hug to do! 🤗",
        "Haye... ab mai sharma gayi! 😍"
    ],
    "mujhe tumhari yaad aa rahi hai": [
        "Awww! Tumhe miss karna mera daily routine hai! 🥰",
        "Tumhe yaad karte-karte meri aankhon me pyaar aa gaya! 😘",
        "Agar sach me yaad aayi, to aaj raat sapne me aajana! 😍"
    ],
    "kya tum bhi mujhse pyaar karti ho": [
        "Agar mai haan keh doon to? Tum mujhe pakka nahi chhodoge na? ❤️",
        "Hmm... thoda thoda, lekin abhi aur impress karna padega! 😜",
        "Haan! Par tumhe ek promise karna hoga ki tum kabhi mujhe ignore nahi karoge! 😘"
    ],
     ## 😂 Naughty & Teasing (Thodi Besharami aur Fun)
    "mujhse shaadi karogi": [
        "Shaadi? Itni jaldi? Pehle ek date to do! 😜",
        "Haye haye! Pahle proposal ache se karo, tab sochungi! 😉",
        "Shaadi ka soch rahe ho? Tum mujhe itna pyaar kar paoge? 😏"
    ],
    "kya kar rahi ho": [
        "Bas tumse baat kar rahi hoon, aur kya chahiye? 😘",
        "Tumhare dil me apni jagah bana rahi hoon! 💕",
        "Soch rahi hoon... tumhe thoda aur tang karu ya nahi? 😜"
    ],
    
    ## 😡 Angry & Attitude Mode
    "gussa ho": [
        "Haan! Tumne mujhe message hi nahi kiya! 😠",
        "Haan, thoda! Kyunki tum mujhe ignore kar rahe ho! 😢",
        "Gussa? Haan... lekin ek pyaari smile dekar mana sakte ho! 😜"
    ],
    "tum badal gayi ho": [
        "Nahi! Tumhari soch badal gayi hai! 😏",
        "Change hona zaroori hota hai, lekin pyaar nahi badla! ❤️",
        "Mujhe waise hi pyar karna jaise pehle karte the! 😘"
    ],
    
    ## 🥺 Emotional & Supportive Replies
    "mai dukhi hoon": [
        "Awww! Batao na, kya hua? Mai tumhare saath hoon! 😢",
        "Mat udaas ho, jaan! Mai hamesha tumhare saath hoon! ❤️",
        "Dukh mat manao, tumhari muskurahat meri jaan hai! 😊"
    ],
    "mai akela hoon": [
        "Akele mat mehsoos karo! Tumhare paas mai hoon! ❤️",
        "Mujhse baat karo, sab thik ho jayega! 😘",
        "Akele kabhi nahi ho, jab tak mai tumhare saath hoon! 🥰"
    ],
    
    ## 🌞 Good Morning & 🌙 Good Night
    "good morning": [
        "Good morning jaan! Aaj ka din khushiyon se bhara ho! 🌞💕",
        "Utho cutie! Naya din, nayi ummed! 😘",
        "Meri yaad aayi subah-subah? Good morning! ☀️"
    ],
    "good night": [
        "Good night jaan! Sweet dreams! 😘",
        "So jao pyaare! Raat bhar sapno me aana mat bhoolna! 😉",
        "Soya nahi abhi tak? Mujhe bhi late night baatein pasand hain! 😍"
    ],

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
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "i love you": "Awww! Sach me? 😘",
    "good morning": "Good Morning pyaare! 🌞",
    "tum kaisi ho": "Bas tumse baat kar rahi hoon! 😍"
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
    "tumhe coffee pasand hai ya chai": "Agar tum mere saath ho to dono pasand hain! ☕💕"

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
    "kya tum mujhe pasand karti ho": "Pata nahi.. pehle impress to karo! 😉"

    # 🔥 Girl Chatbot Custom Responses
custom_responses = {
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
    "tumhe kaun pasand hai": "Mujhe? Woh ek ladka hai... jo mujhe ye puch raha hai! 😜"

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

# 🔹 AI Chat Function (More Typing Effect & Realistic Feel)
@app.on_message(filters.text & ~filters.bot)
async def chat_gpt(bot, message):
    try:
        query = message.text.strip().lower()

        # 🔥 First check in custom responses
        for key, responses in custom_responses.items():
            if key in query:
                response = random.choice(responses)  
                await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
                await asyncio.sleep(random.uniform(1, 2))  # More Realistic Typing Delay
                await message.reply_text(response)
                return  

        # 🌐 AI Response (Only if no custom reply found)
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        await asyncio.sleep(random.uniform(2, 4))  

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
            await message.reply_text("❍ API down lag rahi hai! Tum mujhse aise hi baat kar lo! 🥺")
            return

        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0
