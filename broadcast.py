"""
╔══════════════════════════════════════════╗
║      TIVRA PAY BOT — broadcast.py        ║
║   /broadcast reply karke — sab users ko  ║
╚══════════════════════════════════════════╝

HOW TO USE:
  1. Koi bhi message bhejo (text / photo+caption / video+caption / document)
  2. Us message par REPLY karo aur type karo: /broadcast
  3. Bot automatically sab users ko wahi message bhejega
     — format, spacing, image/video sab SAME rahega

WHO CAN USE:
  Sirf ADMINS list mein jo IDs hain (config.py)
"""

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from config import ADMINS

# In-memory user store
# Production mein database use karo (MongoDB / SQLite)
# Bot start hone par sab users yahan save honge
USER_IDS: set = set()


def register_broadcast_handlers(app: Client):

    # ────────────────────────────────────────────
    # Auto-collect user IDs jab bhi koi message aaye
    # ────────────────────────────────────────────
    @app.on_message(filters.private & ~filters.bot)
    async def collect_user(client: Client, msg: Message):
        USER_IDS.add(msg.from_user.id)

    # ────────────────────────────────────────────
    # /broadcast — reply karke bhejo
    # ────────────────────────────────────────────
    @app.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_handler(client: Client, msg: Message):

        # 1. Admin check
        if msg.from_user.id not in ADMINS:
            await msg.reply_text("❌ <b>Tumhe ye command use karne ki permission nahi hai.</b>", parse_mode="html")
            return

        # 2. Reply check — kisi message par reply hona chahiye
        if not msg.reply_to_message:
            await msg.reply_text(
                "⚠️ <b>Kisi message par REPLY karke /broadcast bhejo.</b>\n\n"
                "<i>Example:\n"
                "1. Koi photo ya text message bhejo\n"
                "2. Us par reply karo: /broadcast</i>",
                parse_mode=enums.ParseMode.HTML
            )
            return

        broadcast_msg: Message = msg.reply_to_message
        total   = len(USER_IDS)
        success = 0
        failed  = 0
        blocked = 0

        if total == 0:
            await msg.reply_text("⚠️ <b>Abhi koi user registered nahi hai.</b>", parse_mode="html")
            return

        # 3. Progress message
        status_msg = await msg.reply_text(
            f"📤 <b>Broadcast shuru ho raha hai...</b>\n"
            f"👥 Total users: <b>{total}</b>",
            parse_mode=enums.ParseMode.HTML
        )

        # 4. Broadcast loop — message type detect karke copy karo
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

            # Har 50 users baad progress update karo
            if (success + failed + blocked) % 50 == 0:
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

            await asyncio.sleep(0.05)  # Rate limit se bachne ke liye

        # 5. Final report
        await status_msg.edit_text(
            f"✅ <b>Broadcast Complete!</b>\n\n"
            f"✅ Successfully sent: <b>{success}</b>\n"
            f"❌ Failed: <b>{failed}</b>\n"
            f"🚫 Blocked/Deleted: <b>{blocked}</b>\n"
            f"👥 Total users: <b>{total}</b>",
            parse_mode=enums.ParseMode.HTML
        )


# ==============================================================
# 📬 FORMAT-PRESERVING SEND
# Jaisa message hai — waisa SAME bhejta hai
# Text spacing, newlines, photo, video, document — sab same
# ==============================================================

async def _forward_exact(client: Client, user_id: int, msg: Message):
    """
    Message ko exactly copy karke bhejta hai.
    caption/text ka format, newlines sab preserve hota hai.
    """

    # Common kwargs
    caption    = msg.caption or None
    

    # ── Photo ────────────────────────────────────
    if msg.photo:
        await client.send_photo(
            chat_id=user_id,
            photo=msg.photo.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    # ── Video ────────────────────────────────────
    elif msg.video:
        await client.send_video(
            chat_id=user_id,
            video=msg.video.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    # ── Animation / GIF ──────────────────────────
    elif msg.animation:
        await client.send_animation(
            chat_id=user_id,
            animation=msg.animation.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    # ── Document ─────────────────────────────────
    elif msg.document:
        await client.send_document(
            chat_id=user_id,
            document=msg.document.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    # ── Audio ────────────────────────────────────
    elif msg.audio:
        await client.send_audio(
            chat_id=user_id,
            audio=msg.audio.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    # ── Voice ────────────────────────────────────
    elif msg.voice:
        await client.send_voice(
            chat_id=user_id,
            voice=msg.voice.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    # ── Sticker ──────────────────────────────────
    elif msg.sticker:
        await client.send_sticker(
            chat_id=user_id,
            sticker=msg.sticker.file_id,
        )

    # ── Pure Text ────────────────────────────────
    elif msg.text:
        await client.send_message(
            chat_id=user_id,
            text=msg.text,
            parse_mode=enums.ParseMode.HTML
            disable_web_page_preview=True,
        )
