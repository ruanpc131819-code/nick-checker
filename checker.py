import requests
import time
import os

# CONFIGURAÇÕES
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://nick-pulse-track.base44.app/api/webhook/6a28c4df9dce26fdd02abe31")
SECRET_KEY = os.environ.get("SECRET_KEY", "lVwqZImjLmJWB6Ay34OxjMPQ88RIssfq")

NICKS_PARA_TESTAR = ["cair", "dormir", "exaltariam"]

def check_nick(nick):
    url = "https://discord.com/api/v9/unique-username/username-attempt-unavailability"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
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
    print("Iniciando o Checker do Discord...")
    while True:
        for nick in NICKS_PARA_TESTAR:
            if check_nick(nick):
                payload = {"nicks": [{"username": nick, "category": "clean"}]}
                headers = {"X-WebHook-Secret": SECRET_KEY, "Content-Type": "application/json"}
                
                try:
                    requests.post(WEBHOOK_URL, json=payload, headers=headers)
                    print(f"Nick disponível e enviado: {nick}")
                except Exception as e:
                    print(f"Falha ao enviar para o Base44: {e}")
            
            time.sleep(15) 

if __name__ == "__main__":
    main()
