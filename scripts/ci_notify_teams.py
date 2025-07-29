import os
import requests


def notify_teams(message: str):
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("Webhook do Teams não configurado.")
        return
    payload = {"text": message}
    resp = requests.post(webhook_url, json=payload)
    if resp.status_code == 200:
        print("Notificação enviada para o Teams.")
    else:
        print(f"Falha ao notificar Teams: {resp.status_code}")


if __name__ == "__main__":
    import sys

    msg = sys.argv[1] if len(sys.argv) > 1 else "CI/CD AUDITORIA360 finalizado."
    notify_teams(msg)
