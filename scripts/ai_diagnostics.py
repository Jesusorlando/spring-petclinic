import os
import sys
import requests
from google import genai
from dotenv import load_dotenv

# 1. Configuración de entorno
load_dotenv()
SLACK_URL = os.getenv("SLACK_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Inicialización del Cliente (SDK v1.0+)
client = genai.Client(api_key=GEMINI_API_KEY)

def send_to_slack(text):
    """Envía el análisis causa raíz al canal de Slack del equipo."""
    if not SLACK_URL:
        print("⚠️ Advertencia: SLACK_WEBHOOK_URL no configurada.")
        return

    payload = {
        "text": "🚨 *AI Diagnostic Report*",
        "attachments": [
            {
                "color": "#ff0000",
                "title": "Análisis de Causa Raíz (RCA)",
                "text": text
            }
        ]
    }
    
    try:
        response = requests.post(SLACK_URL, json=payload)
        response.raise_for_status()
        print("✅ Notificación enviada a Slack con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar a Slack: {e}")

def analyze():
    # 1. Validar argumento de entrada
    if len(sys.argv) < 2:
        print("Uso: python3 ai_diagnostics.py <path_al_log>")
        return

    log_file = sys.argv[1]
    
    try:
        with open(log_file, 'r') as f:
            # Leemos las últimas 100 líneas para el contexto
            log_content = "".join(f.readlines()[-100:])
    except FileNotFoundError:
        print(f"❌ Error: El archivo {log_file} no existe.")
        return

    # 2. Prompt corregido (usando triple comilla para multilínea)
    prompt = f"""Analiza este log de error de mi pipeline en GitHub Actions. 
Identifica la causa raíz y propón una solución técnica detallada:

{log_content}"""
    
    # 3. Generar respuesta
    print("\n--- 🤖 GENERANDO ANÁLISIS DEL AGENTE DE IA ---")
    response = client.models.generate_content(
        model="gemini-2.5-flash", # Ajustado a la versión disponible estable
        contents=prompt
    )
    
    analysis_text = response.text
    print(analysis_text)

    # 4. Notificar al equipo
    send_to_slack(analysis_text)

if __name__ == "__main__":
    analyze()
