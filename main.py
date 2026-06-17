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


# ======================= MENU UTAMA ============================
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Ringkasan Hari Ini", callback_data="today")],
        [
            InlineKeyboardButton("😊 Mood & Relaksasi", callback_data="mood"),
            InlineKeyboardButton("🧠 Tantangan Mini", callback_data="mind_task"),
        ],
        [
            InlineKeyboardButton("📚 Fakta & Pengetahuan", callback_data="knowledge"),
            InlineKeyboardButton("🎮 Mini Game", callback_data="games"),
        ],
        [
            InlineKeyboardButton("📝 Kartu Harian", callback_data="daily_card"),
            InlineKeyboardButton("✨ Inspirasi Acak", callback_data="inspiration"),
        ],
        [
            InlineKeyboardButton("⏳ Fokus 30 Detik", callback_data="focus"),
            InlineKeyboardButton("🔔 Pengingat Istirahat", callback_data="relax"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ======================= SUB MENU ============================
def mood_menu():
    keyboard = [
        [
            InlineKeyboardButton("💬 Kalimat Hari Ini", callback_data="mood_sentence"),
            InlineKeyboardButton("🎨 Warna & Mood", callback_data="mood_color"),
        ],
        [
            InlineKeyboardButton("🧘 Relaksasi Singkat", callback_data="mood_relax"),
            InlineKeyboardButton("📖 Kutipan Positif", callback_data="mood_quote"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def knowledge_menu():
    keyboard = [
        [
            InlineKeyboardButton("🌍 Fakta Unik", callback_data="know_fact"),
            InlineKeyboardButton("🌱 Tips Sehari-hari", callback_data="know_life"),
        ],
        [
            InlineKeyboardButton("🧪 Sains Seru", callback_data="know_science"),
            InlineKeyboardButton("🔤 Edukasi Kata", callback_data="know_word"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def games_menu():
    keyboard = [
        [
            InlineKeyboardButton("✊ Batu Gunting Kertas", callback_data="game_rps"),
            InlineKeyboardButton("🎲 Lempar Dadu", callback_data="game_dice"),
        ],
        [
            InlineKeyboardButton("🔢 Tebak Angka", callback_data="game_guess"),
            InlineKeyboardButton("😊 Kombinasi Emoji", callback_data="game_emoji"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ======================= TEKS START ============================

START_TEXT = """
👋 Selamat datang di **DailyLife Pro · Asisten Harianmu**!

Bot ini dirancang untuk menemani harimu dengan fitur ringan, santai, dan menyenangkan 👇

🌤 **Ringkasan Hari Ini**  
Dapatkan saran kecil & target ringan untuk memulai hari.

😊 **Mood & Relaksasi**  
Kalimat positif, warna mood, hingga relaksasi singkat.

🧠 **Tantangan Mini**  
Latihan fokus & aktivitas kecil untuk pikiranmu.

📚 **Fakta & Pengetahuan**  
Temukan fakta unik, tips praktis, & sains seru.

🎮 **Mini Game**  
Main cepat, santai, tanpa ribet 😆

📝 **Kartu Harian**  
Saran & refleksi ringan setiap hari.

✨ **Inspirasi Acak**  
Ide kecil untuk menyegarkan pikiran.

⏳ **Fokus 30 Detik**  
Masuk ke mode fokus singkat.

🔔 **Pengingat Istirahat**  
Jangan lupa rileks & jaga keseimbangan.

Bot ini aman & bebas konten sensitif.  
Tanpa hadiah, tanpa perjudian, tanpa layanan finansial.

👇 Pilih menu di bawah & mulai eksplor!
"""


# ======================= COMMAND ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_TEXT, reply_markup=main_menu(), parse_mode="Markdown"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Cara penggunaan:\nGunakan /start untuk membuka menu utama."
    )


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "DailyLife Pro adalah bot asisten harian ringan yang dirancang untuk hiburan santai & keseimbangan aktivitas sehari-hari."
    )


# ======================= BUTTON HANDLER ============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "back_main":
        await query.edit_message_text(
            "🏠 Kembali ke menu utama:", reply_markup=main_menu()
        )
        return

    if data == "today":
        summaries = [
            "Hari ini cocok untuk memulai sesuatu yang kecil tapi bermakna.",
            "Pelan-pelan saja, progres kecil tetaplah progres.",
            "Tidak perlu sempurna, nyaman saja sudah cukup.",
        ]
        goals = [
            "Rapikan meja selama 1 menit",
            "Minum segelas air",
            "Kirim pesan ke teman",
            "Tulis satu kalimat",
        ]
        text = f"""
📅 **Ringkasan Hari Ini**

• Saran: {random.choice(summaries)}
• Target kecil: {random.choice(goals)}
• Nikmati hari dengan santai 🌿
"""
        await query.edit_message_text(text, reply_markup=main_menu(), parse_mode="Markdown")
        return

    if data == "mood":
        await query.edit_message_text("😊 Mood & Relaksasi:", reply_markup=mood_menu())
        return

    if data == "mood_sentence":
        sentences = [
            "Kamu sudah melakukan yang terbaik hari ini.",
            "Sedikit istirahat juga bagian dari progres.",
            "Tidak apa-apa berjalan lebih lambat.",
            "Bersikap lembut pada diri sendiri itu penting.",
        ]
        await query.edit_message_text(
            "💬 Kalimat Hari Ini:\n\n" + random.choice(sentences),
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_color":
        colors = [
            "🔵 Biru — cocok untuk ketenangan & refleksi.",
            "🟢 Hijau — cocok untuk relaksasi & pemulihan energi.",
            "🟣 Ungu — cocok untuk kreativitas & inspirasi.",
            "🟡 Kuning — cocok untuk semangat & interaksi.",
        ]
        await query.edit_message_text(
            "🎨 Warna & Mood:\n\n" + random.choice(colors),
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_relax":
        await query.edit_message_text(
            "🧘 Relaksasi Singkat:\n\nTarik napas dalam 5 kali, rilekskan bahu & lehermu.",
            reply_markup=mood_menu(),
        )
        return

    if data == "mood_quote":
        quotes = [
            "Hal kecil yang konsisten akan membawa perubahan besar.",
            "Kamu tidak perlu terburu-buru.",
            "Hari yang tenang juga hari yang produktif.",
        ]
        await query.edit_message_text(
            "📖 Kutipan Positif:\n\n" + random.choice(quotes),
            reply_markup=mood_menu(),
        )
        return

    if data == "knowledge":
        await query.edit_message_text("📚 Fakta & Pengetahuan:", reply_markup=knowledge_menu())
        return

    if data == "know_fact":
        facts = [
            "Madu alami tidak pernah basi.",
            "Gurita memiliki tiga jantung.",
            "Tubuh manusia memiliki lebih dari 600 otot.",
        ]
        await query.edit_message_text(
            "🌍 Fakta Unik:\n\n" + random.choice(facts),
            reply_markup=knowledge_menu(),
        )
        return

    if data == "know_life":
        tips = [
            "Minum air secara teratur membantu menjaga energi.",
            "Istirahat singkat meningkatkan fokus.",
            "Tidur cukup penting untuk kesehatan mental.",
        ]
        await query.edit_message_text(
            "🌱 Tips Sehari-hari:\n\n" + random.choice(tips),
            reply_markup=knowledge_menu(),
        )
        return

    if data == "know_science":
        sci = [
            "Suhu petir bisa lebih panas dari permukaan matahari.",
            "Awan dapat memiliki berat ratusan ton.",
            "Otak manusia aktif bahkan saat tidur.",
        ]
        await query.edit_message_text(
            "🧪 Sains Seru:\n\n" + random.choice(sci),
            reply_markup=knowledge_menu(),
        )
        return

    if data == "know_word":
        words = [
            "“Healing” berarti proses pemulihan diri.",
            "“Mindfulness” berarti kesadaran penuh terhadap momen saat ini.",
        ]
        await query.edit_message_text(
            "🔤 Edukasi Kata:\n\n" + random.choice(words),
            reply_markup=knowledge_menu(),
        )
        return

    if data == "games":
        await query.edit_message_text("🎮 Mini Game:", reply_markup=games_menu())
        return

    if data == "game_rps":
        keyboard = [
            [
                InlineKeyboardButton("✊", callback_data="rps_rock"),
                InlineKeyboardButton("✋", callback_data="rps_paper"),
                InlineKeyboardButton("✌", callback_data="rps_scissors"),
            ],
            [InlineKeyboardButton("⬅ Kembali", callback_data="games")],
        ]
        await query.edit_message_text("✊ Batu Gunting Kertas:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data.startswith("rps_"):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        user_choice = data.split("_")[1]

        emoji = {"rock": "✊", "paper": "✋", "scissors": "✌"}

        if user_choice == bot_choice:
            result = "Seri 🎯"
        elif (
            (user_choice == "rock" and bot_choice == "scissors")
            or (user_choice == "paper" and bot_choice == "rock")
            or (user_choice == "scissors" and bot_choice == "paper")
        ):
            result = "Kamu menang ✨"
        else:
            result = "Aku menang 😆"

        text = f"Kamu: {emoji[user_choice]}\nAku: {emoji[bot_choice]}\n\n{result}"
        await query.edit_message_text(text, reply_markup=games_menu())
        return

    if data == "game_dice":
        await query.edit_message_text(
            f"🎲 Kamu mendapatkan angka {random.randint(1,6)}.",
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
            [InlineKeyboardButton("⬅ Kembali", callback_data="games")],
        ]
        await query.edit_message_text(
            "Aku memikirkan angka antara 1~5, coba tebak:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    if data.startswith("guess_"):
        user = int(data.split("_")[1])
        correct = context.user_data.get("guess")
        if user == correct:
            msg = "🎉 Tebakanmu benar!"
        else:
            msg = f"😄 Belum tepat, angkanya adalah {correct}"
        await query.edit_message_text(msg, reply_markup=games_menu())
        return

    if data == "game_emoji":
        emo = random.sample(["😀","😎","🎉","⭐","🌈","🔥","🍀","🤗","🤩"], 5)
        await query.edit_message_text(
            "😊 Kombinasi Emoji:\n\n" + " ".join(emo),
            reply_markup=games_menu(),
        )
        return

    if data == "daily_card":
        cards = [
            "📝 Kartu Hari Ini:\n\nLakukan satu hal kecil yang mudah dicapai.",
            "✨ Kartu Inspirasi:\n\nCatat satu ide menarik hari ini.",
            "🌿 Kartu Relaksasi:\n\nLuangkan waktu singkat untuk diri sendiri.",
        ]
        await query.edit_message_text(random.choice(cards), reply_markup=main_menu())
        return

    if data == "inspiration":
        ins = [
            "Coba sesuatu yang berbeda hari ini.",
            "Luangkan waktu untuk hal yang kamu sukai.",
            "Mulai dari langkah kecil.",
        ]
        await query.edit_message_text(
            "✨ Inspirasi Acak:\n\n" + random.choice(ins),
            reply_markup=main_menu(),
        )
        return

    if data == "focus":
        await query.edit_message_text(
            "⏳ Mode Fokus:\n\nTenang selama 30 detik, beri ruang untuk pikiranmu.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Selesai ✅", callback_data="focus_done")]]
            ),
        )
        return

    if data == "focus_done":
        await query.edit_message_text(
            "👏 Bagus sekali! Fokus singkat juga sangat bermanfaat.",
            reply_markup=main_menu(),
        )
        return

    if data == "relax":
        await query.edit_message_text(
            "🔔 Waktu Istirahat:\n\nBangun, minum air, dan regangkan tubuhmu.",
            reply_markup=main_menu(),
        )
        return


# ======================= MAIN ============================
def main():
    if not BOT_TOKEN:
        raise RuntimeError("❌ BOT_TOKEN belum diatur")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("DailyLife Pro Bot (Versi Indonesia) berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
