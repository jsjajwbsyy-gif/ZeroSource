import os, asyncio, pytz, requests
from datetime import datetime
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

API_ID = 27503848 
API_HASH = 'a08a570b86888fecda16e0e5e0bdf2a5'
STRING_SESSION = 'AgGjrOgAgsDnSqJPf8AsAEvYktOQyG3WT1C6xdEEh5BgvaNEPVN5trc6olf0w6mZXnSbMJW0TGG73lhdPu22hnWqQds-ZVbriXgRsuaf1ftJidg-P9BVQeF3TvalSOm5XcpZ5urJN-qqbtA1KbTjNUDT-TMrMN00XTWuRFgEzLze-naW3pqNh9MVr6FHn6RV5L502lNslVHSqR8IZFbb1Im5OoaBL_Ekh_5LGfAP9icbrkBTEHHr3M12NUj9hK4frieOZGJWDzh-ucjWJLpNxFW_xWUml1lupnXu8iXYjECTK7NvJcL8lYvZ8NjVSTAtpEFpPO2FBhyQrjGewsZd3WYXmQ_GGwAAAAG6h-BKAA' 

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

TIME_NAME_WORK = False
AUTO_REPLY_LIST = {}

@client.on(events.NewMessage(outgoing=True, pattern=r'\.الاوامر'))
async def main_help(event):
    help_text = """
✦ ────『 **ZERO SOURCE** 』──── ✦
• `.م1` ➪ يوتيوب (تحميل خارجي)
• `.م3` ➪ الوقتي (.وقتي تشغيل)
• `.م4` ➪ الإدارة (.حظر | .طرد | .تثبيت)
• `.م5` ➪ الردود (.اضف_رد | .مسح_رد)
• `.م11` ➪ النشر (.كرر + عدد)
• `.م20` ➪ معلومات (.ايدي | .فحص)
✦ ────『 **ZERO SOURCE** 』──── ✦
    """
    await event.edit(help_text)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.تحميل (.*)'))
async def m1_dl(event):
    link = event.pattern_match.group(1)
    await event.edit("🔄 **جاري الطلب...**")
    async with client.conversation("@utubebot") as conv:
        await conv.send_message(link)
        res = await conv.get_response()
        await client.send_read_acknowledge(conv.chat_id)
        await client.send_message(event.chat_id, res)
        await event.delete()

async def time_name_task():
    global TIME_NAME_WORK
    while TIME_NAME_WORK:
        try:
            tz = pytz.timezone('Asia/Baghdad')
            curr = datetime.now(tz).strftime("%I:%M")
            await client(UpdateProfileRequest(first_name=f"ZERO | {curr}"))
            await asyncio.sleep(60)
        except: break

@client.on(events.NewMessage(outgoing=True, pattern=r'\.وقتي (تشغيل|ايقاف)'))
async def m3_time(event):
    global TIME_NAME_WORK
    status = event.pattern_match.group(1)
    TIME_NAME_WORK = (status == "تشغيل")
    if TIME_NAME_WORK: asyncio.create_task(time_name_task())
    await event.edit(f"⏰ تم {status} الوقتي.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.حظر'))
async def m4_ban(event):
    reply = await event.get_reply_message()
    if reply:
        await client.edit_permissions(event.chat_id, reply.sender_id, view_messages=False)
        await event.edit("🚫 تم الحظر.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.طرد'))
async def m4_kick(event):
    reply = await event.get_reply_message()
    if reply:
        await client.kick_participant(event.chat_id, reply.sender_id)
        await event.edit("👞 تم الطرد.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.تثبيت'))
async def m4_pin(event):
    reply = await event.get_reply_message()
    if reply:
        await client.pin_message(event.chat_id, reply.id)
        await event.edit("📌 تم التثبيت.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.اضف_رد (.*) (.*)'))
async def m5_add(event):
    AUTO_REPLY_LIST[event.pattern_match.group(1)] = event.pattern_match.group(2)
    await event.edit("✅ تم الحفظ.")

@client.on(events.NewMessage(incoming=True))
async def handle_r(event):
    if event.message.message in AUTO_REPLY_LIST:
        await event.reply(AUTO_REPLY_LIST[event.message.message])

@client.on(events.NewMessage(outgoing=True, pattern=r'\.كرر (\d+) (.*)'))
async def m11_rep(event):
    count, text = int(event.pattern_match.group(1)), event.pattern_match.group(2)
    await event.delete()
    for _ in range(count):
        await client.send_message(event.chat_id, text)
        await asyncio.sleep(0.3)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.ايدي'))
async def m20_id(event):
    reply = await event.get_reply_message()
    user_id = reply.sender_id if reply else event.sender_id
    await event.edit(f"🆔 الايدي: `{user_id}`")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.فحص'))
async def ping(event):
    await event.edit("🚀 **ZERO SOURCE IS ONLINE**")

print("ZERO SOURCE IS ONLINE")
client.start()
client.run_until_disconnected()
