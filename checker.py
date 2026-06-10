import requests
import time
import threading
import random
import string
import os
import itertools

# CONFIGURAÇÕES DE AMBIENTE
SECRET_KEY = os.environ.get("SECRET_KEY", "lVwqZImjLmJWB6Ay34OxjMPQ88RIssfq")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://nick-pulse-track.base44.app/api/webhook/6a28c4df9dce26fdd02abe31")

# LISTAS DE DADOS (Expanda estas listas para tornar o bot infinito)
RADICAIS = ["afog", "sumir", "colh", "dorm", "fug", "bat", "sent", "beb", "vend", "exalt", "apodrec", "viv", "am"]
SUFIXOS = ["ariam", "eriam", "iriam", "assem", "eis", "mente", "ado", "ante", "avel", "ico"]
ENGLISH_WORDS = ["sleep", "dream", "run", "live", "love", "smile", "read", "gold", "dark", "light"]

def log(status, category, nick, message=""):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {status} [{category}]: {nick} {message}")

def check_discord(nick, category):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unavailability"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json={"username": nick}, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not data.get("taken", True):
                log("✅ SUCESSO", category, nick)
                payload = {"nicks": [{"username": nick, "category": category}]}
                auth_headers = {"X-WebHook-Secret": SECRET_KEY, "Content-Type": "application/json"}
                requests.post(WEBHOOK_URL, json=payload, headers=auth_headers, timeout=5)
            else:
                log("❌ Ocupado", category, nick)
        elif response.status_code == 429:
            log("⚠️ RATELIMIT", category, nick, "Aguardando cooldown...")
            time.sleep(1)
    except Exception as e:
        log("⚠️ ERRO", category, nick, str(e))

# --- TAREFAS DE GERAÇÃO ---

def task_iterativa(tamanho, chars, cat_name):
    """Gera combinações sequenciais sem repetição usando itertools"""
    for nick_tuple in itertools.product(chars, repeat=tamanho):
        nick = "".join(nick_tuple)
        check_discord(nick, cat_name)
        time.sleep(random.uniform(25, 50))

def task_combinatoria_criativa(cat_name):
    """Combina radicais e sufixos para criar nicks com sentido"""
    while True:
        nick = random.choice(RADICAIS) + random.choice(SUFIXOS)
        check_discord(nick, cat_name)
        time.sleep(random.uniform(30, 60))

def task_lista_aleatoria(lista, cat_name):
    """Mistura listas fixas para evitar ciclos viciosos"""
    while True:
        random.shuffle(lista)
        for nick in lista:
            check_discord(nick, cat_name)
            time.sleep(random.uniform(30, 60))

# --- INICIALIZAÇÃO DO MOTOR ---

tarefas = [
    (3, string.ascii_letters + string.digits, "3C"),
    (3, string.digits, "3N"),
    (3, string.ascii_lowercase, "3L"),
    (4, string.ascii_letters + string.digits, "4C"),
    (4, string.digits, "4N"),
    (4, string.ascii_lowercase, "4L"),
]

threads = []

# Criar threads para geradores sequenciais
for t, chars, name in tarefas:
    threads.append(threading.Thread(target=task_iterativa, args=(t, chars, name), daemon=True))

# Criar threads para geradores criativos
threads.append(threading.Thread(target=task_combinatoria_criativa, args=("Futuro_Criativo",), daemon=True))
threads.append(threading.Thread(target=task_lista_aleatoria, args=(ENGLISH_WORDS, "English_Words"), daemon=True))

# Iniciar todas as threads
log("🚀 SISTEMA", "GERAL", "Iniciando bot com todas as threads...")
for t in threads:
    t.start()

# Manter o programa principal rodando
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    log("🛑 SISTEMA", "GERAL", "Bot encerrado pelo usuário.")
