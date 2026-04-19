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

title="𝗔𝗡𝗬𝗔 𝗕𝗢𝗧𝗦"
rafer="https://t.me/Dkgkmemfcbot"


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
    text = f"""✅ 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘 𝗬𝗢𝗨𝗥 𝗧𝗔𝗦𝗞 𝗔𝗡𝗗 𝗘𝗔𝗥𝗡 𝗠𝗢𝗡𝗘𝗬 😄
    """

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
        welcome_before = f"""<blockquote expandable><b>👋 𝗛𝗲𝗹𝗹𝗼𝘄, <a href='tg://user?id={user_id}'>{user_name}</a>!</b></blockquote>
        <blockquote>
        💐 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 {title}!
        🤑 𝗝𝗼𝗶𝗻 𝟱 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝗔𝗻𝗱 𝗚𝗲𝘁 ₹𝟯𝟴𝟬
        📌 𝗠𝘂𝘀𝘁 𝗝𝗼𝗶𝗻 𝗔𝗹𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝗧𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 𝗕𝗼𝘁
        </blockquote> <blockquote>
        ✔️ 𝗔𝗳𝘁𝗲𝗿 𝗝𝗼𝗶𝗻𝗶𝗻𝗴, 𝗖𝗹𝗶𝗰𝗸 𝗩𝗘𝗥𝗜𝗙𝗬 🔒
        </blockquote>"""

        # ✏️ WELCOME TEXT — Verify ke baad
        welcome_after = f"""<blockquote expandable><b>👋🏻 𝗛𝗘𝗟𝗟𝗢, <a href='tg://user?id={user_id}'>{user_name}</a>!</b></blockquote>
        <blockquote>
        📝 𝗝𝗨𝗦𝗧 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘 𝗔𝗡𝗬 𝗧𝗔𝗦𝗞𝗦 𝗔𝗡𝗗 𝗘𝗔𝗥𝗡 𝗠𝗢𝗡𝗘𝗬 💰
        📲 𝗥𝗔𝗙𝗘𝗥 𝗔𝗡𝗗 𝗘𝗔𝗥𝗡 𝗠𝗢𝗥𝗘 𝗠𝗢𝗡𝗘𝗬. 
        📤 𝗗𝗜𝗥𝗘𝗖𝗧𝗟𝗬 𝗪𝗜𝗧𝗛𝗗𝗥𝗔𝗪𝗔𝗟 𝗜𝗡 𝗬𝗢𝗨 𝗨𝗣𝗜 / 𝗕𝗔𝗡𝗞 𝗔𝗖𝗖𝗢𝗨𝗡𝗧.
        </blockquote>
        <blockquote expandable>
        ✅ 𝗖𝗛𝗘𝗔𝗞𝗢𝗨𝗧 𝗔𝗟𝗟 𝗠𝗘𝗡𝗨 𝗕𝗨𝗧𝗧𝗢𝗡𝗦 𝗧𝗢 𝗜𝗡𝗧𝗥𝗔𝗖𝗧.
        </blockquote>
        """

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
                text="🤑 𝗝𝗼𝗶𝗻 𝟱 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝗔𝗻𝗱 𝗚𝗲𝘁 ₹𝟰𝟬𝟬 𝗬𝗼𝘂𝗿 𝗨𝗣𝗜",
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
                "✅ 𝗔𝗹𝗹 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗖𝗵𝗮𝗻𝗻𝗲𝗹𝘀 𝗛𝗮𝘃𝗲 𝗕𝗲𝗲𝗻 𝗝𝗼𝗶𝗻𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.",
                parse_mode=enums.ParseMode.HTML,
            )
            await send_main_menu(client, msg.chat.id, user_name)
        else:
            await msg.reply_text(
                f"❌ 𝗛𝗮𝘃𝗲𝗻'𝘁 𝗷𝗼𝗶𝗻𝗲𝗱 𝗲𝘃𝗲𝗻 {len(missing)} 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘆𝗲𝘁!\n ✅ 𝗝𝗼𝗶𝗻 𝗮𝗻𝗱 𝘁𝗵𝗲𝗻 𝗰𝗹𝗶𝗰𝗸 𝗩𝗲𝗿𝗶𝗳𝘆 𝗮𝗴𝗮𝗶𝗻.",
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
            await cb.answer(f"❌ 𝗛𝗮𝘃𝗲𝗻'𝘁 𝗷𝗼𝗶𝗻𝗲𝗱 𝗲𝘃𝗲𝗻 {len(missing)} 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘆𝗲𝘁!!", show_alert=True)

    # ════════════════════════════════════════════════════════
    # 💰 BALANCE
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^💰 Balance$"))
    async def balance_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<blockquote expandable>💰 <u>𝐘𝐎𝐔𝐑 𝐁𝐀𝐋𝐀𝐍𝐂𝐄</u></blockquote>
        ◈ ━━━━━━ ⸙ ━━━━━━ ◈
        🎉 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗕𝗼𝗻𝘂𝘀 : ₹𝟱𝟬
        💸 𝗬𝗼𝘂𝗿 𝗘𝗮𝗿𝗻𝗶𝗻𝗴 : ₹𝟬
        💰 𝗧𝗼𝘁𝗮𝗹 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 : ₹𝟱𝟬
        <blockquote>
        ✅ 𝗦𝘁𝗮𝗿𝘁 𝗘𝗮𝗿𝗻𝗶𝗻𝗴 𝗕𝘆 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗶𝗻𝗴 𝗧𝗮𝘀𝗸𝘀.
        </blockquote>
        """

        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML)

    # ════════════════════════════════════════════════════════
    # ☎️ SUPPORT
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^☎️ Support$"))
    async def support_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""<blockquote expandable>☎️ <u>𝐒𝐔𝐏𝐏𝐎𝐑𝐓</u></blockquote>
        ◈ ━━━━━━ ⸙ ━━━━━━ ◈
        
        
        """

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
        text = f"""👋 𝗛𝗲𝘆 𝗨𝘀𝗲𝗿!
        🎯 𝗝𝘂𝘀𝘁 𝟮 𝗧𝗮𝘀𝗸 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲 𝗞𝗮𝗿𝗼
        🤑 ₹𝟮𝟬𝟬 𝗜𝗻𝘀𝘁𝗮𝗻𝘁 𝗘𝗮𝗿𝗻 𝗞𝗮𝗿𝗼
        
        🔒 𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄𝗮𝗹 𝗔𝘂𝘁𝗼 𝗨𝗻𝗹𝗼𝗰𝗸 𝗛𝗼𝗷𝗮𝗲𝗴𝗮
        👍 𝗙𝗮𝘀𝘁 & 𝗘𝗮𝘀𝘆 𝗧𝗮𝘀𝗸. 
        """

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
            text="⌛ 𝗙𝗿𝗶𝘀𝘁 𝗝𝗼𝗶𝗻 𝗮𝗻𝗱 𝘁𝗵𝗲𝗻 𝗖𝗹𝗮𝗶𝗺 𝘆𝗼𝘂𝗿 ₹𝟮𝟬𝟬.",
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
            "⚠️ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲 𝗔𝗹𝗹 𝟮 𝗧𝗮𝘀𝗸𝘀 𝗙𝗶𝗿𝘀𝘁!\n"
            "✅ 𝗙𝗿𝗶𝘀𝘁 𝗝𝗼𝗶𝗻 𝗮𝗻𝗱 𝘁𝗵𝗲𝗻 𝗖𝗹𝗮𝗶𝗺 𝘆𝗼𝘂𝗿 ₹𝟮𝟬𝟬.\n"
            "🚨 𝗧𝗮𝘀𝗸 𝗣𝘂𝗿𝗮 𝗞𝗶𝗲 𝗕𝗶𝗻𝗮 𝗖𝗹𝗮𝗶𝗺 𝗡𝗮𝗵𝗶𝗻 𝗛𝗼𝗴𝗮 🙅",
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
        text = f"""🤑 𝗣𝗘𝗥 𝗥𝗘𝗙𝗘𝗥 ₹𝟭𝟬
        🤵‍♂ 𝗬𝗢𝗨𝗥 𝗥𝗘𝗙𝗘𝗥𝗥𝗔𝗟 𝗟𝗜𝗡𝗞:
        ➥  {rafer}
        
        🔍 𝗦𝗛𝗔𝗥𝗘 𝗪𝗜𝗧𝗛 𝗬𝗢𝗨𝗥 𝗙𝗥𝗜𝗘𝗡𝗗𝗦 & 𝗙𝗔𝗠𝗜𝗟𝗬 𝗔𝗡𝗗 𝗘𝗔𝗥𝗡 ₹𝟭𝟬 💰
        """

        # ✏️ INLINE BUTTON — Yahan apna button set karo
        inline_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 LINK", url="https://t.me/Dkgkmemfcbot")],
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
        text = f"""
        
        """

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
        text = f"""📤<u> 𝐖𝐈𝐓𝐇𝐃𝐑𝐀𝐖𝐀𝐋𝐒</u>
        ◈ ━━━━━━ ⸙ ━━━━━━ ◈
        💰 𝗠𝗶𝗻𝗶𝗺𝘂𝗺 𝗪𝗶𝘁𝗵𝗱𝗿𝗮𝘄𝗮𝗹: ₹𝟳𝟬
        💳 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗕𝗮𝗹𝗮𝗻𝗰𝗲: ₹𝟱𝟬
        
        ✅ 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲 𝘁𝗮𝘀𝗸𝘀 𝘁𝗼 𝗲𝗮𝗿𝗻 𝗮𝗻𝗱 𝘂𝗻𝗹𝗼𝗰𝗸 𝘄𝗶𝘁𝗵𝗱𝗿𝗮𝘄𝗮𝗹.
        """
        
        await msg.reply_text(text=text, parse_mode=enums.ParseMode.HTML)

    # ════════════════════════════════════════════════════════
    # 📊 STATISTICS
    # ════════════════════════════════════════════════════════
    @app.on_message(filters.text & filters.private & filters.regex("^📊 Statistics$"))
    async def statistics_handler(client: Client, msg: Message):

        # ✏️ YAHAN APNA TEXT LIKHO
        text = f"""📊 <u>𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒</u>
        👤 𝗧𝗼𝘁𝗮𝗹 𝗧𝗮𝘀𝗸𝘀: 𝟯 + <b>Rafer</b>
        ✅ 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱 𝗧𝗮𝘀𝗸𝘀: 𝟬
        💰 𝗧𝗼𝘁𝗮𝗹 𝗘𝗮𝗿𝗻𝗶𝗻𝗴𝘀: 𝟬
        """

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
