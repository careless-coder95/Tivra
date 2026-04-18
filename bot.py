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
    api_id=12345678,        # 👈 https://my.telegram.org se apna API ID daalo
    api_hash="abcdef1234",  # 👈 https://my.telegram.org se apna API Hash daalo
)

# ==============================================================
# ── Handlers import — app ke BAAD import hona chahiye
# ==============================================================
from start import register_handlers
register_handlers(app)

# ==============================================================
# ▶️ START
# ==============================================================

if __name__ == "__main__":
    print("✅ Tivra Pay Bot starting...")
    app.run()
    print("🔴 Bot stopped.")
