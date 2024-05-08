import logging
import re
import os
import sys
import asyncio
from telethon import TelegramClient, events
import telethon.utils
from telethon.tl import functions
from telethon.tl.functions.channels import LeaveChannelRequest
from asyncio import sleep
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins, ChatAdminRights
from telethon.tl.functions.channels import EditBannedRequest
from datetime import datetime
from var import Var
from time import sleep
from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


logging.basicConfig(level=logging.INFO)

print("تبدأ البوت فى التشغيل.....")

Riz = TelegramClient('Riz', Var.API_ID, Var.API_HASH).start(bot_token=Var.BOT_TOKEN)


SUDO_USERS = []
for x in Var.SUDO: 
    SUDO_USERS.append(x)

@Riz.on(events.NewMessage(pattern="بونغ"))  
async def ping(e):
    if e.sender_id in SUDO_USERS:
        start = datetime.now()
        text = "بونغ"
        event = await e.reply(text, parse_mode=None, link_preview=None )
        end = datetime.now()
        ms = (end-start).microseconds / 1000
        await event.edit(f"**انا موجود** \n\n __بونغ__ !! `{ms}` مللي ثانية")


@Riz.on(events.NewMessage(pattern="طرد"))
async def kickall(event):
   if event.sender_id in SUDO_USERS:
     if not event.is_group:
         Reply = f"لاعب غير محترف !! استخدم Cmd هذا في المجموعة."
         await event.reply(Reply)
     else:
         await event.delete()
         RiZ = await event.get_chat()
         RiZoeLop = await event.client.get_me()
         admin = RiZ.admin_rights
         creator = RiZ.creator
         if not admin and not creator:
              return await event.reply("ليس لدي حقوق كافية !!")
         RiZoeL = await Riz.send_message(event.chat_id, "**مرحبًا !! أنا حي**")
         admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
         admins_id = [i.id for i in admins]
         all = 0
         kimk = 0
         async for user in event.client.iter_participants(event.chat_id):
             all += 1
             try:
                if user.id not in admins_id:
                    await event.client.kick_participant(event.chat_id, user.id)
                    kimk += 1
                    await asyncio.sleep(0.1)
             except Exception as e:
                    print(str(e))
                    await asyncio.sleep(0.1)
         await RiZoeL.edit(f"**تم طرد المستخدمين بنجاح ! \n\n مطرود:** `{kimk}` \n **المجموع:** `{all}`")
    

@Riz.on(events.NewMessage(pattern="بح"))
async def banall(event):
   if event.sender_id in SUDO_USERS:
     if not event.is_group:
         Reply = f"جار التحميل... ."
         await event.reply(Reply)
     else:
         await event.delete()
         RiZ = await event.get_chat()
         RiZoeLop = await event.client.get_me()
         admin = RiZ.admin_rights
         creator = RiZ.creator
         if not admin and not creator:
              return await event.reply("ليس لدي حقوق كافية !!")
         RiZoeL = await Riz.send_message(event.chat_id, "**جاري فشخ البار **")
         admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
         admins_id = [i.id for i in admins]
         all = 0
         bann = 0
         async for user in event.client.iter_participants(event.chat_id):
             all += 1
             try:
               if user.id not in admins_id:
                    await event.client(EditBannedRequest(event.chat_id, user.id, RIGHTS))
                    bann += 1
                    await asyncio.sleep(0.1)
             except Exception as e:
                   print(str(e))
                   await asyncio.sleep(0.1)
         await RiZoeL.edit(f"**مرحبا المستخدمين! \n\n تم تصفية:** `{bann}` \n **إجمالي عدد المستخدمين:** `{all}`")

    
@Riz.on(events.NewMessage(pattern="المحظورين"))
async def unban(event):
   if event.sender_id in SUDO_USERS:
     if not event.is_group:
         Reply = f"استخدم Cmd هذا في المجموعة."
         await event.reply(Reply)
     else:
         msg = await event.reply("البحث في قوائم المشاركين.")
         p = 0
         async for i in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
              rights = ChatBannedRights(until_date=0, view_messages=False)
              try:
                await event.client(functions.channels.EditBannedRequest(event.chat_id, i, rights))
              except FloodWaitError as ex:
                 print(f"النوم ل {ex.seconds} ثواني")
                 sleep(ex.seconds)
              except Exception as ex:
                 await msg.edit(str(ex))
              else:
                  p += 1
         await msg.edit("{}: {} غير محظور".format(event.chat_id, p))


@Riz.on(events.NewMessage(pattern="غادر"))
async def _(e):
    if e.sender_id in SUDO_USERS:
        rizoel = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        if len(e.text) > 7:
            bc = rizoel[0]
            bc = int(bc)
            text = "تمت مغادرة....."
            event = await e.reply(text, parse_mode=None, link_preview=None )
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("تركت بنجاح")
            except Exception as e:
                await event.edit(str(e))   
        else:
            bc = e.chat_id
            text = "تمت مغادرة....."
            event = await e.reply(text, parse_mode=None, link_preview=None )
            try:
                await event.client(LeaveChannelRequest(bc))
                await event.edit("تركت بنجاح")
            except Exception as e:
                await event.edit(str(e))   
          

@Riz.on(events.NewMessage(pattern="^تنشيط"))
async def restart(e):
    if e.sender_id in SUDO_USERS:
        text = "__إعادة التشغيل__ !!!"
        await e.reply(text, parse_mode=None, link_preview=None )
        try:
            await Riz.disconnect()
        except Exception:
            pass
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()


print("\n\n")
print("تم تشغيل البوت بنجاح 🏴‍☠️🏴‍☠️")

Riz.run_until_disconnected()
