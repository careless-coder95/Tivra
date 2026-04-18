# ==============================================================
# ⚙️ CONFIG — SIRF YAHAN APNI VALUES DAALO
# ==============================================================

# ── BOT TOKEN (BotFather se) ───────────────────────────────
BOT_TOKEN = "1234567890:ABCxxx..."   # 👈 APNA TOKEN

# ── BOT OWNER (sirf 1 — highest authority) ────────────────
OWNER_ID = 5864182070   # 👈 Apna user ID

# ── BROADCAST ADMINS (ye log /broadcast use kar sakte hain) ─
# Owner automatically admin hota hai, yahan aur log add karo
ADMINS = [
    5864182070,    # Owner
    # 9876543210,  # Admin 2 — uncomment karke ID daalo
    # 1122334455,  # Admin 3
]

# ── REQUIRED FORCE JOIN CHANNELS / GROUPS ─────────────────
#
# PUBLIC channel/group:
#   "_id"  → "@username"  (@ ke saath)
#   "link" → "https://t.me/username"
#
# PRIVATE channel/group:
#   "_id"  → Chat numeric ID, e.g. -1001234567890
#             (Bot ko us group/channel ka admin banana padega)
#   "link" → Private invite link, e.g. "https://t.me/+AbCdEfGhIjK"
#
# Button naam automatically "Join 1", "Join 2" ban jaata hai.
# 2 buttons ek row mein aate hain.
#
REQUIRED_CHANNELS = [
    {
        "_id":  "@musicgroupxd",                    # public
        "link": "https://t.me/musicgroupxd",
    },
    {
        "_id":  "@phblicdarling",                   # public
        "link": "https://t.me/phblicdarling",
    },
    # {
    #     "_id":  -1001234567890,                   # private group/channel
    #     "link": "https://t.me/+AbCdEfGhIjKlMnOp",
    # },
    # {
    #     "_id":  -1009876543210,
    #     "link": "https://t.me/+XyZaBcDeFgHiJkLm",
    # },
    # Aur add karte jao...
]

# ── WELCOME IMAGE FILE ID ──────────────────────────────────
WELCOME_IMAGE = "https://n.uguu.se/xqNNNipL.jpg"
