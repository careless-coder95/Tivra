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
    # 9876543210,  # Admin 2
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
    # Aur add karna ho to copy karo upar wala block:
    # {
    #     "_id":  -1001122334455,
    #     "link": "https://t.me/+YourPrivateLink",
    # },
]

# ── WELCOME IMAGES ─────────────────────────────────────────
WELCOME_IMAGE_BEFORE = "FILE_ID_YAHAN"  # 👈 Force join se pehle wali image
WELCOME_IMAGE_AFTER  = "FILE_ID_YAHAN"  # 👈 Verify ke baad wali image

# ── TASK & EARN IMAGE ──────────────────────────────────────
TASK_IMAGE  = "FILE_ID_YAHAN"  # 👈 Task & Earn wali image

# ── REFER & EARN IMAGE ─────────────────────────────────────
REFER_IMAGE = "FILE_ID_YAHAN"  # 👈 Refer & Earn wali image
