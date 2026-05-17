import base64
import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def diagnosticar_planta(imagen_bytes: bytes, tipo_imagen: str, cultivo: str, municipio: str) -> dict:
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    prompt = f"""Eres un experto agronomo especializado en cultivos de Chiapas, Mexico.
    
Analiza esta imagen de un cultivo de {cultivo} del municipio de {municipio}, Chiapas.

Responde SOLO con un JSON con esta estructura exacta:
{{
    "estado": "saludable" o "enfermo" o "deficiente",
    "problema": "nombre del problema detectado o null si esta saludable",
    "severidad": "bajo" o "medio" o "alto" o null,
    "descripcion": "descripcion breve en espanol",
    "tratamiento_organico": "tratamiento organico recomendado",
    "tratamiento_convencional": "tratamiento convencional recomendado",
    "prevencion": "medidas preventivas"
}}"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            types.Part.from_bytes(data=imagen_bytes, mime_type=tipo_imagen),
            prompt
        ]
    )
    
    texto = response.text.strip()
    if texto.startswith("```"):
        texto = texto.split("```")[1]
        if texto.startswith("json"):
            texto = texto[4:]
    
    return json.loads(texto.strip())
