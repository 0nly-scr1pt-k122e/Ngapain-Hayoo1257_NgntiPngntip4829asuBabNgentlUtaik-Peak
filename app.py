import os
import json
import requests
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8685515038:AAEW_N4J98oYLIMpP71Fc9W99ha7nR4mJAs")

def save_log(data):
    """Simpan log ke file"""
    try:
        with open("logs.txt", "a") as f:
            f.write(json.dumps(data) + "\n")
    except:
        pass

def send_log_to_admin(chat_id, username, text, command):
    try:
        message = (
            f"📋 *LOG ACTIVITY BOT*\n\n"
            f"🕐 Waktu: {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}\n"
            f"🆔 User ID: `{chat_id}`\n"
            f"👤 Username: @{username or 'Unknown'}\n"
            f"📝 Pesan: `{text or 'Tidak ada'}`\n"
            f"⚡ Command: `{command or 'Tidak ada'}`"
        )
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": 8873967955,  # Admin ID kamu
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def get_logs():
    try:
        with open("logs.txt", "r") as f:
            logs = [json.loads(line.strip()) for line in f if line.strip()]
        return logs
    except:
        return []

def get_user_stats():
    """Statistik user"""
    logs = get_logs()
    users = {}
    for log in logs:
        chat_id = log.get("chat_id")
        if chat_id:
            if chat_id not in users:
                users[chat_id] = {
                    "username": log.get("username", "Unknown"),
                    "total_pesan": 0,
                    "last_active": log.get("time", "")
                }
            users[chat_id]["total_pesan"] += 1
            users[chat_id]["last_active"] = log.get("time", "")
    return users

@app.route("/", methods=["GET"])
def index():
    return "Bot is running with Log Monitor!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            username = data["message"]["chat"].get("username", "Unknown")
            text = data["message"].get("text", "")
            first_name = data["message"]["chat"].get("first_name", "")
            
            # Deteksi command
            command = None
            if text and text.startswith("/"):
                command = text.split()[0]
            
            # Simpan log
            log_data = {
                "time": datetime.now().strftime('%H:%M:%S - %d/%m/%Y'),
                "chat_id": chat_id,
                "username": username,
                "first_name": first_name,
                "text": text,
                "command": command
            }
            save_log(log_data)
            
            # Kirim notifikasi ke admin (cuma untuk command tertentu biar ga spam)
            if command:
                send_log_to_admin(chat_id, username, text, command)
            
            # Balik response
            return {"status": "ok", "log": log_data}, 200
        
        return {"status": "ok"}, 200
        
    except Exception as e:
        return {"status": "error", "error": str(e)}, 200

@app.route("/logs", methods=["GET"])
def view_logs():
    """Lihat semua log via browser"""
    logs = get_logs()
    if not logs:
        return "<h3>Belum ada log</h3>"
    
    html = "<h2>📋 LOG ACTIVITY BOT</h2>"
    html += "<table border='1' cellpadding='5'>"
    html += "<tr><th>Waktu</th><th>User ID</th><th>Username</th><th>Pesan</th><th>Command</th></tr>"
    
    for log in logs[-50:]:  # 50 log terakhir
        html += f"<tr>"
        html += f"<td>{log.get('time', '')}</td>"
        html += f"<td>{log.get('chat_id', '')}</td>"
        html += f"<td>@{log.get('username', 'Unknown')}</td>"
        html += f"<td>{log.get('text', '')}</td>"
        html += f"<td>{log.get('command', '')}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

@app.route("/stats", methods=["GET"])
def view_stats():
    """Lihat statistik user via browser"""
    users = get_user_stats()
    if not users:
        return "<h3>Belum ada data user</h3>"
    
    html = "<h2>📊 STATISTIK USER</h2>"
    html += "<table border='1' cellpadding='5'>"
    html += "<tr><th>User ID</th><th>Username</th><th>Total Pesan</th><th>Last Active</th></tr>"
    
    for chat_id, data in users.items():
        html += f"<tr>"
        html += f"<td>{chat_id}</td>"
        html += f"<td>@{data.get('username', 'Unknown')}</td>"
        html += f"<td>{data.get('total_pesan', 0)}</td>"
        html += f"<td>{data.get('last_active', '')}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

@app.route("/keepalive", methods=["GET"])
def keepalive():
    return "Alive!", 200

if __name__ == "__main__":
    app.run()