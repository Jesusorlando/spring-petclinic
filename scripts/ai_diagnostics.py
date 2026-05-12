import os
import sys
from google import genai
from dotenv import load_dotenv

# 1. Configuración de entorno
load_dotenv()
SLACK_URL = os.getenv("SLACK_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Inicialización del Cliente (Nuevo SDK)
client = genai.Client(api_key=GEMINI_API_KEY)

def analyze():
    # 1. Leer el archivo de log que pasamos por argumento
    log_file = sys.argv[1]
    with open(log_file, 'r') as f:
        # Leemos las últimas 100 líneas para no saturar el context window
        log_content = "".join(f.readlines()[-100:])

    
    prompt = f"Analiza este log de error de mi pipeline 
    y dime la causa raíz y solución:\n\n{log_content}"
    
    # 3. Generar respuesta
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    print("\n--- 🤖 ANÁLISIS DEL AGENTE DE IA ---")
    print(response.text)

if __name__ == "__main__":
    analyze()
