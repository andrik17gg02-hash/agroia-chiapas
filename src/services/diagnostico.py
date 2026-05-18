import anthropic
import base64
import json
import os
from dotenv import load_dotenv

def diagnosticar_planta(imagen_bytes: bytes, tipo_imagen: str, cultivo: str, municipio: str) -> dict:
    load_dotenv()
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    imagen_b64 = base64.standard_b64encode(imagen_bytes).decode("utf-8")
    
    prompt = f"""Eres un experto agronomo especializado en cultivos de Chiapas, Mexico.

Analiza esta imagen de un cultivo de {cultivo} del municipio de {municipio}, Chiapas.

Responde SOLO con un JSON valido con esta estructura exacta, sin texto adicional, sin markdown, sin backticks:
{{
    "estado": "saludable" o "enfermo" o "deficiente",
    "problema": "nombre del problema detectado o null si esta saludable",
    "severidad": "bajo" o "medio" o "alto" o null,
    "descripcion": "descripcion breve en espanol de lo que observas",
    "tratamiento_organico": "tratamiento organico recomendado",
    "tratamiento_convencional": "tratamiento convencional recomendado",
    "prevencion": "medidas preventivas para evitar el problema"
}}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": tipo_imagen,
                            "data": imagen_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    
    texto = message.content[0].text.strip()
    
    # Limpiar si viene con markdown
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]
        texto = texto.strip()
    
    return json.loads(texto)