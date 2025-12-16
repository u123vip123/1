import os
from flask import Flask, request

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ======================
# 1. Flask 应用
# ======================
app = Flask(__name__)

@app.route("/")
def index():
    return "OK - Web Service is running"


# ======================
# 2. Telegram Bot 逻辑
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
tg_app = None   # 先占位，后面初始化

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot 已通过 Webhook 成功运行")


@app.post(f"/webhook/{BOT_TOKEN}")
async def telegram_webhook():
    update = Update.de_json(request.json, tg_app.bot)
    await tg_app.process_update(update)
    return "ok"


# ======================
# 3. 关键：在 __main__ 初始化 Bot
# ======================
if __name__ == "__main__":
    if not BOT_TOKEN:
        raise RuntimeError("❌ 未设置 BOT_TOKEN")

    # ✅ 初始化 Telegram Bot（但不 run）
    tg_app = ApplicationBuilder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))

    # ✅ 启动 Flask（Render 只认这个端口）
    port = int(os.getenv("PORT", 10000))
    print(f"在 {port} 端口监听")
    app.run(host="0.0.0.0", port=port)
