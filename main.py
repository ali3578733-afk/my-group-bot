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

# --- هيكل القائمة ---
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1 م ⇦ أوامر القفل والفتح", callback_data="lock_cmd")],
        [InlineKeyboardButton("2 م ⇦ أعدادات المجموعة", callback_data="group_settings")],
        [InlineKeyboardButton("3 م ⇦ أوامر تفعيل وتعطيل", callback_data="toggle_cmd")],
        [InlineKeyboardButton("4 م ⇦ أوامر المسح", callback_data="clear_cmd")],
        [InlineKeyboardButton("🏦 أوامر البنك", callback_data="bank_cmd")]
    ])

# أمر الـ start بدون أزرار
@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply_text("👑 أهلاً بك! أنا بوت حماية المجموعات الخاص بك.\n\nقم بإضافتي لمجموعتك وارفعني مشرفاً لتفعيل الحماية.\nاكتب 'الاوامر' لعرض قائمة التحكم.")

# أمر الاوامر بالأزرار
@bot.on_message(filters.command("الاوامر"))
async def show_menu(client, message: Message):
    text = "مرحباً بك في قائمة الأوامر\n\nاختر من الأزرار أدناه:"
    await message.reply_text(text, reply_markup=get_main_menu())

@bot.on_message(filters.new_chat_members)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        await message.reply_text(f"أهلاً بك يا {member.mention} في المجموعة! 🌹 ورّد نورتنا.")

@bot.on_message(filters.command("طرد") & filters.group)
async def ban_user(client, message: Message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status.value in ["administrator", "owner"]:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            await client.ban_chat_member(message.chat.id, user_id)
            await message.reply_text(f"✈️ تم طرد العضو {message.reply_to_message.from_user.mention} بنجاح.")
        else:
            await message.reply_text("⚠️ يرجى الرد على رسالة الشخص الذي تريد طرده.")
    else:
        await message.reply_text("❌ هذا الأمر خاص بالمشرفين فقط.")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("جاري تشغيل السورس...")
    bot.run()
