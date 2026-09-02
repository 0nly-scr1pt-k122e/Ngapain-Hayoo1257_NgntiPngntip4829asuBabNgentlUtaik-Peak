from flask import Flask, request, jsonify
import requests
import json
import logging
import re
import time
from bot import MikasaBot

app = Flask(__name__)
BOT_TOKEN = "8685515038:AAEW_N4J98oYLIMpP71Fc9W99ha7nR4mJAs"
ADMIN_ID = 8873967955

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_instance = MikasaBot(BOT_TOKEN)

# ===================== VARIABEL =====================
stop_spam_flag = {}

# ===================== HELPERS =====================

def send_message(chat_id, text, parse_mode=None, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        return requests.post(url, json=payload, timeout=10)
    except:
        return None

def edit_message_caption(chat_id, message_id, caption, parse_mode=None, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageCaption"
    payload = {"chat_id": chat_id, "message_id": message_id, "caption": caption}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        return requests.post(url, json=payload, timeout=10)
    except:
        return None

def delete_message(chat_id, message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    try:
        return requests.post(url, json={"chat_id": chat_id, "message_id": message_id}, timeout=10)
    except:
        return None

def answer_callback(callback_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    try:
        return requests.post(url, json={"callback_query_id": callback_id}, timeout=10)
    except:
        return None

# ===================== ROUTES =====================

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error"}), 400
        
        logger.info(f"Webhook received")
        
        # ============= HANDLE MESSAGE =============
        if "message" in data:
            msg = data["message"]
            chat_id = str(msg["chat"]["id"])
            user_id = str(msg["from"]["id"])
            first_name = msg["from"].get("first_name", "User")
            text = msg.get("text", "")
            
            if text.startswith("/"):
                parts = text.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                # ===== STOP BOT (HANYA ADMIN) =====
                if cmd == "/stopbot" or cmd == "/matibot":
                    if int(user_id) == ADMIN_ID:
                        bot_instance.send_text(chat_id, "🛑 *Bot sedang dimatikan oleh Admin...*", "Markdown")
                        url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
                        requests.get(url)
                        return
                    else:
                        bot_instance.send_text(chat_id, "❌ *Akses Ditolak!* Hanya Admin yang bisa mematikan bot.", "Markdown")
                
                # ===== CEK USER TERDAFTAR (HANYA ADMIN) =====
                elif cmd == "/cekuser" or cmd == "/users":
                    if int(user_id) == ADMIN_ID:
                        users = bot_instance.users
                        if users:
                            msg_text = "📋 *DAFTAR USER TERDAFTAR*\n\n"
                            for uid, data_user in users.items():
                                status = "✅ Aktif" if data_user.get('status') == 'active' else "⏳ Pending"
                                msg_text += f"🆔 `{uid}`\n"
                                msg_text += f"👤 {data_user.get('nama', 'Unknown')}\n"
                                msg_text += f"📌 Status: {status}\n"
                                msg_text += f"─────────────────\n"
                            bot_instance.send_text(chat_id, msg_text, "Markdown")
                        else:
                            bot_instance.send_text(chat_id, "📋 *Belum ada user yang terdaftar.*", "Markdown")
                    else:
                        bot_instance.send_text(chat_id, "❌ *Akses Ditolak!* Hanya Admin yang bisa melihat user.", "Markdown")
                
                # ===== STOP SPAM =====
                elif cmd == "/berhenti" or cmd == "/stop":
                    stop_spam_flag[chat_id] = True
                    bot_instance.send_text(chat_id, "🛑 *Proses Spam Dihentikan!*", "Markdown")
                
                # ===== REGISTER & VERIFY =====
                elif cmd == "/start":
                    bot_instance.start_sync(chat_id, user_id, first_name)
                
                elif cmd == "/register":
                    if args:
                        bot_instance.register_sync(chat_id, user_id, " ".join(args))
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /register nama_anda")
                
                elif cmd == "/verify":
                    if args:
                        bot_instance.verify_sync(chat_id, user_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /verify user_id")
                
                # ===== SPAM COMMANDS =====
                elif cmd == "/spamotp":
                    if args:
                        stop_spam_flag[chat_id] = False
                        bot_instance.spam_otp_sync(chat_id, args[0], stop_spam_flag, chat_id)
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /spamotp 628xxxxxxxxx")
                
                elif cmd == "/spamcall":
                    if args:
                        stop_spam_flag[chat_id] = False
                        bot_instance.spam_call_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /spamcall 62xxxxxxxxx")
                
                elif cmd == "/spampair":
                    if args:
                        stop_spam_flag[chat_id] = False
                        bot_instance.spam_pair_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /spampair 628xxxxxxxxx")
                
                elif cmd == "/spamrepwa":
                    if args:
                        stop_spam_flag[chat_id] = False
                        bot_instance.spam_repwa_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /spamrepwa +628xxxxxxxxx")
                
                elif cmd == "/spamngl":
                    if args:
                        stop_spam_flag[chat_id] = False
                        bot_instance.spam_ngl_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /spamngl username")
                
                elif cmd == "/spamgmail":
                    if args:
                        stop_spam_flag[chat_id] = False
                        target_email = args[0]
                        custom_message = " ".join(args[1:]) if len(args) > 1 else None
                        bot_instance.spam_gmail_sync(chat_id, target_email, custom_message)
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /spamgmail target@gmail.com")
                
                # ===== OSINT & TRACKER =====
                elif cmd == "/osint":
                    bot_instance.osint_sync(chat_id)
                
                elif cmd == "/osintnomor":
                    if args:
                        bot_instance.osint_nomor_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /osintnomor +628xxxxxxxxx")
                
                elif cmd == "/osintusername":
                    if args:
                        bot_instance.osint_username_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /osintusername username")
                
                elif cmd == "/osintip":
                    if args:
                        bot_instance.osint_ip_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /osintip 8.8.8.8")
                
                elif cmd == "/osintdomain":
                    if args:
                        bot_instance.osint_domain_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /osintdomain google.com")
                
                elif cmd == "/iptracker":
                    if args:
                        bot_instance.ip_tracker_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /iptracker 8.8.8.8")
                
                elif cmd == "/portscan":
                    if args:
                        bot_instance.port_scan_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /portscan google.com")
                
                # ===== UTILITY =====
                elif cmd == "/nikparse":
                    if args:
                        bot_instance.nik_parse_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /nikparse 3307110101990001")
                
                elif cmd == "/cekkodepos":
                    if args:
                        bot_instance.cek_kodepos_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /cekkodepos 16112")
                
                elif cmd == "/ceknpsn":
                    if args:
                        bot_instance.cek_npsn_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /ceknpsn 40203594")
                
                elif cmd == "/ffuid":
                    if args:
                        bot_instance.ff_uid_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /ffuid 10353221131")
                
                elif cmd == "/cekroblox":
                    if args:
                        bot_instance.cek_roblox_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /cekroblox Builderman")
                
                elif cmd == "/cekdataguru":
                    if args:
                        bot_instance.cek_dataguru_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /cekdataguru 1234567890123456")
                
                elif cmd == "/cekimei":
                    if args:
                        bot_instance.cek_imei_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /cekimei 353911112345678")
                
                elif cmd == "/cekphising":
                    if args:
                        bot_instance.cek_phising_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /cekphising https://example.com")
                
                elif cmd == "/webrecon":
                    if args:
                        bot_instance.web_recon_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /webrecon google.com")
                
                elif cmd == "/shortenerurl":
                    if args:
                        bot_instance.shortener_url_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /shortenerurl https://www.tokopedia.com")
                
                elif cmd == "/cekresi":
                    if len(args) >= 2:
                        bot_instance.cek_resi_sync(chat_id, args[0], args[1])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /cekresi jne 1234567890")
                
                # ===== BOT TELEGRAM UTILITY =====
                elif cmd == "/killbottele":
                    if args:
                        bot_instance.kill_bottele_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /killbottele 1234567890:ABCdef")
                
                elif cmd == "/cekinfobot":
                    if args:
                        bot_instance.cek_infobot_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /cekinfobot 1234567890:ABCdef")
                
                elif cmd == "/getidchatbot":
                    if args:
                        bot_instance.get_id_chat_sync(chat_id, args[0])
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /getidchatbot 1234567890:ABCdef")
                
                elif cmd == "/spambottele":
                    if len(args) >= 3:
                        bot_instance.spam_bottele_sync(chat_id, args[0], args[1], " ".join(args[2:]))
                    else:
                        bot_instance.send_text(chat_id, "❌ Format: /spambottele token idchat pesan")
                
                # ===== MISC =====
                elif cmd == "/laporbug":
                    bot_instance.lapor_bug_sync(chat_id)
                
                elif cmd == "/fototourl":
                    bot_instance.foto_tourl_sync(chat_id)
                
                elif cmd == "/filetourl":
                    bot_instance.file_tourl_sync(chat_id)
                
                elif cmd == "/hackstatuswa":
                    bot_instance.hack_status_wa_sync(chat_id)
                
                else:
                    bot_instance.send_text(chat_id, f"❌ Command tidak dikenal: {cmd}")
        
        # ============= HANDLE CALLBACK QUERY =============
        elif "callback_query" in data:
            query = data["callback_query"]
            chat_id = str(query["message"]["chat"]["id"])
            message_id = query["message"]["message_id"]
            callback_id = query["id"]
            data_callback = query["data"]
            
            answer_callback(callback_id)
            
            if data_callback == "menu_spam":
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "⬅️ Kembali", "callback_data": "menu_back"}]
                    ]
                }
                caption = (
                    f" KATEGORI SPAM\n\n"
                    f"╭───〔 1 〕───╮\n"
                    f"│ 𝙎𝙋𝘼𝙈 𝙈𝙀𝙉𝙐 :\n"
                    f"│ /spamotp\n"
                    f"│ /spamcall\n"
                    f"│ /spampair\n"
                    f"│ /spamrepwa\n"
                    f"│ /spamngl\n"
                    f"│ /spamgmail\n"
                    f"│ /berhenti\n"
                    f"╰────────────────────────────╯\n\n"
                    f"📌 *Cara penggunaan:*\n"
                    f"Ketik command di atas dengan nomor target\n"
                    f"Gunakan /berhenti untuk menghentikan proses spam"
                )
                edit_message_caption(chat_id, message_id, caption, "Markdown", json.dumps(keyboard))
            
            elif data_callback == "menu_osint":
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "⬅️ Kembali", "callback_data": "menu_back"}]
                    ]
                }
                caption = (
                    f" KATEGORI OSINT & TRACKING\n\n"
                    f"╭───〔 2 〕───╮\n"
                    f"│ 𝙊𝙎𝙄𝙉𝙏 & 𝙏𝙍𝘼𝘾𝙆𝙄𝙉𝙂 :\n"
                    f"│ /osintnomor\n"
                    f"│ /osintusername\n"
                    f"│ /osintip\n"
                    f"│ /osintdomain\n"
                    f"│ /iptracker\n"
                    f"│ /portscan\n"
                    f"│ /nikparse\n"
                    f"╰────────────────────────────╯\n\n"
                    f"📌 *Cara penggunaan:*\n"
                    f"Ketik command di atas dengan target"
                )
                edit_message_caption(chat_id, message_id, caption, "Markdown", json.dumps(keyboard))
            
            elif data_callback == "menu_utility":
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "⬅️ Kembali", "callback_data": "menu_back"}]
                    ]
                }
                caption = (
                    f" KATEGORI UTILITY\n\n"
                    f"╭───〔 3 〕───╮\n"
                    f"│ 𝙐𝙏𝙄𝙇𝙄𝙏𝙔 𝙈𝙀𝙉𝙐 :\n"
                    f"│ /cekkodepos\n"
                    f"│ /ceknpsn\n"
                    f"│ /ffuid\n"
                    f"│ /cekroblox\n"
                    f"│ /cekdataguru\n"
                    f"│ /cekimei\n"
                    f"│ /cekphising\n"
                    f"│ /webrecon\n"
                    f"│ /fototourl\n"
                    f"│ /filetourl\n"
                    f"│ /shortenerurl\n"
                    f"│ /cekresi\n"
                    f"╰────────────────────────────╯\n\n"
                    f"📌 *Cara penggunaan:*\n"
                    f"Ketik command di atas dengan target"
                )
                edit_message_caption(chat_id, message_id, caption, "Markdown", json.dumps(keyboard))
            
            elif data_callback == "menu_all":
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "⬅️ Kembali", "callback_data": "menu_back"}]
                    ]
                }
                caption = (
                    f" 𝐌𝐄𝐍𝐔 𝐀𝐋𝐋 𝐌𝐈𝐊𝐀𝐒𝐀\n\n"
                    f"╭───〔 ♛♛ 〕───╮\n"
                    f"│ 𝙈𝙀𝙉𝙐 𝘽𝙊𝙏 𝙈𝙄𝙆𝘼𝙎𝘼🥘 :\n"
                    f"│ /spamotp\n"
                    f"│ /spamcall\n"
                    f"│ /spampair\n"
                    f"│ /spamrepwa\n"
                    f"│ /spamngl\n"
                    f"│ /osint\n"
                    f"│ /iptracker\n"
                    f"│ /portscan\n"
                    f"│ /nikparse\n"
                    f"│ /cekkodepos\n"
                    f"│ /ceknpsn\n"
                    f"│ /ffuid\n"
                    f"│ /cekroblox\n"
                    f"│ /spamgmail\n"
                    f"│ /cekdataguru\n"
                    f"│ /spambottele\n"
                    f"│ /cekimei\n"
                    f"│ /cekphising\n"
                    f"│ /webrecon\n"
                    f"│ /laporbug\n"
                    f"│ /fototourl\n"
                    f"│ /filetourl\n"
                    f"│ /killbottele\n"
                    f"│ /cekinfobot\n"
                    f"│ /shortenerurl\n"
                    f"│ /hackstatuswa\n"
                    f"│ /cekresi\n"
                    f"│ /getidchatbot\n"
                    f"│ /berhenti\n"
                    f"╰────────────────────────────╯\n\n"
                    f"📌 *Cara penggunaan:*\n"
                    f"Ketik command di atas dengan format yang sesuai\n"
                    f"Gunakan /berhenti untuk menghentikan proses spam"
                )
                edit_message_caption(chat_id, message_id, caption, "Markdown", json.dumps(keyboard))
            
            elif data_callback == "menu_back":
                keyboard = {
                    "inline_keyboard": [
                        [{"text": "〔 1 〕𝐒𝐏𝐀𝐌 𝐌𝐄𝐍𝐔", "callback_data": "menu_spam"}],
                        [{"text": "〔 2 〕𝐎𝐒𝐈𝐍𝐓 & 𝐓𝐀𝐑𝐂𝐊𝐄𝐑", "callback_data": "menu_osint"}],
                        [{"text": "〔 3 〕𝐔𝐓𝐈𝐋𝐈𝐓𝐘", "callback_data": "menu_utility"}],
                        [{"text": "〔 4 〕𝐌𝐄𝐍𝐔 𝐀𝐋𝐋", "callback_data": "menu_all"}],
                        [{"text": "〔 5 〕𝐂𝐋𝐎𝐒𝐄", "callback_data": "menu_close"}],
                    ]
                }
                caption = (
                    f"𝙈𝙄𝙆𝘼𝙎𝘼 𝘽𝙊𝙏 𝙈𝘿\n"
                    f"𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑: 𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔\n\n"
                    f"𝙿𝚒𝚕𝚒𝚑 𝚔𝚊𝚝𝚎𝚐𝚘𝚛𝚒 𝚍𝚒 𝚋𝚊𝚠𝚊𝚑 👇"
                )
                edit_message_caption(chat_id, message_id, caption, "Markdown", json.dumps(keyboard))
            
            elif data_callback == "menu_close":
                delete_message(chat_id, message_id)
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

# ===================== UNTUK VERCEL =====================
application = app
