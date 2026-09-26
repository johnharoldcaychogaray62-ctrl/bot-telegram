import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
print(f"Token cargado: {'SI' if TOKEN else 'NO - FALTA EN RENDER'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bot activo! Soy Harold.")

def main():
    if not TOKEN:
        print("ERROR: No hay TOKEN en Environment de Render")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot iniciando polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
