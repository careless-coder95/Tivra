"""
╔══════════════════════════════════════════╗
║        TIVRA PAY BOT — start.py          ║
╚══════════════════════════════════════════╝
"""

from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    CallbackQuery,
    Message,
)
from config import ADMINS, REQUIRED_CHANNELS, WELCOME_IMAGE_BEFORE, WELCOME_IMAGE_AFTER

# ==============================================================
# TASK & EARN ke andar ke fake channels (prank wale)
# Ye real join check nahi karta — hamesha "join nahi kiya" bolta hai
# ==============================================================
TASK_CHANNELS = [
    {
        "link": "https://t.me/+JGntuGUw1PNhYTQ1",   # 👈 Apna link daalo
    },
    {
        "link": "https://t.me/+RpTKZ1_u3mk5NDFl",   # 👈 Apna link daalo
    },
]

# Task & Earn image
TASK_IMAGE = "https://files.catbox.moe/3rdf9a.jpg"  # 👈 Task wali image ka file_id

# Refer & Earn image
REFER_IMAGE = "https://files.catbox.moe/yp0cak.jpg"  # 👈 Refer wali image ka file_id yahan daalo


# ==============================================================
# 🎹 KEYBOARDS
# ==============================================================

def get_verify_keyboard():
    """Force join ke liye — sirf Verify button."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton("✅ Verify")]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_main_keyboard():
    """Main menu — verify ke baad."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💰 Balance")],
            [KeyboardButton("☎️ Support"),        KeyboardButton("🏦 Task & Earn")],
            [KeyboardButton("📲 Refer & Earn"),   KeyboardButton("💸 Claim ₹500")],
            [KeyboardButton("📤 Withdrawal"),     KeyboardButton("📊 Statistics")],
            [KeyboardButton("❓ How to Earn")],
        ],
        resize_keyboard=True,
    )


def get_task_keyboard():
    """Task & Earn ke andar — 2 join buttons + Claim ₹200 + Back."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💸 Claim ₹200")],
            [KeyboardButton("🔙 Back")],
        ],
        resize_keyboard=True,
    )


# ==============================================================
# 🔍 FSUB CHECK — Force Join
# ==============================================================

async def check_fsub(client: Client, user_id: int):
    if user_id in ADMINS:
        return True, []

    missing = []
    for i, ch in enumerate(REQUIRED_CHANNELS):
        try:
            member = await client.get_chat_member(ch["_id"], user_id)
            if member.status.value in ("left", "banned", "kicked"):
                missing.append({**ch, "index": i + 1})
        except Exception:
            missing.append({**ch, "index": i + 1})

    return (len(missing) == 0), missing


# ==============================================================
# 📨 FSUB INLINE BUTTONS — Join 1, Join 2, 2 per row
# ==============================================================

def get_fsub_inline(missing_channels: list):
    flat_buttons = []
    for ch in missing_channels:
        idx = ch.get("index", "?")
        flat_buttons.append(
            InlineKeyboardButton(text=f"𝗝𝗢𝗜𝗡 {idx} ", url=ch["link"])
        )

    rows = []
    for i in range(0, len(flat_buttons), 2):
        rows.append(flat_buttons[i:i+2])

    rows.append([InlineKeyboardButton("✅ Verify Karo", callback_data="verify_fsub")])
    return InlineKeyboardMarkup(rows)


def get_task_inline():
    """Task & Earn ke inline join buttons — hamesha dikhenge."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝟭", url=TASK_CHANNELS[0]["link"]),
            InlineKeyboardButton("𝗝𝗢𝗜𝗡 𝟮", url=TASK_CHANNELS[1]["link"]),
        ],
    ])


# ==============================================================
# 🏠 MAIN MENU SENDER
# ==============================================================

async def send_main_menu(client: Client, chat_id: int, user_name: str):

    # ✏️ MAIN MENU TEXT
    text = f"""<b>🏠 Main Menu</b>

👋 <b>Hello, {user_name}!</b>

Niche se apni service chunein."""

    await client.send_photo(
        chat_id=chat_id,
        photo=WELCOME_IMAGE_AFTER,
        caption=text,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=get_main_keyboard(),
    )


# ==============================================================
# 📌 REGISTER ALL HANDLERS
# ==============================================================

