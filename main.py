import telebot
import random
import string
import sqlite3

TOKEN = "BOT_TOKEN"
CHANNEL = "@CSNZEUS"

bot = telebot.TeleBot(TOKEN)

# DB
conn = sqlite3.connect("bot.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, ref_code TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS refs (user_id INTEGER PRIMARY KEY, count INTEGER DEFAULT 0)")
conn.commit()


def generate_ref():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()

    # kullanıcı var mı kontrol
    c.execute("SELECT ref_code FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()

    if not user:
        ref_code = generate_ref()
        c.execute("INSERT INTO users VALUES (?,?)", (user_id, ref_code))
        c.execute("INSERT INTO refs VALUES (?,0)", (user_id,))
        conn.commit()
    else:
        ref_code = user[0]

    # referral işlem
    if len(args) > 1:
        ref = args[1]

        c.execute("SELECT user_id FROM users WHERE ref_code=?", (ref,))
        owner = c.fetchone()

        if owner and owner[0] != user_id:
            if is_joined(user_id):
                c.execute("UPDATE refs SET count = count + 1 WHERE user_id=?", (owner[0],))
                conn.commit()

    # kanal kontrol
    if not is_joined(user_id):
        bot.send_message(
            message.chat.id,
            "🚨 Önce kanala katıl!\n\n👉 https://t.me/CSNZEUS"
        )
        return

    # referral link
    ref_link = f"https://t.me/zeuscasinodavet_bot?start={ref_code}"

    c.execute("SELECT count FROM refs WHERE user_id=?", (user_id,))
    count = c.fetchone()[0]

    bot.send_message(
        message.chat.id,
        f"✅ Hoşgeldin!\n\n"
        f"🔗 Davet linkin:\n{ref_link}\n\n"
        f"👥 Getirdiğin kişi: {count}"
    )


bot.polling(none_stop=True)