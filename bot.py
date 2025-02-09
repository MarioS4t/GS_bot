# Bot de Telegram

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import requests

# Configuración
BOT_TOKEN = "7587883390:AAFSos6YeOXG9PaMXq50mU7I9JL169Kw79o"
SERVER_URL = "http://192.168.100.56:5000"

# Responder a /start con menú interactivo
async def start(update: Update, context):
    await update.message.reply_text("🔑 Envía un código de acceso para continuar.")

# Generar menú de opciones
def menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📂 Ver catálogo", callback_data="ver_catalogo")],
        [InlineKeyboardButton("🛠 Solicitar un servicio", callback_data="solicitar_servicio")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Manejar los botones del menú
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "ver_catalogo":
        response_text = "📂 Catálogo de Servicios:\n\n1️⃣ Pentesting Web 🕵️‍♂️\n2️⃣ Análisis de Malware 🦠\n3️⃣ Seguridad en APIs 🔐"
        await query.message.edit_text(response_text, reply_markup=catalogo_keyboard())
    elif query.data == "solicitar_servicio":
        await query.message.edit_text("🛠 Selecciona un servicio:", reply_markup=servicios_keyboard())
    elif query.data == "regresar_menu":
        await query.message.edit_text("✅ Has regresado al menú principal.", reply_markup=menu_keyboard())
    elif query.data in ["1", "2", "3"]:
        response_text = obtener_descripcion_servicio(query.data)
        await query.message.edit_text(response_text, reply_markup=regresar_menu_keyboard())

# Generar teclado de servicios
def servicios_keyboard():
    keyboard = [
        [InlineKeyboardButton("1️⃣ Pentesting Web", callback_data="1")],
        [InlineKeyboardButton("2️⃣ Análisis de Malware", callback_data="2")],
        [InlineKeyboardButton("3️⃣ Seguridad en APIs", callback_data="3")],
        [InlineKeyboardButton("Regresar al menú", callback_data="regresar_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Generar teclado de catálogo
def catalogo_keyboard():
    keyboard = [
        [InlineKeyboardButton("Regresar al menú", callback_data="regresar_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Generar teclado de regresar al menú
def regresar_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Regresar al menú", callback_data="regresar_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Obtener descripción del servicio
def obtener_descripcion_servicio(opcion):
    descripciones = {
        "1": "🔍 Pentesting Web: Evaluamos la seguridad de tu sitio.\n💰 Precio: Desde $X,XXX MXN\n📞 Contacto: @TuUsuario",
        "2": "🦠 Análisis de Malware: Realizamos un análisis exhaustivo de tu sistema para detectar malware.\n💰 Precio: Desde $X,XXX MXN\n📞 Contacto: @TuUsuario",
        "3": "🔐 Seguridad en APIs: Evaluamos la seguridad de tus APIs y te brindamos recomendaciones.\n💰 Precio: Desde $X,XXX MXN\n📞 Contacto: @TuUsuario"
    }
    return descripciones.get(opcion, "❌ Opción no válida.")

# Validar código de acceso
async def validar_codigo(update: Update, context):
    user_id = update.message.from_user.id
    codigo = update.message.text.strip()

    response = requests.post(f"{SERVER_URL}/validar", json={"codigo": codigo, "usuario": user_id})
    data = response.json()

    if response.status_code == 200 and data.get("valid"):
        await update.message.reply_text("✅ Código válido. Tienes acceso.", reply_markup=menu_keyboard())
    else:
        await update.message.reply_text("❌ Código inválido o expirado. Intenta de nuevo.")

# Configurar el bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))  # Maneja botones del menú
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, validar_codigo))  # Valida códigos

    print("Bot en funcionamiento...")
    app.run_polling()

if __name__ == "__main__":
    main()
