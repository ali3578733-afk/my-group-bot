import os
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "سورس الحماية يعمل بنجاح! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

API_ID = int(os.environ.get("API_ID", "39262198"))
API_HASH = os.environ.get("API_HASH", "0bbcdfdbfd468898ecffd0e5cc91334c")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("my_group_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- القائمة الرئيسية ---
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1 م ⇦ أوامر القفل والفتح", callback_data="lock_cmd")],
        [InlineKeyboardButton("2 م ⇦ أعدادات المجموعة", callback_data="group_settings")],
        [InlineKeyboardButton("3 م ⇦ أوامر تفعيل وتعطيل", callback_data="toggle_cmd")],
        [InlineKeyboardButton("4 م ⇦ أوامر المسح", callback_data="clear_cmd")],
        [InlineKeyboardButton("🏦 أوامر البنك", callback_data="bank_cmd")]
    ])


# --- الأوامر ---
@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply_text("👑 أهلاً بك! أنا بوت حماية المجموعات الخاص بك.\n\nقم بإضافتي لمجموعتك وارفعني مشرفاً لتفعيل الحماية.\nاكتب 'الاوامر' لعرض قائمة التحكم.")

@bot.on_message(filters.command("الاوامر"))
async def show_menu(client, message: Message):
    await message.reply_text("مرحباً بك في قائمة الأوامر\n\nاختر من الأزرار أدناه:", reply_markup=get_main_menu())

@bot.on_message(filters.new_chat_members)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        await message.reply_text(f"أهلاً بك يا {member.mention} في المجموعة! 🌹 ورّد نورتنا.")

# --- معالج الأزرار ---
@bot.on_callback_query()
async def handle_buttons(client, callback_query):
    data = callback_query.data
    if data == "lock_cmd":
        await callback_query.message.edit_text("🔒 **قائمة أوامر القفل والفتح:**\n\n1. قفل التعديل\n2. قفل الملصقات", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_main")]]))
    elif data == "group_settings":
        await callback_query.message.edit_text("⚙️ **إعدادات المجموعة:**\n\nيمكنك التحكم في الترحيب والمغادرة من هنا.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_main")]]))
    elif data == "back_main":
        await callback_query.message.edit_text("مرحباً بك في قائمة الأوامر\n\nاختر من الأزرار أدناه:", reply_markup=get_main_menu())

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.run()
