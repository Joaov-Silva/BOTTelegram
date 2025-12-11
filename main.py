import telebot
from telebot import types

# ===== CONFIG =====
TOKEN = '8090312023:AAH2IC_yvm6tayWgHwlJ0BQ1N74iW_Susgw'    # NÃO MEXER
TARGET_CHAT_ID = -4920887594      # Grupo onde o bot vai reenviar as mensagens
ADMINS = [5855115360]             # IDs autorizados a ligar/desligar o bot

bot = telebot.TeleBot(TOKEN)

bot_active = True


# ========== FUNÇÃO PARA VERIFICAR ADMINS ==========
def is_admin(user_id):
    return user_id in ADMINS


# ========== COMANDO /start E /help ==========
@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):

    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("▶️ Ativar Bot", callback_data="startbot")
    btn_stop = types.InlineKeyboardButton("⏹️ Pausar Bot", callback_data="stopbot")

    markup.add(btn_start, btn_stop)

    bot.reply_to(
        msg,
        "Controle do Bot:\nClique em uma opção:",
        reply_markup=markup
    )


# ========== CALLBACK DOS BOTÕES ==========
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    global bot_active

    # Verificação de admin
    if not is_admin(call.from_user.id):
        return bot.answer_callback_query(
            call.id, "❌ Você não tem permissão.", show_alert=True
        )

    # --- Ligar ---
    if call.data == "startbot":
        bot_active = True
        bot.answer_callback_query(call.id, "Bot ativado!")
        bot.send_message(call.message.chat.id, "▶️ Bot foi ATIVADO!")

    # --- Pausar ---
    elif call.data == "stopbot":
        bot_active = False
        bot.answer_callback_query(call.id, "Bot pausado!")
        bot.send_message(call.message.chat.id, "⏹️ Bot foi PAUSADO!")


# ========== CAPTURA DE MENSAGENS ==========
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'audio', 'voice'])
def forward_and_rewrite(msg: telebot.types.Message):
    global bot_active

    if not bot_active:
        return
    if msg.chat.id == TARGET_CHAT_ID:
        return
    if msg.from_user.is_bot:
        return

    nome = msg.from_user.first_name

    if msg.text:
        bot.send_message(
            TARGET_CHAT_ID,
            f"💬  *{nome} disse:*\n{msg.text}",
            parse_mode="Markdown"
        )

    if msg.photo:
        bot.send_photo(
            TARGET_CHAT_ID,
            msg.photo[-1].file_id,
            caption=f"🖼️ Foto enviada por {nome}"
        )

    if msg.document:
        bot.send_document(
            TARGET_CHAT_ID,
            msg.document.file_id,
            caption=f"📄 Documento enviado por {nome}"
        )

    if msg.video:
        bot.send_video(
            TARGET_CHAT_ID,
            msg.video.file_id,
            caption=f"🎥 Vídeo enviado por {nome}"
        )

    if msg.audio:
        bot.send_audio(
            TARGET_CHAT_ID,
            msg.audio.file_id,
            caption=f"🎵 Áudio enviado por {nome}"
        )

    if msg.voice:
        bot.send_voice(
            TARGET_CHAT_ID,
            msg.voice.file_id,
            caption=f"🎤 Mensagem de voz enviada por {nome}"
        )


# ========== INICIAR O BOT ==========
bot.infinity_polling()
