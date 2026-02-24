import requests
from bs4 import BeautifulSoup
import os

# Telegram bot token and chat ID from environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Players to watch
PLAYERS = ["Magdalena", "устал пиздц"]
URL = "http://unit-online.ru/online"

# File to store already notified players
SEEN_FILE = "seen.txt"
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        seen = set(f.read().splitlines())
else:
    seen = set()

def send_message(text):
    try:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=10
        )
    except Exception as e:
        print("Telegram send error:", e)

try:
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text()

    new_seen = set(seen)

    for player in PLAYERS:
        if player in page_text and player not in seen:
            send_message(f"Player online: {player}")
            new_seen.add(player)

    # Save updated seen list
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        for s in new_seen:
            f.write(s + "\n")

except Exception as e:
    print("Check error:", e)
