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
from config import ADMINS, OWNER_ID, REQUIRED_CHANNELS, WELCOME_IMAGE


# ==============================================================
# 🎹 KEYBOARDS
# ==============================================================

def get_verify_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("✅ Verify")]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💳 Tivra Pay"),  KeyboardButton("📞 Support")],
            [KeyboardButton("📢 Channel"),    KeyboardButton("📩 Contact Us")],
        ],
        resize_keyboard=True,
    )


# ==============================================================
# 🔍 FSUB CHECK — Public + Private dono support
# ==============================================================

async def check_fsub(client: Client, user_id: int):
    """
    Returns: (all_joined: bool, missing_list: list of dicts with index)
    """
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
# 📨 FSUB INLINE BUTTONS — Join 1, Join 2 style, 2 per row
# ==============================================================

def get_fsub_inline(missing_channels: list):
    """
    Missing channels ke buttons — [Join 1][Join 2] format, 2 per row.
    """
    flat_buttons = []
    for ch in missing_channels:
        idx = ch.get("index", "?")
        flat_buttons.append(
            InlineKeyboardButton(
                text=f"Join {idx} 🔗",
                url=ch["link"],
            )
        )

    # 2 buttons per row
    rows = []
    for i in range(0, len(flat_buttons), 2):
        rows.append(flat_buttons[i:i+2])

    # Verify button — full width
    rows.append([InlineKeyboardButton("✅ Verify Karo", callback_data="verify_fsub")])

    return InlineKeyboardMarkup(rows)


# ==============================================================
# 🏠 MAIN MENU SENDER
# ==============================================================

async def send_main_menu(client: Client, chat_id: int, user_name: str):
    # ──────────────────────────────────────────────
    # ✏️ MAIN MENU TEXT — Yahan apna text likho
    # ──────────────────────────────────────────────
    text = f"""<b>🏠 Main Menu</b>

👋 <b>Hello, {user_name}!</b>

Niche se apni service chunein:

💳 <b>Tivra Pay</b>   — Payment gateway
📞 <b>Support</b>     — Help & assistance
📢 <b>Channel</b>     — Latest updates
📩 <b>Contact Us</b>  — Direct contact"""

    await client.send_message(
        chat_id=chat_id,
        text=text,
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

        # ──────────────────────────────────────────────
        # ✏️ WELCOME TEXT — Yahan apna text likho
        # ──────────────────────────────────────────────
        welcome_text = f"""<b>👋 Welcome, <a href='tg://user?id={user_id}'>{user_name}</a>!</b>

╔══════════════════════════════╗
║      <b>💳 TIVRA PAY BOT</b>        ║
║    Fast · Safe · Reliable    ║
╚══════════════════════════════╝

➻ Yahan apna welcome text likho.
➻ <b>Bold</b>, <i>italic</i>, <code>code</code> sab chal sakta hai.

{'⚠️ <b>Pehle niche diye channels join karo, phir ✅ Verify dabao.</b>' if not joined else '✅ <b>Ab niche se apni service chunein!</b>'}"""

        if not joined:
            await client.send_photo(
                chat_id=msg.chat.id,
                photo=WELCOME_IMAGE,
                caption=welcome_text,
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
                photo=WELCOME_IMAGE,
                caption=welcome_text,
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
                "✅ <b>Verification successful!</b>\n\nAb tum bot use kar sakte ho. 🎉",
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

    # ────────────────────────────────────────────
    # 💳 TIVRA PAY
    # ────────────────────────────────────────────
    @app.on_message(filters.text & filters.private & filters.regex("^💳 Tivra Pay$"))
    async def tivra_pay_handler(client: Client, msg: Message):

        # ✏️ TEXT
        text = f"""<b>💳 TIVRA PAY</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan Tivra Pay ka description likho.
➻ <b>Features, rates, process</b> — jo bhi batana ho.

<i>Example: UPI se payment karo, turant wallet mein aayega.</i>"""

        # ✏️ INLINE BUTTONS
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 Pay Now",    url="https://example.com/pay")],
            [InlineKeyboardButton("📋 View Rates", callback_data="view_rates")],
        ])

        # 1️⃣ Sirf Text:
        # await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML, reply_markup=inline_buttons)

        # 2️⃣ Image + Text + Buttons:
        # await msg.reply_photo(photo="FILE_ID", caption=text, parse_mode=enums.ParseMode.HTML, reply_markup=inline_buttons)

        # 3️⃣ Video + Text + Buttons ← Active
        await msg.reply_video(
            video="BAACAgEAAxkBAAMEaeJgowABHm--uQsp6-OY3SMZE5UkAAKXCQACxI4IRz0WM-vgGpjmOwQ",
            caption=text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=inline_buttons,
        )

    # ────────────────────────────────────────────
    # 📞 SUPPORT
    # ────────────────────────────────────────────
    @app.on_message(filters.text & filters.private & filters.regex("^📞 Support$"))
    async def support_handler(client: Client, msg: Message):

        # ✏️ TEXT
        text = f"""<b>📞 SUPPORT</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan support info likho.
➻ <b>Working hours, contact method</b> etc.

<i>Example: Mon–Sat, 10AM–8PM</i>"""

        # ✏️ INLINE BUTTONS
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("👤 Contact Admin", url="https://t.me/youradmin")],
            [InlineKeyboardButton("💬 Support Group", url="https://t.me/yoursupportgroup")],
        ])

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML, reply_markup=inline_buttons)

    # ────────────────────────────────────────────
    # 📢 CHANNEL
    # ────────────────────────────────────────────
    @app.on_message(filters.text & filters.private & filters.regex("^📢 Channel$"))
    async def channel_handler(client: Client, msg: Message):

        # ✏️ TEXT
        text = f"""<b>📢 OUR CHANNELS</b>
━━━━━━━━━━━━━━━━━━━━

➻ Hamare channels join karo latest updates ke liye.
➻ <b>Offers, news, announcements</b> sab wahan milenge."""

        # ✏️ INLINE BUTTONS
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Main Channel",   url="https://t.me/musicgroupxd")],
            [InlineKeyboardButton("🔔 Update Channel", url="https://t.me/phblicdarling")],
        ])

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML, reply_markup=inline_buttons)

    # ────────────────────────────────────────────
    # 📩 CONTACT US
    # ────────────────────────────────────────────
    @app.on_message(filters.text & filters.private & filters.regex("^📩 Contact Us$"))
    async def contact_us_handler(client: Client, msg: Message):

        # ✏️ TEXT
        text = f"""<b>📩 CONTACT US</b>
━━━━━━━━━━━━━━━━━━━━

➻ Yahan contact details likho.
➻ <b>Email, Telegram, WhatsApp</b> — jo bhi relevant ho.

<i>Example: Business inquiries ke liye direct message karo.</i>"""

        # ✏️ INLINE BUTTONS
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 WhatsApp",    url="https://wa.me/91XXXXXXXXXX")],
            [InlineKeyboardButton("✉️ Telegram DM", url="https://t.me/youradmin")],
        ])

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML, reply_markup=inline_buttons)
