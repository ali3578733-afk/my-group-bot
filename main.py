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
            f"🌹 أهلاً وسهلاً {user.mention} في المجموعة."
        )

# حذف الملصقات والصور المتحركة
@bot.on_message(filters.group & (filters.sticker | filters.animation))
async def delete_media(client, message):
    try:
        await message.delete()
    except:
        pass

# حذف الروابط + تحذيرات
@bot.on_message(filters.group & filters.text)
async def anti_links(client, message):
    if not message.from_user:
        return

    text = message.text.lower()

    if any(x in text for x in [
        "http://", "https://", "t.me/",
        "telegram.me/", ".com", ".net"
    ]):
        try:
            member = await message.chat.get_member(
                message.from_user.id
            )

            if member.status in ["administrator", "owner"]:
                return

            await message.delete()

            user_id = message.from_user.id
            warnings[user_id] = warnings.get(user_id, 0) + 1

            if warnings[user_id] >= 3:
                await message.chat.ban_member(user_id)
                await message.reply_text(
                    f"🚫 تم حظر {message.from_user.mention} بعد 3 مخالفات."
                )
            else:
                await message.reply_text(
                    f"⚠️ تحذير {warnings[user_id]}/3"
                )

        except:
            pass

# معلومات عضو
@bot.on_message(filters.command("info") & filters.reply)
async def info(client, message):
    user = message.reply_to_message.from_user

    username = (
        f"@{user.username}"
        if user.username else
        "لا يوجد"
    )

    await message.reply_text(
        f"👤 الاسم: {user.first_name}\n"
        f"🆔 الآيدي: {user.id}\n"
        f"📎 المعرف: {username}"
    )

# حظر
@bot.on_message(
    filters.command("ban")
    & filters.reply
    & filters.user(ADMINS)
)
async def ban(client, message):
    user = message.reply_to_message.from_user
    await message.chat.ban_member(user.id)
    await message.reply_text(
        f"🚫 تم حظر {user.mention}"
    )

# طرد
@bot.on_message(
    filters.command("kick")
    & filters.reply
    & filters.user(ADMINS)
)
async def kick(client, message):
    user = message.reply_to_message.from_user
    await message.chat.ban_member(user.id)
    await message.chat.unban_member(user.id)

    await message.reply_text(
        f"👢 تم طرد {user.mention}"
    )

# كتم
@bot.on_message(
    filters.command("mute")
    & filters.reply
    & filters.user(ADMINS)
)
async def mute(client, message):
    user = message.reply_to_message.from_user

    await client.restrict_chat_member(
        message.chat.id,
        user.id,
        ChatPermissions()
    )

    await message.reply_text(
        f"🔇 تم كتم {user.mention}"
    )

# فك الكتم
@bot.on_message(
    filters.command("unmute")
    & filters.reply
    & filters.user(ADMINS)
)
async def unmute(client, message):
    user = message.reply_to_message.from_user

    await client.restrict_chat_member(
        message.chat.id,
        user.id,
        ChatPermissions(
            can_send_messages=True
        )
    )

    await message.reply_text(
        f"🔊 تم فك كتم {user.mention}"
    )

# القوانين
@bot.on_message(filters.command("rules"))
async def rules(client, message):
    await message.reply_text(
        "📜 قوانين المجموعة:\n\n"
        "1- منع السب والشتم.\n"
        "2- منع الروابط.\n"
        "3- منع السبام.\n"
        "4- احترام الجميع.\n"
        "5- الالتزام بتعليمات الإدارة."
    )

print("Bot Started...")
bot.run()
