# -*- coding: utf-8 -*-

import os
import random
import logging
import time

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

# ======================= 日志 ============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ======================= TOKEN ============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("❌ 未设置 BOT_TOKEN")

# ======================= 主菜单 ============================
def main_menu():
    keyboard = [
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
    ]
    return InlineKeyboardMarkup(keyboard)

# ======================= 子菜单 ============================
def mood_menu():
    keyboard = [
        [
            InlineKeyboardButton("💬 心情一句话", callback_data="mood_sentence"),
            InlineKeyboardButton("🎨 颜色心情", callback_data="mood_color"),
        ],
        [
            InlineKeyboardButton("🧘 简单放松", callback_data="mood_relax"),
            InlineKeyboardButton("📖 温柔句子", callback_data="mood_quote"),
        ],
        [InlineKeyboardButton("⬅ 返回主菜单", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def knowledge_menu():
    keyboard = [
        [
            InlineKeyboardButton("🌍 随机小知识", callback_data="know_fact"),
            InlineKeyboardButton("🌱 生活常识", callback_data="know_life"),
        ],
        [
            InlineKeyboardButton("🧪 趣味科学", callback_data="know_science"),
            InlineKeyboardButton("🔤 字词小科普", callback_data="know_word"),
        ],
        [InlineKeyboardButton("⬅ 返回主菜单", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu():
    keyboard = [
        [
            InlineKeyboardButton("✊ 石头剪刀布", callback_data="game_rps"),
            InlineKeyboardButton("🎲 掷骰子", callback_data="game_dice"),
        ],
        [
            InlineKeyboardButton("🔢 数字猜谜", callback_data="game_guess"),
            InlineKeyboardButton("😊 表情组合", callback_data="game_emoji"),
        ],
        [InlineKeyboardButton("⬅ 返回主菜单", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ======================= /start 文案 ============================
START_TEXT = (
    "👋 欢迎来到 **DailyLife Pro · 日常助手**！\n\n"
    "这是一个轻量、健康、无任何敏感内容的日常陪伴机器人 🌿\n\n"
    "👇 点击下方菜单开始体验吧！"
)

# ======================= 指令 ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_TEXT,
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("发送 /start 打开主菜单即可使用全部功能")

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "DailyLife Pro 是一款轻娱乐 + 日常助手机器人"
    )

# ======================= 按钮处理 ============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # 返回主菜单
    if data == "back_main":
        await query.edit_message_text("🏠 主菜单", reply_markup=main_menu())
        return

    # 今日概览
    if data == "today":
        summaries = [
            "今天适合做一件一直想做但没开始的小事。",
            "保持轻松，慢慢来已经很好。",
            "不必把今天过得完美，过得舒适就好。",
        ]
        goals = [
            "整理桌面 1 分钟",
            "喝一杯水",
            "发一句问候给朋友",
            "写一行文字",
        ]
        text = (
            "📅 今日概览\n\n"
            f"• 今日建议：{random.choice(summaries)}\n"
            f"• 今日小目标：{random.choice(goals)}\n"
            "• 记得给自己一点轻松时间 🌿"
        )
        await query.edit_message_text(text, reply_markup=main_menu())
        return

    # 情绪工具
    if data == "mood":
        await query.edit_message_text("😊 情绪工具", reply_markup=mood_menu())
        return

    if data == "mood_sentence":
        sentences = [
            "你已经做得很好了。",
            "今天也可以温柔地对自己一点。",
            "放慢一点也没关系。",
            "给自己一点点时间吧。",
        ]
        await query.edit_message_text(
            "💬 心情一句话：\n\n" + random.choice(sentences),
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_color":
        colors = [
            "🔵 蓝色：适合安静与沉思。",
            "🟢 绿色：适合放松与恢复。",
            "🟣 紫色：适合创作灵感。",
            "🟡 黄色：适合社交与微笑。",
        ]
        await query.edit_message_text(
            "🎨 颜色心情：\n\n" + random.choice(colors),
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_relax":
        await query.edit_message_text(
            "🧘 放松练习：\n\n做 5 次深呼吸，让肩膀轻轻放松一下。",
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_quote":
        quotes = [
            "你值得所有温柔的事。",
            "慢慢来，不着急。",
            "你已经走了很远了。",
        ]
        await query.edit_message_text(
            "📖 温柔句子：\n\n" + random.choice(quotes),
            reply_markup=mood_menu(),
        )
        return

    # 知识
    if data == "knowledge":
        await query.edit_message_text("📚 轻知识百科", reply_markup=knowledge_menu())
        return

    if data == "know_fact":
        facts = [
            "蜂蜜永远不会变质。",
            "章鱼有三颗心脏。",
            "人的鼻子可以记住五万种气味。",
        ]
        await query.edit_message_text(
            "🌍 小知识：\n\n" + random.choice(facts),
            reply_markup=knowledge_menu(),
        )
        return

    # 小游戏
    if data == "games":
        await query.edit_message_text("🎮 小游戏区", reply_markup=games_menu())
        return

    if data == "game_dice":
        await query.edit_message_text(
            f"🎲 你掷出了 {random.randint(1,6)} 点",
            reply_markup=games_menu(),
        )
        return

    # 每日卡片
    if data == "daily_card":
        cards = [
            "今日提示卡：\n\n做一件“小到不会失败”的小事。",
            "灵感卡：\n\n记下一句今天想到的好句子。",
            "自我关怀卡：\n\n允许自己慢下来，不必完美。",
            "小目标卡：\n\n10 分钟内能完成的小事情，做一件就好。",
        ]
        await query.edit_message_text(
            "📝 " + random.choice(cards),
            reply_markup=main_menu(),
        )
        return

    # 灵感
    if data == "inspiration":
        ideas = [
            "给未来自己一句话。",
            "拍一张今天的天空。",
            "写下一件感恩的小事。",
        ]
        await query.edit_message_text(
            "✨ 随机灵感：\n\n" + random.choice(ideas),
            reply_markup=main_menu(),
        )
        return

    # 专注
    if data == "focus":
        await query.edit_message_text(
            "⏳ 专注 30 秒\n\n深呼吸，安静一下",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("完成了", callback_data="back_main")]]
            ),
        )
        return

    # 休息提醒
    if data == "relax":
        await query.edit_message_text(
            "🔔 休息提醒：\n\n站起来走走，喝口水，活动一下肩颈吧。",
            reply_markup=main_menu(),
        )
        return

# ======================= 启动入口 ============================
def main():
    logger.info("🤖 Bot 启动中...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
