import requests
import time

# CONFIGURAÇÕES
WEBHOOK_URL = "https://preview-sandbox--6a28c253504b8c66cc63535f.base44.app/api/webhook/6a28c4df9dce26fdd02abe31"
SECRET_KEY = "lVwqZImjLmJWB6Ay34OxjMPQ88RIssfq"
NICKS_PARA_TESTAR = ["cair", "dormir", "exaltariam"] # Exemplo

def check_nick(nick):
    # NOTA: Aqui você substituiria pela lógica real de verificação do site
    # Exemplo hipotético de checagem:
    response = requests.get(f"https://api.exemplo.com/check/{nick}")
    return response.status_code == 404 # Se 404, geralmente está livre

def main():
    while True:
        for nick in NICKS_PARA_TESTAR:
            if check_nick(nick):
                # Envia para o Base44
                payload = {"nicks": [{"username": nick, "category": "clean"}]}
                headers = {"X-WebHook-Secret": SECRET_KEY, "Content-Type": "application/json"}
                requests.post(WEBHOOK_URL, json=payload, headers=headers)
                print(f"Nick encontrado e enviado: {nick}")
            time.sleep(5) # Delay para evitar banimento

if __name__ == "__main__":
    main()
