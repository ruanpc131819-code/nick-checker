import requests
import time
import os

# CONFIGURAÇÕES - O Railway vai ler estas variáveis se as definires lá
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://nick-pulse-track.base44.app/api/webhook/6a28c4df9dce26fdd02abe31")
SECRET_KEY = os.environ.get("SECRET_KEY", "lVwqZImjLmJWB6Ay34OxjMPQ88RIssfq")

NICKS_PARA_TESTAR = ["cair", "dormir", "exaltariam"]

def check_nick(nick):
    # Endpoint do Discord para verificar nicks
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
            # Se 'taken' for False, o nick está livre
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
                print(f"Nick disponível: {nick}")
                payload = {"nicks": [{"username": nick, "category": "clean"}]}
                headers = {"X-WebHook-Secret": SECRET_KEY, "Content-Type": "application/json"}
                
                try:
                    requests.post(WEBHOOK_URL, json=payload, headers=headers)
                    print(f"Nick enviado para o Base44 com sucesso.")
                except Exception as e:
                    print(f"Falha ao enviar para o Base44: {e}")
            else:
                print(f"Nick ocupado: {nick}")
            
            # Delay de 15 segundos entre cada checagem para evitar bloqueios
            time.sleep(15) 

if __name__ == "__main__":
    main()
