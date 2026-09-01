import requests

BOT_TOKEN = "8685515038:AAEW_N4J98oYLIMpP71Fc9W99ha7nR4mJAs"
WEBHOOK_URL = "https://api-mikasa-bot.vercel.app/webhook"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
resp = requests.get(url)
print(resp.json())