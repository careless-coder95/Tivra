"""
╔══════════════════════════════════════════╗
║       TIVRA PAY BOT — bot.py             ║
║          YAHAN SE BOT CHALTA HAI         ║
╚══════════════════════════════════════════╝

INSTALL (pehli baar):
    pip install pyrogram tgcrypto

RUN KARO:
    python bot.py
"""

from pyrogram import Client
from config import BOT_TOKEN

# ==============================================================
# 🚀 BOT INITIALIZE — Pehle app banao
# ==============================================================

app = Client(
    name="TivraPayBot",
    bot_token=BOT_TOKEN,
    api_id=22815212,        # 👈 https://my.telegram.org se apna API ID daalo
    api_hash="7ff4abb86e8b8b6ac93bee9d4e55ee0d",  # 👈 https://my.telegram.org se apna API Hash daalo
)

# ==============================================================
# ── Handlers register — app ke BAAD
# ==============================================================

from start import register_handlers
from broadcast import register_broadcast_handlers

register_handlers(app)
register_broadcast_handlers(app)

# ==============================================================
# ▶️ START
# ==============================================================

if __name__ == "__main__":
    print("✅ Tivra Pay Bot starting...")
    app.run()
    print("🔴 Bot stopped.")
