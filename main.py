from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

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

# حذف الملصقات والصور المتحركة
@bot.on_message(filters.group & (filters.sticker | filters.animation))
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

    links = [
        "http://",
        "https://",
        "t.me/",
        "telegram.me/",
        ".com",
        ".net"
    ]

    if any(link in text for link in links):

        try:
            member = await message.chat.get_member(
                message.from_user.id
            )

            if str(member.status) in [
                "ChatMemberStatus.OWNER",
                "ChatMemberStatus.ADMINISTRATOR"
            ]:
                return

            await message.delete()

            user_id = message.from_user.id

            warnings[user_id] = warnings.get(user_id, 0) + 1

            if warnings[user_id] >= 3:
                await message.chat.ban_member(user_id)

                await message.reply_text(
                    f"🚫 تم حظر {message.from_user.mention}"
                )
            else:
                await message.reply_text(
                    f"⚠️ تحذير {warnings[user_id]}/3"
                )

        except Exception as e:
            print(e)

# معلومات العضو
@bot.on_message(filters.command("info") & filters.reply)
async def info(client, message):

    user = message.reply_to_message.from_user

    username = (
        f"@{user.username}"
        if user.username
        else "لا يوجد"
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
async def ban_user(client, message):

    user = message.reply_to_message.from_user

    await message.chat.ban_member(user.id)

    await message.reply_text(
        "🚫 تم حظر العضو"
    )

# طرد
@bot.on_message(
    filters.command("kick")
    & filters.reply
    & filters.user(ADMINS)
)
async def kick_user(client, message):

    user = message.reply_to_message.from_user

    await message.chat.ban_member(user.id)
    await message.chat.unban_member(user.id)

    await message.reply_text(
        "👢 تم طرد العضو"
    )

# كتم
@bot.on_message(
    filters.command("mute")
    & filters.reply
    & filters.user(ADMINS)
)
async def mute_user(client, message):

    user = message.reply_to_message.from_user

    await client.restrict_chat_member(
        message.chat.id,
        user.id,
        ChatPermissions()
    )

    await message.reply_text(
        "🔇 تم كتم العضو"
    )

# فك الكتم
@bot.on_message(
    filters.command("unmute")
    & filters.reply
    & filters.user(ADMINS)
)
async def unmute_user(client, message):

    user = message.reply_to_message.from_user

    permissions = ChatPermissions(
        can_send_messages=True
    )

    await client.restrict_chat_member(
        message.chat.id,
        user.id,
        permissions
    )

    await message.reply_text(
        "🔊 تم فك الكتم"
    )

# القوانين
@bot.on_message(filters.command("rules"))
async def rules(client, message):

    await message.reply_text(
        "📜 قوانين المجموعة:\n\n"
        "1- منع السب والشتم\n"
        "2- منع الروابط\n"
        "3- منع السبام\n"
        "4- احترام الجميع\n"
        "5- الالتزام بتعليمات الإدارة"
    )

print("Bot Started...")
bot.run()
