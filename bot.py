import os
import sqlite3
import telebot
import google.generativeai as genai
from gtts import gTTS

# --- YAHAN APNI DETAILS DAALEIN ---
TELEGRAM_TOKEN = "8827748908:AAGFuI27nD1tPGB14e54GajHHbt8u-LQLN0"
GEMINI_API_KEY = "AIzaSyCuc3J112-RmgPpJnTRkzOmDOhOJ_hK87s"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Database Setup (Topic save karne ke liye)
conn = sqlite3.connect('bot_database.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_topics (
        user_id INTEGER PRIMARY KEY,
        topic TEXT
    )
''')
conn.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Namaste! Main aapka Automated Script Bot hoon.\n\n"
        "📌 Mujhe apni service/business ka topic bhejiye (jaise: 'Digital Marketing'), "
        "main roz us par AI script aur voiceover tayar karunga!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    topic = message.text
    
    # Topic Database mein save karein
    cursor.execute('INSERT OR REPLACE INTO user_topics (user_id, topic) VALUES (?, ?)', (user_id, topic))
    conn.commit()
    
    # Gemini AI se script banwayein
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Write a short promotional script in Hinglish for: {topic}")
        script = response.text
    except Exception as e:
        script = f"Topic saved: {topic}"

    bot.reply_to(message, f"✅ **Topic Saved Successfully!**\n\n📝 **Generated Script:**\n{script}")

if __name__ == "__main__":
    print("Bot cloud par chalu ho raha hai...")
    bot.infinity_polling()
