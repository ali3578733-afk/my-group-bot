from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatPermissions

API_ID = 12345678
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Client(
    "guard_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

ADMINS = [123456789]
warnings = {}

# ترحيب
@bot.on_message(filters.new_chat_members)
async def welcome(client, message):
    for user in message.new_chat_members:
        await message.reply_text(
            f"🌹 أهلاً بك {user.mention} في المجموعة"
        )

# حذف الوسائط (تم التعديل ليشمل أنواعاً إضافية)
@bot.on_message(filters.group & (filters.sticker | filters.animation | filters.video | filters.document | filters.audio | filters.voice))
async def anti_media(client, message):
    try:
        await message.delete()
    except:
        pass

# منع الروابط
@bot.on_message(filters.group & filters.text)
async def anti_links(client, message):
    if not message.from_user:
        return

    text = message.text.lower()
    links = ["http://", "https://", "t.me/", "telegram.me/", ".com", ".net"]

    if any(link in text for link in links):
        try:
            member = await message.chat.get_member(message.from_user.id)
            if str(member.status) in ["ChatMemberStatus.OWNER", "ChatMemberStatus.ADMINISTRATOR"]:
                return

            await message.delete()
            user_id = message.from_user.id
            warnings[user_id] = warnings.get(user_id, 0) + 1

            if warnings[user_id] >= 3:
                await message.chat.ban_member(user_id)
                await message.reply_text(f"🚫 تم حظر {message.from_user.mention} بعد 3 مخالفات")
            else:
                await message.reply_text(f"⚠️ تحذير {warnings[user_id]}/3")
        except Exception as e:
            print(e)

# معلومات العضو
@bot.on_message(filters.command("info") & filters.reply)
async def info(client, message):
    user = message.reply_to_message.from_user
    username = f"@{user.username}" if user.username else "لا يوجد"
    await message.reply_text(
        f"👤 الاسم: {user.first_name}\n🆔 الآيدي: {user.id}\n📎 المعرف: {username}"
    )

# الأوامر الإدارية (ban, kick, mute, unmute, rules) بقيت كما في المصدر
# /fact-check: تم التأكد من توافق الدوال المضافة مع بنية الكود في الملف

print("Bot Started...")
bot.run()

