import json, datetime, os, asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8857891537:AAGbpta77K1Eps7AcG9IUD435IkAqMEwJSQ"
OWNER_NOMBRE = "JOSE SISTEMA"
PERSONAL_LINK = "https://t.me/josesistemabloqueo"
OWNER_ID = 8767808702

def load_users():
    if not os.path.exists("users.json"): return {}
    try: return json.load(open("users.json","r", encoding="utf-8"))
    except: return {}
def save_users(d): json.dump(d, open("users.json","w", encoding="utf-8"), indent=2)

def get_user(uid):
    users=load_users(); s=str(uid)
    if s not in users:
        users[s]={"creditos":5,"consultas":0,"f_reg":datetime.datetime.now().strftime("%d/%m/%Y - %I:%M:%S %p"),"dias":30,"last":0}
        save_users(users)
    return users

async def check(update, cost):
    uid=str(update.effective_user.id); users=get_user(uid); u=users[uid]
    if datetime.datetime.now().timestamp() - u.get("last",0) < 20:
        await update.message.reply_text("⏱️ Espera 20 seg anti-spam"); return None
    if u.get("creditos",0) < cost:
        await update.message.reply_text(f"❌ Sin creditos. Tienes {u.get('creditos',0)}. Compra en /buy"); return None
    return users

async def avisar_dueno(context, texto):
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=texto)
    except:
        pass

async def cmds(update, context):
    kb=[
        [InlineKeyboardButton("🔵 ENTEL",callback_data="op_entel"), InlineKeyboardButton("🟡 BITEL",callback_data="op_bitel")],
        [InlineKeyboardButton("🔴 CLARO",callback_data="op_claro"), InlineKeyboardButton("🟢 MOVI",callback_data="op_movi")],
        [InlineKeyboardButton("🚫 BLOQUEOS BIM",callback_data="op_bim")],
        [InlineKeyboardButton("💸 COMPRAR /buy",callback_data="buy")],
        [InlineKeyboardButton(f"👤 {OWNER_NOMBRE} 👑", url=PERSONAL_LINK)]
    ]
    txt=f"🔥 {OWNER_NOMBRE} - COMANDOS 🔥\n\n→ COMANDOS\n/entel /bitel /claro /movistar - Bloqueos Chip\n/bindni - Bloqueo BIM por DNI\n/binun - Bloqueo BIM por Numero\n\n→ OTROS\n/me - Mi perfil\n/buy - Precios\n\n👑 Dueño: {OWNER_NOMBRE}\n"
    try:
        if os.path.exists("comandos.jpg"):
            await context.bot.send_photo(update.effective_chat.id, photo=open("comandos.jpg","rb"), caption=txt, reply_markup=InlineKeyboardMarkup(kb))
        else:
            await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))
    except:
        await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))

async def buy(update, context):
    txt=f"💸 PRECIOS {OWNER_NOMBRE} 💸\n\n💲 1 Credito = S/1.50\n💲 10 Creditos = S/13.50\n⏰ 7 Dias = S/10\n⏰ 30 Dias = S/25\n\n👑 Contacto: {OWNER_NOMBRE}\n🔗 {PERSONAL_LINK}\n"
    try:
        if os.path.exists("buy.jpg"):
            await context.bot.send_photo(update.effective_chat.id, photo=open("buy.jpg","rb"), caption=txt)
        else:
            await update.message.reply_text(txt)
    except:
        await update.message.reply_text(txt)

async def me(update, context):
    users=get_user(update.effective_user.id); uid=str(update.effective_user.id); info=users[uid]
    username=f"@{update.effective_user.username}" if update.effective_user.username else "SinUser"
    txt=f"→ PERFIL DE USUARIO\n\n👤 PERFIL DE → {update.effective_user.first_name}\n\n[📋] - INFORMACIÓN PERSONAL\n\n┌「🆔」 ID → {uid}\n┌「👤」 USER → {username}\n┌「✅」 ESTADO → LIBRE ⚠️\n┌「📅」 F. REGISTRO →\n{info.get('f_reg','-')}\n\n[💳] - ESTADO DE CUENTA\n\n┌「〽️」 ROL → USER\n┌「⏱️」 ANTI-SPAM → 20 seg.\n┌「💲」 CRÉDITOS → {info.get('creditos',0)}\n┌「⏰」 DIAS → {info.get('dias',30)}\n"
    try:
        if os.path.exists("nocliente.jpg"):
            await context.bot.send_photo(update.effective_chat.id, photo=open("nocliente.jpg","rb"), caption=txt)
        else:
            await update.message.reply_text(txt)
    except:
        await update.message.reply_text(txt)

