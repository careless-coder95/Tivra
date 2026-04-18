"""
╔══════════════════════════════════════════╗
║      TIVRA PAY BOT — broadcast.py        ║
╚══════════════════════════════════════════╝
"""

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from config import ADMINS

USER_IDS: set = set()


def register_broadcast_handlers(app: Client):

    # ────────────────────────────────────────────
    # /broadcast — group=0 (highest priority)
    # ────────────────────────────────────────────
    @app.on_message(filters.command("broadcast") & filters.private, group=0)
    async def broadcast_handler(client: Client, msg: Message):

        # Admin check
        if msg.from_user.id not in ADMINS:
            await msg.reply_text(
                "❌ <b>Tumhe ye command use karne ki permission nahi hai.</b>",
                parse_mode=enums.ParseMode.HTML
            )
            return

        # Reply check
        if not msg.reply_to_message:
            await msg.reply_text(
                "⚠️ <b>Kisi message par REPLY karke /broadcast bhejo.</b>\n\n"
                "<b>Steps:</b>\n"
                "1️⃣ Bot mein koi message bhejo (text/photo/video)\n"
                "2️⃣ Us message par reply karo → <code>/broadcast</code>",
                parse_mode=enums.ParseMode.HTML
            )
            return

        broadcast_msg: Message = msg.reply_to_message
        total   = len(USER_IDS)
        success = 0
        failed  = 0
        blocked = 0

        if total == 0:
            await msg.reply_text(
                "⚠️ <b>Abhi koi user registered nahi hai.</b>\n"
                "<i>Users tab register hote hain jab wo bot se pehli baar baat karte hain.</i>",
                parse_mode=enums.ParseMode.HTML
            )
            return

        status_msg = await msg.reply_text(
            f"📤 <b>Broadcast shuru ho raha hai...</b>\n"
            f"👥 Total users: <b>{total}</b>",
            parse_mode=enums.ParseMode.HTML
        )

        for user_id in list(USER_IDS):
            try:
                await _forward_exact(client, user_id, broadcast_msg)
                success += 1

            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await _forward_exact(client, user_id, broadcast_msg)
                    success += 1
                except Exception:
                    failed += 1

            except (UserIsBlocked, InputUserDeactivated):
                blocked += 1
                USER_IDS.discard(user_id)

            except Exception:
                failed += 1

            done = success + failed + blocked
            if done % 50 == 0:
                try:
                    await status_msg.edit_text(
                        f"📤 <b>Broadcast chal raha hai...</b>\n\n"
                        f"✅ Sent: <b>{success}</b>\n"
                        f"❌ Failed: <b>{failed}</b>\n"
                        f"🚫 Blocked: <b>{blocked}</b>\n"
                        f"👥 Total: <b>{total}</b>",
                        parse_mode=enums.ParseMode.HTML
                    )
                except Exception:
                    pass

            await asyncio.sleep(0.05)

        await status_msg.edit_text(
            f"✅ <b>Broadcast Complete!</b>\n\n"
            f"✅ Successfully sent: <b>{success}</b>\n"
            f"❌ Failed: <b>{failed}</b>\n"
            f"🚫 Blocked/Deleted: <b>{blocked}</b>\n"
            f"👥 Total users: <b>{total}</b>",
            parse_mode=enums.ParseMode.HTML
        )

    # ────────────────────────────────────────────
    # User collect — group=1 (low priority)
    # /broadcast ke saath conflict nahi karega
    # ────────────────────────────────────────────
    @app.on_message(filters.private & ~filters.bot, group=1)
    async def collect_user(client: Client, msg: Message):
        if msg.from_user:
            USER_IDS.add(msg.from_user.id)


# ==============================================================
# 📬 EXACT FORMAT PRESERVE KARKE BHEJNA
# ==============================================================

async def _forward_exact(client: Client, user_id: int, msg: Message):
    caption    = msg.caption or None
    parse_mode = enums.ParseMode.HTML

    if msg.photo:
        await client.send_photo(
            chat_id=user_id,
            photo=msg.photo.file_id,
            caption=caption,
            parse_mode=parse_mode,
        )
    elif msg.video:
        await client.send_video(
            chat_id=user_id,
            video=msg.video.file_id,
            caption=caption,
            parse_mode=parse_mode,
        )
    elif msg.animation:
        await client.send_animation(
            chat_id=user_id,
            animation=msg.animation.file_id,
            caption=caption,
            parse_mode=parse_mode,
        )
    elif msg.document:
        await client.send_document(
            chat_id=user_id,
            document=msg.document.file_id,
            caption=caption,
            parse_mode=parse_mode,
        )
    elif msg.audio:
        await client.send_audio(
            chat_id=user_id,
            audio=msg.audio.file_id,
            caption=caption,
            parse_mode=parse_mode,
        )
    elif msg.voice:
        await client.send_voice(
            chat_id=user_id,
            voice=msg.voice.file_id,
            caption=caption,
            parse_mode=parse_mode,
        )
    elif msg.sticker:
        await client.send_sticker(
            chat_id=user_id,
            sticker=msg.sticker.file_id,
        )
    elif msg.text:
        await client.send_message(
            chat_id=user_id,
            text=msg.text,
            parse_mode=parse_mode,
            disable_web_page_preview=True,
        )
