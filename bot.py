import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola John! Soy tu bot y ya estoy prendido 24/7 en Render!")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot iniciado...")
    app.run_polling()

# Servidor web falso para que Render no lo apague
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(('0.0.0.0', port), Handler)
    httpd.serve_forever()

if __name__ == "__main__":
    Thread(target=run_server, daemon=True).start()
    run_bot()