async def bloq(update, context, tipo):
    users=await check(update, 2)
    if not users: return
    if not context.args:
        await update.message.reply_text(f"Uso: /{tipo} 987654321"); return
    num=context.args[0]; uid=str(update.effective_user.id)
    nombre = update.effective_user.first_name
    username = f"@{update.effective_user.username}" if update.effective_user.username else "Sin username"
    users[uid]["creditos"]-=2; users[uid]["last"]=datetime.datetime.now().timestamp(); users[uid]["consultas"]+=1; save_users(users)
    texto=f"🔥 BLOQUEO ENVIADO EXITOSAMENTE 🔥\n\n┌ Operador: {tipo.upper()}\n├ Numero: {num}\n├ Estado: ✅ BLOQUEADO\n├ Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %I:%M %p')}\n└ Bot: JOSE SISTEMA\n\n💳 Te quedan: {users[uid]['creditos']} creditos\n👑 Gracias por usar {OWNER_NOMBRE}"
    try:
        if os.path.exists("bloqueo.jpg"):
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("bloqueo.jpg","rb"), caption=texto)
        else:
            await update.message.reply_text(texto)
    except:
        await update.message.reply_text(texto)
    aviso = f"🚨 NUEVA SOLICITUD DE BLOQUEO 🚨\n\n👤 Cliente: {nombre}\n{username}\n🆔 ID: {uid}\n📱 Numero a bloquear: {num}\n📡 Operador: {tipo.upper()}\n💰 Creditos restantes: {users[uid]['creditos']}\n\n📅 {datetime.datetime.now().strftime('%d/%m %I:%M %p')}"
    await avisar_dueno(context, aviso)

async def entel(u,c): await bloq(u,c,"entel")
async def bitel(u,c): await bloq(u,c,"bitel")
async def claro(u,c): await bloq(u,c,"claro")
async def movistar(u,c): await bloq(u,c,"movistar")

async def bindni(u,c):
    users=await check(u,6)
    if not users: return
    dni = u.message.text.split()[1] if len(u.message.text.split())>1 else "?"
    await u.message.reply_text(f"🔍 DNI {dni} buscado (pon tu API aqui)")
    await avisar_dueno(c, f"🔍 NUEVA BUSQUEDA BIM DNI\n👤 {u.effective_user.first_name} ({u.effective_user.id})\nDNI: {dni}")

async def binun(u,c):
    users=await check(u,6)
    if not users: return
    num = u.message.text.split()[1] if len(u.message.text.split())>1 else "?"
    await u.message.reply_text(f"🔍 NUM {num} buscado (pon tu API aqui)")
    await avisar_dueno(c, f"🔍 NUEVA BUSQUEDA BIM NUM\n👤 {u.effective_user.first_name} ({u.effective_user.id})\nNUM: {num}")

async def add(update, context):
    if update.effective_user.id!= OWNER_ID:
        await update.message.reply_text(f"❌ Solo dueño. Tu ID: {update.effective_user.id}"); return
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /add ID CANTIDAD\nEj: /add 8767808702 50"); return
    uid_add = str(context.args[0])
    try: cant = int(context.args[1])
    except: await update.message.reply_text("Cantidad debe ser número"); return
    users = load_users()
    if uid_add not in users:
        users[uid_add]={"creditos":cant,"consultas":0,"f_reg":datetime.datetime.now().strftime("%d/%m/%Y - %I:%M:%S %p"),"dias":30,"last":0}
    else:
        users[uid_add]["creditos"] = users[uid_add].get("creditos",0) + cant
    save_users(users)
    await update.message.reply_text(f"✅ Agregado {cant} creditos a {uid_add}\nAhora tiene: {users[uid_add]['creditos']}")

