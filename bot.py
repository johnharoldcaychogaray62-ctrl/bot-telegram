import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🔥 *JOSE BLOQUEO PERU* 🔥
*¡PRECIOS ACTUALIZADOS!*

💳 *CREDITOS:*
• 1 credito - S/1.50
• 10 creditos - S/13.50
• 15 creditos - S/20.50

⏰ *RENTAS:*
• 7 dias - S/10.00
• 15 dias - S/18.00
• 30 dias - S/30.00

📲 Pago: Yape / Plin
"""
    botones = [
        [InlineKeyboardButton("📢 CANAL OFICIAL", url="https://t.me/josesistema")],
        [InlineKeyboardButton("👥 GRUPO SOPORTE", url="https://t.me/+v7x6gtLnr2gyNTgx")],
        [InlineKeyboardButton("💬 COMPRAR AQUI @josebloqueo", url="https://t.me/josebloqueo")]
    ]
    await update.message.reply_text(texto, reply_markup=InlineKeyboardMarkup(botones), parse_mode="Markdown")

async def start(update, context):
    await buy(update, context)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("buy", buy))
app.add_handler(CommandHandler("start", start))
print("Bot iniciado JOSE BLOQUEO PERU...")
app.run_polling()