def register_handlers(app: Client):

    # ────────────────────────────────────────────
    # /start
    # ────────────────────────────────────────────
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client: Client, msg: Message):
        user_id   = msg.from_user.id
        user_name = msg.from_user.first_name

        if user_id in ADMINS:
            await send_main_menu(client, msg.chat.id, user_name)
            return

        joined, missing = await check_fsub(client, user_id)

        # ✏️ WELCOME TEXT — Force join se pehle
        welcome_before = f"""<b>👋 𝗛𝗲𝗹𝗹𝗼𝘄, <a href='tg://user?id={user_id}'>{user_name}</a>!</b>
        💐 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 𝗔𝗡𝗬𝗔 𝗕𝗢𝗧𝗦!
        🤑 𝗝𝗼𝗶𝗻 𝟱 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝗔𝗻𝗱 𝗚𝗲𝘁 ₹𝟯𝟴𝟬
        📌 𝗠𝘂𝘀𝘁 𝗝𝗼𝗶𝗻 𝗔𝗹𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝗧𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 𝗕𝗼𝘁
        ✔️ 𝗔𝗳𝘁𝗲𝗿 𝗝𝗼𝗶𝗻𝗶𝗻𝗴, 𝗖𝗹𝗶𝗰𝗸 𝗩𝗘𝗥𝗜𝗙𝗬 🔒"""

        # ✏️ WELCOME TEXT — Verify ke baad
        welcome_after = f"""<b>✅ Welcome, <a href='tg://user?id={user_id}'>{user_name}</a>!</b>

╔══════════════════════════════╗
║      <b>💳 TIVRA PAY BOT</b>        ║
║    Fast · Safe · Reliable    ║
╚══════════════════════════════╝

➻ Yahan apna welcome text likho.

✅ <b>Ab niche se apni service chunein!</b>"""

        if not joined:
            await client.send_photo(
                chat_id=msg.chat.id,
                photo=WELCOME_IMAGE_BEFORE,
                caption=welcome_before,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=get_fsub_inline(missing),
            )
            await client.send_message(
                chat_id=msg.chat.id,
                text="👇 <b>Sab join karne ke baad niche ka button dabao:</b>",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=get_verify_keyboard(),
            )
        else:
            await client.send_photo(
                chat_id=msg.chat.id,
                photo=WELCOME_IMAGE_AFTER,
                caption=welcome_after,
                parse_mode=enums.ParseMode.HTML,
            )
            await send_main_menu(client, msg.chat.id, user_name)

    # ────────────────────────────────────────────
    # ✅ VERIFY — Reply Keyboard
    # ────────────────────────────────────────────
    @app.on_message(filters.text & filters.private & filters.regex("^✅ Verify$"))
    async def verify_button_handler(client: Client, msg: Message):
        user_id   = msg.from_user.id
        user_name = msg.from_user.first_name
        joined, missing = await check_fsub(client, user_id)

        if joined:
            await msg.reply_text(
                "✅ <b>Verification successful! Ab bot use karo. 🎉</b>",
                parse_mode=enums.ParseMode.HTML,
            )
            await send_main_menu(client, msg.chat.id, user_name)
        else:
            await msg.reply_text(
                f"❌ <b>Abhi bhi {len(missing)} channel(s) join nahi kiye!</b>\n\nJoin karo phir dobara Verify dabao.",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=get_fsub_inline(missing),
            )

    # ────────────────────────────────────────────
    # ✅ VERIFY — Inline callback
    # ────────────────────────────────────────────
    @app.on_callback_query(filters.regex("^verify_fsub$"))
    async def verify_callback(client: Client, cb: CallbackQuery):
        user_id   = cb.from_user.id
        user_name = cb.from_user.first_name
        joined, missing = await check_fsub(client, user_id)

        if joined:
            await cb.answer("✅ Verified!", show_alert=False)
            await send_main_menu(client, cb.message.chat.id, user_name)
        else:
            await cb.answer(f"❌ Abhi bhi {len(missing)} channel(s) join nahi kiye!", show_alert=True)

    # ════════════════════════════════════════════════════════
    # 💰 BALANCE
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^💰 Balance$"))
    async def balance_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<b>💰 YOUR BALANCE</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan balance info likho.
