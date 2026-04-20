# ==============================================================
# ⚙️ CONFIG — SIRF YAHAN APNI VALUES DAALO
# ==============================================================

# ── BOT TOKEN (BotFather se) ───────────────────────────────
BOT_TOKEN = "1234567890:ABCxxx..."   # 👈 APNA TOKEN

# ── BOT OWNER ─────────────────────────────────────────────
OWNER_ID = 5864182070   # 👈 Apna user ID

# ── BROADCAST ADMINS ──────────────────────────────────────
ADMINS = [
    5864182070,
    8260757052,  # Admin 2
    # 1122334455,  # Admin 3
]

# ── FORCE JOIN CHANNELS (PRIVATE) ─────────────────────────
#
# PRIVATE channel/group ke liye:
#   "_id"  → Numeric chat ID  (e.g. -1001234567890)
#   "link" → Private invite link (e.g. https://t.me/+AbCdEfGh)
#
# ⚠️ IMPORTANT:
#   1. Bot ko us channel/group ka ADMIN banana ZAROORI hai
#   2. Numeric ID pane ke liye @userinfobot ya @RawDataBot use karo
#
REQUIRED_CHANNELS = [
    {
        "_id":  -1001234567890,                   # 👈 Pehle channel ka numeric ID
        "link": "https://t.me/+AbCdEfGhIjKlMnOp", # 👈 Pehle channel ka invite link
    },
    {
        "_id":  -1009876543210,                   # 👈 Doosre channel ka numeric ID
        "link": "https://t.me/+XyZaBcDeFgHiJkLm", # 👈 Doosre channel ka invite link
    },
    {
        "_id":  -1001234567890,                   # 👈 Pehle channel ka numeric ID
        "link": "https://t.me/+AbCdEfGhIjKlMnOp", # 👈 Pehle channel ka invite link
    },
    {
        "_id":  -1009876543210,                   # 👈 Doosre channel ka numeric ID
        "link": "https://t.me/+XyZaBcDeFgHiJkLm", # 👈 Doosre channel ka invite link
    },
    
]

# ── WELCOME IMAGES ─────────────────────────────────────────
WELCOME_IMAGE_BEFORE = "https://o.uguu.se/ZnvqCTFv.jpg"  # 👈 Force join se pehle wali image
WELCOME_IMAGE_AFTER  = "FILE_ID_YAHAN"  # 👈 Verify ke baad wali image
