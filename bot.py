"""
╔══════════════════════════════════════════╗
║       TIVRA PAY BOT — bot.py             ║
║          YAHAN SE BOT CHALTA HAI         ║
╚══════════════════════════════════════════╝

RUN KARO:
    python bot.py

INSTALL (pehli baar):
    pip install pyrogram tgcrypto
"""

from pyrogram import Client
from config import BOT_TOKEN

# ── Handlers import ──
import start  # start.py ke saare handlers yahan load honge


# ==============================================================
# 🚀 BOT INITIALIZE
# ==============================================================

app = Client(
    name="TivraPayBot",
    bot_token=BOT_TOKEN,

    # API ID aur API Hash — https://my.telegram.org se lo
    api_id=22815212,        # 👈 Apna API ID daalo
    api_hash="7ff4abb86e8b8b6ac93bee9d4e55ee0d",  # 👈 Apna API Hash daalo
)


# ==============================================================
# ▶️ START
# ==============================================================

if __name__ == "__main__":
    print("✅ Tivra Pay Bot starting...")
    app.run()
    print("🔴 Bot stopped.")
