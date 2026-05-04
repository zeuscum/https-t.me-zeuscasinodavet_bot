import telebot
import random
import string

TOKEN = "8336168818:AAFFDZG9o-IGdvubWBVikSZbxcvFDZoIGN4"
CHANNEL = "@CSNZEUS"

bot = telebot.TeleBot(TOKEN)

users = {}
ref_counts = {}

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

    if user_id not in users:
        ref_code = generate_ref()
        users[user_id] = ref_code
        ref_counts[user_id] = 0

        if len(args) > 1:
            ref = args[1]
            for uid, code in users.items():
                if code == ref and uid != user_id:
                    if is_joined(user_id):
                        ref_counts[uid] += 1

    if not is_joined(user_id):
        bot.send_message(
            message.chat.id,
            "🚨 Önce kanala katıl!\n\n👉 https://t.me/CSNZEUS"
        )
        return

    ref_link = f"https://t.me/zeuscasinodavet_bot?start={users[user_id]}"

    bot.send_message(
        message.chat.id,
        f"✅ Hoşgeldin!\n\n"
        f"🔗 Davet linkin:\n{ref_link}\n\n"
        f"👥 Getirdiğin kişi: {ref_counts[user_id]}"
    )

bot.polling(none_stop=True)