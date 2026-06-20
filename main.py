from telethon import TelegramClient, events
import asyncio

# تأكد من وضع بياناتك هنا
api_id = 1234567 
api_hash = 'YOUR_API_HASH'
bot_token = 'YOUR_BOT_TOKEN'

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# الذاكرة (سوف تفرغ عند إعادة التشغيل)
protection_status = {}

@client.on(events.NewMessage(pattern='^(قفل الملصقات|فتح الملصقات)$'))
async def toggle_protection(event):
    if not event.is_group:
        return

    # التحقق من صلاحيات المرسل (Admin)
    sender = await event.get_sender()
    perms = await event.client.get_permissions(event.chat_id, sender.id)
    
    if not (perms.is_admin or perms.is_creator):
        return # يتجاهل الأمر إذا لم يكن مشرفاً

    if 'قفل' in event.raw_text:
        protection_status[event.chat_id] = True
        await event.reply("🚫 تم تفعيل الحماية: الملصقات والمتحركات ممنوعة.")
    else:
        protection_status[event.chat_id] = False
        await event.reply("✅ تم إيقاف الحماية.")

@client.on(events.NewMessage)
async def handler(event):
    if event.is_group and protection_status.get(event.chat_id, False):
        # التأكد من أن الرسالة تحتوي على محتوى غير مرغوب
        if event.message.sticker or event.message.gif or event.message.video_note:
            try:
                # محاولة الحذف
                await event.delete()
            except Exception as e:
                # إذا فشل الحذف، غالباً البوت ليس مشرفاً
                print(f"فشل الحذف في مجموعة {event.chat_id}: {e}")

print("--- البوت يعمل الآن بكامل طاقته ---")
client.run_until_disconnected()
