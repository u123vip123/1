import os
import random
import time
import logging
import asyncio

from flask import Flask, request

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

# ======================= 基础配置 ============================
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BOT_TOKENS = os.getenv("BOT_TOKENS")
if not BOT_TOKENS:
    raise RuntimeError("❌ BOT_TOKENS 未设置")

TOKENS = [t.strip() for t in BOT_TOKENS.split(",") if t.strip()]

PORT = int(os.getenv("PORT", 10000))

app = Flask(__name__)

# 保存所有 bot Application
BOT_APPS = {}

# ======================= 菜单 ============================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 今日概览", callback_data="today")],
        [
            InlineKeyboardButton("😊 情绪工具", callback_data="mood"),
            InlineKeyboardButton("🧠 心智小任务", callback_data="mind_task"),
        ],
        [
            InlineKeyboardButton("📚 轻知识百科", callback_data="knowledge"),
            InlineKeyboardButton("🎮 小游戏", callback_data="games"),
        ],
        [
            InlineKeyboardButton("📝 每日卡片", callback_data="daily_card"),
            InlineKeyboardButton("✨ 随机灵感", callback_data="inspiration"),
        ],
        [
            InlineKeyboardButton("⏳ 专注 30 秒", callback_data="focus"),
            InlineKeyboardButton("🔔 休息提醒", callback_data="relax"),
        ],
    ])


def mood_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 心情一句话", callback_data="mood_sentence"),
            InlineKeyboardButton("🎨 颜色心情", callback_data="mood_color"),
        ],
        [
            InlineKeyboardButton("🧘 简单放松", callback_data="mood_relax"),
            InlineKeyboardButton("📖 温柔句子", callback_data="mood_quote"),
        ],
        [InlineKeyboardButton("⬅ 返回主菜单", callback_data="back_main")],
    ])


def knowledge_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🌍 随机小知识", callback_data="know_fact"),
            InlineKeyboardButton("🌱 生活常识", callback_data="know_life"),
        ],
        [
            InlineKeyboardButton("🧪 趣味科学", callback_data="know_science"),
            InlineKeyboardButton("🔤 字词小科普", callback_data="know_word"),
        ],
        [InlineKeyboardButton("⬅ 返回主菜单", callback_data="back_main")],
    ])


def games_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✊ 石头剪刀布", callback_data="game_rps"),
            InlineKeyboardButton("🎲 掷骰子", callback_data="game_dice"),
        ],
        [
            InlineKeyboardButton("🔢 数字猜谜", callback_data="game_guess"),
            InlineKeyboardButton("😊 表情组合", callback_data="game_emoji"),
        ],
        [InlineKeyboardButton("⬅ 返回主菜单", callback_data="back_main")],
    ])


# ======================= 文案 ============================
START_TEXT = """👋 欢迎来到《DailyLife Pro · 日常助手》
👇 点击菜单开始体验"""


# ======================= 指令 ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_TEXT, reply_markup=main_menu(), parse_mode="Markdown"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("发送 /start 打开主菜单")


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("DailyLife Pro · 健康轻娱乐机器人")


# ======================= 按钮处理（原逻辑不变） ============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "back_main":
        await query.edit_message_text("🏠 主菜单", reply_markup=main_menu())
        return

    if data == "today":
        await query.edit_message_text(
            "📅 今天适合做一件小事 🌱", reply_markup=main_menu()
        )
        return

    if data == "mood":
        await query.edit_message_text("😊 情绪工具", reply_markup=mood_menu())
        return

    if data == "knowledge":
        await query.edit_message_text("📚 轻知识", reply_markup=knowledge_menu())
        return

    if data == "games":
        await query.edit_message_text("🎮 小游戏", reply_markup=games_menu())
        return


# ======================= Flask 路由 ============================
@app.get("/")
def health():
    return "OK", 200


@app.post("/webhook/<token>")
def webhook(token):
    if token not in BOT_APPS:
        return "Invalid token", 404

    bot_app = BOT_APPS[token]
    update = Update.de_json(request.get_json(force=True), bot_app.bot)

    # 在事件循环中处理 update
    bot_app.create_task(bot_app.process_update(update))
    return "OK", 200


# ======================= 初始化 Bots ============================
async def init_bots():
    for token in TOKENS:
        application = ApplicationBuilder().token(token).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_cmd))
        application.add_handler(CommandHandler("about", about_cmd))
        application.add_handler(CallbackQueryHandler(button_handler))

        await application.initialize()
        await application.start()

        BOT_APPS[token] = application
        logger.info(f"✅ Bot 初始化完成: {token[:10]}***")


# ======================= 主入口 ============================
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_bots())

    logger.info(f"🚀 Flask Webhook 服务启动，端口 {PORT}")
    app.run(host="0.0.0.0", port=PORT)
