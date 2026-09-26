import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# TOKEN lo lee de Render para que sea seguro
TOKEN = os.environ.get("TOKEN")

# LINKS OFICIALES JOSE BLOQUEO PERU EPIC
CANAL_LINK = "https://t.me/josesistema"
GRUPO_LINK = "https://t.me/+v7x6gtLnr2gyNTgx"
PERSONAL_LINK = "https://t.me/josesistema2026"

logging.basicConfig(level=logging.INFO)

def get_botones():
    keyboard = [
        [InlineKeyboardButton("📢 CANAL OFICIAL", url=CANAL_LINK)],
        [InlineKeyboardButton("👥 GRUPO DE VENTAS", url=GRUPO_LINK)],
        [InlineKeyboardButton("👤 SOPORTE @josesistema2026", url=PERSONAL_LINK)],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🔥 **JOSE BLOQUEO PERU EPIC** 🔥\n"
        "✅ **BLOQUEO** DE OPERADORAS 100% EFECTIVO\n"
        "❌ NO ES DESBLOQUEO\n\n"
        "📱 Bloqueo Entel / Bitel / Claro / Movistar / Bim\n"
        "⚡ Rápido - Seguro - 24/7\n\n"
        "👇 **Usa /buy para ver precios** 👇"
    )
    await update.message.reply_text(texto, reply_markup=get_botones(), parse_mode="Markdown")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "💰 **PRECIOS - JOSE BLOQUEO PERU** 💰\n\n"
        "📱 **CREDITOS:**\n"
        "• 1 credito - S/ 1.50\n"
        "• 10 creditos - S/ 13.50\n"
        "• 15 creditos - S/ 20.50\n\n"
        "♾️ **DIAS ILIMITADOS:**\n"
        "• 7 dias - S/ 10.00\n"
        "• 15 dias - S/ 13.50\n"
        "• 25 dias - S/ 18.50\n"
        "• 30 dias - S/ 25.00\n\n"
        "🔥 **PROMO ESPECIAL:**\n"
        "⚡ 7 soles x 20 creditos\n"
        "⚡ 13 soles x 30 dias\n\n"
        "👇 **ELIGE DONDE CONTACTARME** 👇"
    )
    await update.message.reply_text(texto, reply_markup=get_botones(), parse_mode="Markdown")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    print("Iniciando bot JOSE BLOQUEO PERU EPIC...")
    app.run_polling(stop_signals=None, close_loop=False)
