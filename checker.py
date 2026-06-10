import requests
import time
import os
import itertools
import string

# CONFIGURAÇÕES
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://nick-pulse-track.base44.app/api/webhook/6a28c4df9dce26fdd02abe31")
SECRET_KEY = os.environ.get("SECRET_KEY", "lVwqZImjLmJWB6Ay34OxjMPQ88RIssfq")

# Define os caracteres que o bot vai usar para criar os nicks (ex: letras de a-z)
CARACTERES = string.ascii_lowercase 

def gerar_nicks():
    # Gera combinações de 3 letras (pode mudar para 4, 5, etc.)
    for tamanho in range(3, 4):
        for combinacao in itertools.product(CARACTERES, repeat=tamanho):
            yield "".join(combinacao)

def check_nick(nick):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unavailability"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json"
    }
    payload = {"username": nick}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return not data.get("taken", True)
        return False
    except Exception as e:
        print(f"Erro ao checar {nick}: {e}")
        return False

def main():
    print("Iniciando gerador de combinações...")
    # O loop vai percorrer todas as combinações possíveis
    for nick in gerar_nicks():
        if check_nick(nick):
            print(f"Nick disponível: {nick}")
            payload = {"nicks": [{"username": nick, "category": "clean"}]}
            headers = {"X-WebHook-Secret": SECRET_KEY, "Content-Type": "application/json"}
            requests.post(WEBHOOK_URL, json=payload, headers=headers)
        else:
            print(f"Ocupado: {nick}")
        
        # Delay importante para não ser banido pelo Discord
        time.sleep(20) 

if __name__ == "__main__":
    main()
