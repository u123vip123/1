import os
import random
import time
import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


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


# ======================= 各子菜单 ============================
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


# ======================= /start 文案（极高内容密度） ============================

START_TEXT = """
👋 欢迎来到 **《DailyLife Pro · 日常助手》**！

这里集合了 *轻松、实用、健康、安全* 的日常功能，让你的碎片时间也能变得有意义👇

🌤 **今日概览**
• 一句话天气感受
• 今日建议与小提醒
• 一个轻量行动小目标

😊 **情绪工具**
• 心情一句话生成器  
• 颜色心情提示  
• 30 秒轻放松练习  
• 温柔语录  

🧠 **心智小任务**
• 专注练习  
• 思维小谜题  
• 习惯微行动  
• 小目标生成器  

📚 **轻知识百科**
• 随机有趣小知识  
• 生活小常识  
• 趣味科学  
• 字词小科普  

🎮 **小游戏区**
• 石头剪刀布  
• 掷骰子  
• 数字猜谜  
• 表情组合  

📝 **每日卡片**
• 今日提示卡  
• 灵感卡  
• 关怀卡  
• 小目标卡  

✨ **随机灵感**
• 灵感句子  
• 创意火花  
• 随机建议  

⏳ **专注 30 秒**
• 引导你快速进入短专注状态

🔔 **休息提醒**
• 轻柔的放松建议

本机器人为轻娱乐与日常助手用途，内容健康，不含奖励、博彩、金融等任何敏感内容。

👇 点击下方菜单开始体验！
"""


# ======================= 指令 ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_TEXT, reply_markup=main_menu(), parse_mode="Markdown"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 使用说明：发送 /start 打开主菜单即可使用全部功能。"
    )


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "《DailyLife Pro》是一款轻娱乐与小工具结合的健康机器人，适合所有用户使用。"
    )


# ======================= 按钮处理 ============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # 返回主菜单
    if data == "back_main":
        await query.edit_message_text(
            "🏠 已返回主菜单：", reply_markup=main_menu()
        )
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
        text = f"""
📅 **今日概览**

• 今日建议：{random.choice(summaries)}
• 今日小目标：{random.choice(goals)}
• 记得给自己一点轻松时间 🌿
"""
        await query.edit_message_text(text, reply_markup=main_menu(), parse_mode="Markdown")
        return

    # 情绪工具
    if data == "mood":
        await query.edit_message_text("😊 情绪工具：", reply_markup=mood_menu())
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
        await query.edit_message_text("📚 轻知识百科：", reply_markup=knowledge_menu())
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

    if data == "know_life":
        tips = [
            "睡前 1 小时不要玩手机，有助于睡眠。",
            "牙刷使用 3 个月需要更换。",
            "喝水分多次喝比一次喝很多更好。",
        ]
        await query.edit_message_text(
            "🌱 生活常识：\n\n" + random.choice(tips),
            reply_markup=knowledge_menu(),
        )
        return

    if data == "know_science":
        sci = [
            "闪电的温度比太阳表面还高五倍。",
            "企鹅会终生伴侣。",
            "一朵云的重量可达数百吨。",
        ]
        await query.edit_message_text(
            "🧪 趣味科学：\n\n" + random.choice(sci),
            reply_markup=knowledge_menu(),
        )
        return

    if data == "know_word":
        words = [
            "“松弛感”指内在安定、外在从容。",
            "“治愈系”指让人情绪恢复的风格。",
        ]
        await query.edit_message_text(
            "🔤 字词小科普：\n\n" + random.choice(words),
            reply_markup=knowledge_menu(),
        )
        return

    # 小游戏
    if data == "games":
        await query.edit_message_text("🎮 小游戏区：", reply_markup=games_menu())
        return

    if data == "game_rps":
        keyboard = [
            [
                InlineKeyboardButton("✊", callback_data="rps_rock"),
                InlineKeyboardButton("✋", callback_data="rps_paper"),
                InlineKeyboardButton("✌", callback_data="rps_scissors"),
            ],
            [InlineKeyboardButton("⬅ 返回", callback_data="games")],
        ]
        await query.edit_message_text("✊ 石头剪刀布：", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data.startswith("rps_"):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        user_choice = data.split("_")[1]

        emoji = {"rock": "✊", "paper": "✋", "scissors": "✌"}

        if user_choice == bot_choice:
            result = "平局 🎯"
        elif (
            (user_choice == "rock" and bot_choice == "scissors")
            or (user_choice == "paper" and bot_choice == "rock")
            or (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = "你赢了 ✨"
        else:
            result = "我赢了 😆"

        text = f"你：{emoji[user_choice]}\n我：{emoji[bot_choice]}\n\n{result}"
        await query.edit_message_text(text, reply_markup=games_menu())
        return

    if data == "game_dice":
        await query.edit_message_text(
            f"🎲 你掷出了 {random.randint(1,6)} 点。",
            reply_markup=games_menu(),
        )
        return

    if data == "game_guess":
        num = random.randint(1, 5)
        context.user_data["guess"] = num
        keyboard = [
            [
                InlineKeyboardButton(str(i), callback_data=f"guess_{i}")
                for i in range(1, 6)
            ],
            [InlineKeyboardButton("⬅ 返回", callback_data="games")],
        ]
        await query.edit_message_text(
            "我想了 1~5 之间的数字，你来猜：",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if data.startswith("guess_"):
        user = int(data.split("_")[1])
        correct = context.user_data.get("guess")
        if user == correct:
            msg = "🎉 你猜对了！"
        else:
            msg = f"😄 没猜中，我想的是 {correct}"
        await query.edit_message_text(msg, reply_markup=games_menu())
        return

    if data == "game_emoji":
        emo = random.sample(["😀","😎","🎉","⭐","🌈","🔥","🍀","🤗","🤩"], 5)
        await query.edit_message_text(
            "😊 表情组合：\n\n" + " ".join(emo),
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
        await query.edit_message_text("📝 " + random.choice(cards), reply_markup=main_menu())
        return

    # 灵感
    if data == "inspiration":
        ins = [
            "试着拍一张“今天的颜色”的照片。",
            "想一件你很久没做但想做的事。",
            "给未来自己一句话。",
        ]
        await query.edit_message_text(
            "✨ 随机灵感：\n\n" + random.choice(ins),
            reply_markup=main_menu(),
        )
        return

    # 30 秒专注
    if data == "focus":
        context.user_data["focus_start"] = time.time()
        await query.edit_message_text(
            "⏳ 专注练习开始：\n\n保持安静 30 秒，我会提醒你结束。",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("我完成了", callback_data="focus_done")]]
            ),
        )
        return

    if data == "focus_done":
        await query.edit_message_text(
            "👏 做得很好！感谢你给自己一点专注时间。",
            reply_markup=main_menu(),
        )
        return

    # 休息提醒
    if data == "relax":
        await query.edit_message_text(
            "🔔 休息提醒：\n\n站起来走走、喝口水、活动一下肩颈吧。",
            reply_markup=main_menu(),
        )
        return


# ======================= 主入口 ============================
def main():
    if not BOT_TOKEN:
        raise RuntimeError("❌ BOT_TOKEN 环境变量未设置")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("DailyLife Pro 中文机器人已启动")
    app.run_polling()


if __name__ == "__main__":
    main()
