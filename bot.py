import os, requests, random, threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CA = os.getenv("CA", "Coming soon")

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "SABAI bot running"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def get_price():
    try:
        r = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{CA}", timeout=10).json()
        if not r.get("pairs"): return None
        p = sorted(r["pairs"], key=lambda x: x.get("volume",{}).get("h24",0), reverse=True)[0]
        return p
    except: return None

async def start(update, context):
    await update.message.reply_text("🧘 SABAI AI พร้อมแล้ว\n/check - เช็คราคา\n/ca - ดู Contract")

async def check_cmd(update, context):
    await update.message.reply_text("เช็คกราฟแปป... 📈")
    p = get_price()
    if not p:
        await update.message.reply_text(f"ยังไม่เจอ CA {CA}")
        return
    await update.message.reply_text(f"Price: ${p.get('priceUsd')}\n24h: {p.get('priceChange',{}).get('h24')}%\n{p.get('url')}")

async def ca_cmd(update, context):
    await update.message.reply_text(f"{CA}\nhttps://dexscreener.com/solana/{CA}")

async def chat(update, context):
    await update.message.reply_text(random.choice(["ชิลๆดิเพื่อน 🧘","SABAI อยู่นะ 😎","เหรียญชิล คนถือต้องชิลตาม 🍃"]))

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_cmd))
    app.add_handler(CommandHandler("ca", ca_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__": main()
