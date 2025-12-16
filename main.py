import os
import time
import random
import asyncio
import logging

from flask import Flask, request

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ======================= 基础配置 =======================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

BOT_TOKENS = os.getenv("BOT_TOKENS")
if not BOT_TOKENS:
    raise RuntimeError("BOT_TOKENS 未设置")

TOKENS = [t.strip() for t in BOT_TOKENS.split(",")]

PORT = int(os.getenv("PORT", 10000))

app = Flask(__name__)

BOT_APPS: dict[str, Application] = {}
MAIN_LOOP: asyncio.AbstractEventLoop | None = None


# ======================= 菜单 =======================

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


# ======================= 文案 =======================

START_TEXT = """
👋 欢迎来到 **DailyLife Pro · 日常助手**

一个轻松、健康、无敏感内容的日常工具机器人。

👇 点击下方菜单开始体验
"""


# ======================= 指令 =======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_TEXT,
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("发送 /start 打开主菜单")


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("DailyLife Pro · 轻娱乐日常助手")


# ======================= 按钮处理（完整） =======================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "back_main":
        await query.edit_message_text("🏠 主菜单", reply_markup=main_menu())
        return

    if data == "today":
        await query.edit_message_text(
            "📅 今日概览\n\n慢慢来，今天已经很好了。",
            reply_markup=main_menu(),
        )
        return

    if data == "mood":
        await query.edit_message_text("😊 情绪工具", reply_markup=mood_menu())
        return

    if data == "mood_sentence":
        await query.edit_message_text(
            random.choice([
                "你已经做得很好了。",
                "慢一点也没关系。",
                "对自己温柔一点。",
            ]),
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_color":
        await query.edit_message_text(
            random.choice([
                "🔵 蓝色：安静",
                "🟢 绿色：恢复",
                "🟡 黄色：轻快",
            ]),
            reply_markup=mood_menu(),
        )
        return

    if data == "knowledge":
        await query.edit_message_text("📚 轻知识百科", reply_markup=knowledge_menu())
        return

    if data == "know_fact":
        await query.edit_message_text(
            random.choice([
                "蜂蜜不会变质",
                "章鱼有三颗心脏",
                "云也有重量",
            ]),
            reply_markup=knowledge_menu(),
        )
        return

    if data == "games":
        await query.edit_message_text("🎮 小游戏", reply_markup=games_menu())
        return

    if data == "game_dice":
        await query.edit_message_text(
            f"🎲 你掷出了 {random.randint(1,6)}",
            reply_markup=games_menu(),
        )
        return

    if data == "daily_card":
        await query.edit_message_text(
            "📝 今日卡片：\n\n做一件小到不会失败的事。",
            reply_markup=main_menu(),
        )
        return

    if data == "inspiration":
        await query.edit_message_text(
            "✨ 灵感：\n\n给未来的自己一句话。",
            reply_markup=main_menu(),
        )
        return

    if data == "focus":
        await query.edit_message_text(
            "⏳ 专注 30 秒开始",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("我完成了", callback_data="focus_done")]]
            ),
        )
        return

    if data == "focus_done":
        await query.edit_message_text(
            "👏 做得很好",
            reply_markup=main_menu(),
        )
        return

    if data == "relax":
        await query.edit_message_text(
            "🔔 休息一下，喝口水",
            reply_markup=main_menu(),
        )
        return


# ======================= Webhook =======================

@app.post("/webhook/<token>")
def webhook(token):
    if token not in BOT_APPS:
        return "Invalid token", 404

    bot_app = BOT_APPS[token]
    update = Update.de_json(request.get_json(force=True), bot_app.bot)

    asyncio.run_coroutine_threadsafe(
        bot_app.process_update(update),
        MAIN_LOOP,
    )

    return "OK", 200


# ======================= 初始化 =======================

async def init_bots():
    for token in TOKENS:
        application = (
            ApplicationBuilder()
            .token(token)
            .build()
        )

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_cmd))
        application.add_handler(CommandHandler("about", about_cmd))
        application.add_handler(CallbackQueryHandler(button_handler))

        await application.initialize()
        await application.start()

        BOT_APPS[token] = application

    logger.info(f"✅ 已启动 {len(BOT_APPS)} 个 Bot")


# ======================= 主入口 =======================

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    MAIN_LOOP = loop

    loop.run_until_complete(init_bots())

    app.run(host="0.0.0.0", port=PORT)
