import os
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# إعداد Flask ليعمل البوت على Railway
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# إعدادات البوت
API_ID = int(os.environ.get("API_ID", "39262198"))
API_HASH = os.environ.get("API_HASH", "0bbcdfdbfd468898ecffd0e5cc91334c")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("my_group_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# دالة الأزرار
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1 م ⇦ أوامر القفل والفتح", callback_data="lock_cmd")],
        [InlineKeyboardButton("2 م ⇦ أعدادات المجموعة", callback_data="group_settings")],
        [InlineKeyboardButton("3 م ⇦ أوامر تفعيل وتعطيل", callback_data="toggle_cmd")]
    ])

# أمر الـ start (بدون أزرار)
@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply_text("👑 أهلاً بك! أنا بوت حماية المجموعات.\nاكتب 'الاوامر' لعرض القائمة.")

# أمر الاوامر (بالأزرار)
@bot.on_message(filters.command("الاوامر"))
async def show_menu(client, message: Message):
    await message.reply_text("مرحباً بك في قائمة الأوامر:", reply_markup=get_main_menu())

# معالج الضغط على الأزرار
@bot.on_callback_query()
async def callback_handler(client, query):
    if query.data == "lock_cmd":
        await query.message.edit_text("🔒 قفل التعديل مفعل.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_main")]]))
    elif query.data == "back_main":
        await query.message.edit_text("مرحباً بك في قائمة الأوامر:", reply_markup=get_main_menu())

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run()
