import requests
from bs4 import BeautifulSoup
import os
import time

TOKEN = os.getenv("8548011715:AAHN6uG9S74hlhMjNNHpVdIjqi80rOwJGas")
CHAT_ID = os.getenv("843757701")

PLAYERS = ["Magdalena", "устал пиздц"]
URL = "http://unit-online.ru/online"

seen = set()

def send_message(text):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

while True:
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()

        for player in PLAYERS:
            if player in page_text and player not in seen:
                send_message(f"🔥 Игрок зашел: {player}")
                seen.add(player)

        time.sleep(60)

    except Exception as e:
        print("Ошибка:", e)
        time.sleep(60)
