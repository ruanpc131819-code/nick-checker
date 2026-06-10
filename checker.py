import requests
import time
import threading
import random
import string
import os

# CONFIGURAÇÕES
SECRET_KEY = os.environ.get("SECRET_KEY", "lVwqZImjLmJWB6Ay34OxjMPQ88RIssfq")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://nick-pulse-track.base44.app/api/webhook/6a28c4df9dce26fdd02abe31")

# Listas de palavras para as categorias de texto
VERBOS_SIMPLES = ["cair", "dormir", "correr", "viver", "amar", "rir", "ler", "ver"]
VERBOS_FUTURO = ["apodreceriam", "exaltariam", "correriam", "viveriam", "amariam"]
ENGLISH_WORDS = ["sleep", "dream", "run", "live", "love", "smile", "read", "gold"]

def check_discord(nick, category):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unavailability"
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
    try:
        response = requests.post(url, json={"username": nick}, headers=headers, timeout=5)
        if response.status_code == 200 and not response.json().get("taken", True):
            payload = {"nicks": [{"username": nick, "category": category}]}
            headers = {"X-WebHook-Secret": SECRET_KEY, "Content-Type": "application/json"}
            requests.post(WEBHOOK_URL, json=payload, headers=headers)
            print(f"✅ SUCESSO [{category}]: {nick}")
        else:
            print(f"❌ Ocupado [{category}]: {nick}")
    except Exception as e:
        print(f"Erro [{category}]: {e}")

# --- TAREFAS ---

def task_gerador(tamanho, chars, cat_name):
    while True:
        nick = "".join(random.choices(chars, k=tamanho))
        check_discord(nick, cat_name)
        time.sleep(random.uniform(25, 45))

def task_lista(lista, cat_name):
    while True:
        nick = random.choice(lista)
        check_discord(nick, cat_name)
        time.sleep(random.uniform(25, 45))

# --- INICIALIZAÇÃO ---

tarefas = [
    (3, string.ascii_letters + string.digits, "3C"),
    (3, string.digits, "3N"),
    (3, string.ascii_lowercase, "3L"),
    (4, string.ascii_letters + string.digits, "4C"),
    (4, string.digits, "4N"),
    (4, string.ascii_lowercase, "4L"),
]

threads = []
for t, chars, name in tarefas:
    threads.append(threading.Thread(target=task_gerador, args=(t, chars, name)))

# Adicionando categorias de palavras
threads.append(threading.Thread(target=task_lista, args=(VERBOS_SIMPLES, "Clean")))
threads.append(threading.Thread(target=task_lista, args=(VERBOS_FUTURO, "Futuro")))
threads.append(threading.Thread(target=task_lista, args=(ENGLISH_WORDS, "English")))

for t in threads:
    t.start()