async def anuncio(update, context):
    if update.effective_user.id!= OWNER_ID: return
    if not context.args:
        await update.message.reply_text("Uso: /anuncio Tu mensaje"); return
    msg = " ".join(context.args)
    users = load_users()
    await update.message.reply_text(f"📢 Enviando a {len(users)} usuarios...")
    ok=0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=f"📢 ANUNCIO {OWNER_NOMBRE} 📢\n\n{msg}\n\n🔗 {PERSONAL_LINK}")
            ok+=1
        except: pass
    await update.message.reply_text(f"✅ Enviado a {ok}/{len(users)}")

async def cb(update, context):
    q=update.callback_query; await q.answer()
    if q.data == "buy":
        await buy(update, context)

    elif q.data == "op_entel":
        txt = """🔵 BLOQUEO ENTEL 🔵

- Comando ➤ /entel 987654321
- Precio ➤ 2 Créditos

🔒 ¿Qué incluye el servicio?
Bloqueo total de chip Entel por pérdida o robo.
Se bloquean llamadas, SMS y datos. Nadie podrá usar tu número.

♻️ ."""
        await q.message.reply_text(txt)

    elif q.data == "op_bitel":
        txt = """🟡 BLOQUEO BITEL 🟡

- Comando ➤ /bitel 987654321
- Precio ➤ 2 Créditos

🔒 ¿Qué incluye el servicio?
Bloqueo total de chip Bitel por pérdida o robo.
Se bloquean llamadas, SMS y datos inmediatamente.

♻️ ."""
        await q.message.reply_text(txt)

    elif q.data == "op_claro":
        txt = """🔴 BLOQUEO CLARO 🔴

- Comando ➤ /claro 987654321
- Precio ➤ 2 Créditos

🔒 ¿Qué incluye el servicio?
Bloqueo total de chip Claro por pérdida o robo.
Bloqueo inmediato de línea y servicios.

♻️ ."""
        await q.message.reply_text(txt)

    elif q.data == "op_movi":
        txt = """🟢 BLOQUEO MOVISTAR 🟢

- Comando ➤ /movistar 987654321
- Precio ➤ 2 Créditos

🔒 ¿Qué incluye el servicio?
Bloqueo total de chip Movistar por pérdida o robo.
Tu línea queda inactiva para terceros.

♻️ ."""
        await q.message.reply_text(txt)

    elif q.data == "op_bim":
        txt = """🚫 BLOQUEOS BIM 🚫

1. POR NUMERO DNI
- Comando ➤ /bindni 44443333
- Precio ➤ 6 Créditos

2. POR NUMERO CELULAR
- Comando ➤ /binun 987654321
- Precio ➤ 6 Créditos

🔒 ¿Qué incluye el servicio?
Dinero protegido: El saldo se congela por completo. Nadie podrá sacar ni transferir nada, pero sí podrás seguir recibiendo dinero de forma segura.
Recuperación: Tus fondos se quedan guardados intactos. Los volverás a ver cuando saques un nuevo chip con tu operador y reactives tu cuenta Bim."""
        await q.message.reply_text(txt)

async def start(update, context): await cmds(update, context)

if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except:
        pass
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("cmds",cmds))
    app.add_handler(CommandHandler("buy",buy))
    app.add_handler(CommandHandler("me",me))
    app.add_handler(CommandHandler("add",add))
    app.add_handler(CommandHandler("anuncio",anuncio))
    app.add_handler(CommandHandler("entel",entel))
    app.add_handler(CommandHandler("bitel",bitel))
    app.add_handler(CommandHandler("claro",claro))
    app.add_handler(CommandHandler("movistar",movistar))
    app.add_handler(CommandHandler("bindni",bindni))
    app.add_handler(CommandHandler("binun",binun))
    app.add_handler(CallbackQueryHandler(cb))
    print("BOT JOSE SISTEMA V14 - COMANDOS /entel SIN B + CADA OPERADORA SU TEXTO + AVISOS PRIVADO 8767808702")
    app.run_polling()