➻ <b>Current balance, pending, total earned</b> etc."""

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML)

    # ════════════════════════════════════════════════════════
    # ☎️ SUPPORT
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^☎️ Support$"))
    async def support_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<b>☎️ SUPPORT</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan support info likho.
➻ <b>Working hours, contact method</b> etc."""

        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("👤 Contact Admin", url="https://t.me/youradmin")],
        ])

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML, reply_markup=inline_buttons)

    # ════════════════════════════════════════════════════════
    # 🏦 TASK & EARN — Prank system
    # Hamesha "join nahi kiya" bolta hai chahe join kare ya na kare
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^🏦 Task & Earn$"))
    async def task_earn_handler(client: Client, msg: Message):

        # ✏️ TASK & EARN TEXT — Yahan apna text likho
        text = f"""<b>🏦 TASK & EARN</b>
━━━━━━━━━━━━━━━━━━━━

➻ Niche diye channels join karo.
➻ Join karne ke baad <b>Claim ₹200</b> button dabao.

<i>Dono channels join karna zaroori hai!</i>"""

        await client.send_photo(
            chat_id=msg.chat.id,
            photo=TASK_IMAGE,
            caption=text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=get_task_inline(),       # Inline: Join 1 | Join 2
        )
        # Niche menu: Claim ₹200 + Back
        await client.send_message(
            chat_id=msg.chat.id,
            text="👇 <b>Channels join karne ke baad Claim karo:</b>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=get_task_keyboard(),
        )

    # ────────────────────────────────────────────
    # 💸 CLAIM ₹200 — Task & Earn ke andar (prank)
    # Hamesha same message — "join nahi kiya"
    # ────────────────────────────────────────────
    @app.on_message(filters.text & filters.private & filters.regex("^💸 Claim ₹200$"))
    async def claim_200_handler(client: Client, msg: Message):
        await msg.reply_text(
            "❌ <b>Aapne abhi tak dono channels join nahi kiye!</b>\n\n"
            "➻ Pehle dono channels join karo.\n"
            "➻ Phir Claim karo.\n\n"
            "<i>Bina join kiye claim nahi milega! 🙅</i>",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=get_task_keyboard(),
        )

    # ────────────────────────────────────────────
    # 🔙 BACK — Task & Earn se wapas main menu
    # ────────────────────────────────────────────
    @app.on_message(filters.text & filters.private & filters.regex("^🔙 Back$"))
    async def back_handler(client: Client, msg: Message):
        user_name = msg.from_user.first_name
        await send_main_menu(client, msg.chat.id, user_name)

    # ════════════════════════════════════════════════════════
    # 📲 REFER & EARN
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^📲 Refer & Earn$"))
    async def refer_earn_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<b>📲 REFER & EARN</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan refer & earn ka description likho.
➻ <b>Reward per referral, conditions</b> etc."""

        # ✏️ INLINE BUTTON — Yahan apna button set karo
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Share Referral Link", url="https://t.me/share/url?url=YOUR_LINK")],
            [InlineKeyboardButton("📋 My Referrals",        callback_data="my_referrals")],
        ])

        await msg.reply_photo(
            photo=REFER_IMAGE,
            caption=text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=inline_buttons,
        )

    # ════════════════════════════════════════════════════════
    # 💸 CLAIM ₹500
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^💸 Claim ₹500$"))
    async def claim_500_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<b>💸 CLAIM ₹500</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan claim ka description likho.
➻ <b>Conditions, steps, eligibility</b> etc."""

        # ✏️ INLINE BUTTON
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("💸 Claim Now", callback_data="do_claim_500")],
            [InlineKeyboardButton("📋 Conditions", url="https://t.me/yourchannel")],
        ])

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML, reply_markup=inline_buttons)

    # ════════════════════════════════════════════════════════
    # 📤 WITHDRAWAL
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^📤 Withdrawal$"))
    async def withdrawal_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<b>📤 WITHDRAWAL</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan withdrawal info likho.
➻ <b>Min amount, method, processing time</b> etc."""

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML)

    # ════════════════════════════════════════════════════════
    # 📊 STATISTICS
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^📊 Statistics$"))
    async def statistics_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<b>📊 STATISTICS</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan statistics info likho.
➻ <b>Total users, total paid, active users</b> etc."""

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML)

    # ════════════════════════════════════════════════════════
    # ❓ HOW TO EARN
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^❓ How to Earn$"))
    async def how_to_earn_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<b>❓ HOW TO EARN</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan earning guide likho.
➻ <b>Steps, tips, methods</b> etc."""

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML)
