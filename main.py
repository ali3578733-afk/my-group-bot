import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# --- الإعدادات ---
bot = Client("my_group_bot", 
             api_id=int(os.environ.get("API_ID", "39262198")), 
             api_hash=os.environ.get("API_HASH", "0bbcdfdbfd468898ecffd0e5cc91334c"), 
             bot_token=os.environ.get("BOT_TOKEN"))

ADMINS = [218073323] 

# --- الحماية (حذف الوسائط المخالفة) ---
@bot.on_message(filters.group & (filters.sticker | filters.animation))
async def anti_media(client, message):
    await message.delete()

# --- الترحيب التلقائي ---
@bot.on_message(filters.group & filters.new_chat_members)
async def welcome(client, message):
    for member in message.new_chat_members:
        await message.reply_text(f"أهلاً بك {member.mention} في مجموعتنا! نرجو الالتزام بالقوانين. 🌸")

# --- أمر معلومات العضو (للتفاعل) ---
@bot.on_message(filters.command("info") & filters.reply)
async def get_info(client, message):
    user = message.reply_to_message.from_user
    info = f"👤 المعلومات:\nالاسم: {user.first_name}\nالآيدي: `{user.id}`\nالمعرف: @{user.username}"
    await message.reply_text(info)

# --- أمر الحظر (للمدير) ---
@bot.on_message(filters.command("ban") & filters.reply & filters.user(ADMINS))
async def ban_user(client, message):
    user_id = message.reply_to_message.from_user.id
    await message.chat.ban_member(user_id)
    await message.reply_text("🚫 تم حظر العضو المخالف.")

# --- الأزرار ---
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 الألعاب", callback_data="games_menu")],
        [InlineKeyboardButton("🛡 أوامر الحماية", callback_data="shield_menu")]
    ])

@bot.on_message(filters.command("الاوامر"))
async def show_menu(client, message: Message):
    await message.reply_text("لوحة التحكم:", reply_markup=get_main_menu())

@bot.on_callback_query()
async def callback_handler(client, query):
    if query.data == "games_menu":
        await query.message.edit_text("الألعاب:\n1. XO (قيد التطوير)\n2. أسئلة ذكاء", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_main")]]))
    elif query.data == "shield_menu":
        await query.message.edit_text("الحماية مفعلة (حذف الملصقات والمتحركة).", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("رجوع 🔙", callback_data="back_main")]]))
    elif query.data == "back_main":
        await query.message.edit_text("لوحة التحكم:", reply_markup=get_main_menu())

bot.run()
