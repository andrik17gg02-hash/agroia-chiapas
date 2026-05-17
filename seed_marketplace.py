"""
AgroIA Chiapas — Seed Marketplace
Ejecutar con: python seed_marketplace.py
Requiere: pip install requests (ya incluido en el venv)

INSTRUCCIONES:
1. Primero haz login en http://127.0.0.1:8000/docs con juan@agroia.com / password123
2. Copia el token que retorna el endpoint /api/auth/login
3. Pegalo en la variable TOKEN abajo
4. Ejecuta: python seed_marketplace.py
"""

import requests

# --- PEGA TU TOKEN AQUI ---
TOKEN = "PEGAR_TOKEN_AQUI"
# --------------------------

BASE_URL = "http://127.0.0.1:8000"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

productos = [
    {
        "nombre": "Cafe Arabica Organico",
        "descripcion": "Cafe de altura cosecha 2026, certificado organico, municipio San Cristobal de las Casas",
        "precio": 180.0,
        "unidad": "kg",
        "municipio": "San Cristobal",
        "cultivo": "cafe",
        "disponible": 500.0
    },
    {
        "nombre": "Cacao Fino de Aroma",
        "descripcion": "Cacao premium de Tapachula, variedad criollo, apto para exportacion",
        "precio": 220.0,
        "unidad": "kg",
        "municipio": "Tapachula",
        "cultivo": "cacao",
        "disponible": 300.0
    },
    {
        "nombre": "Maiz Criollo de los Altos",
        "descripcion": "Maiz nativo de los Altos de Chiapas, sin transgenicos, cosecha reciente",
        "precio": 8.0,
        "unidad": "kg",
        "municipio": "Comitan",
        "cultivo": "maiz",
        "disponible": 2000.0
    },
    {
        "nombre": "Miel de Abeja Melipona",
        "descripcion": "Miel pura de abeja sin aguijon, produccion artesanal de Palenque",
        "precio": 350.0,
        "unidad": "litro",
        "municipio": "Palenque",
        "cultivo": "miel",
        "disponible": 80.0
    },
    {
        "nombre": "Chile de Agua Seco",
        "descripcion": "Chile tradicional de Chiapas, deshidratado, ideal para exportacion gourmet",
        "precio": 95.0,
        "unidad": "kg",
        "municipio": "Tuxtla Gutierrez",
        "cultivo": "chile",
        "disponible": 150.0
    },
]

def main():
    if TOKEN == "PEGAR_TOKEN_AQUI":
        print("ERROR: Primero pega tu token en la variable TOKEN")
        print("Obtenlo en: http://127.0.0.1:8000/docs -> /api/auth/login")
        return

    print(f"Conectando a {BASE_URL}...")
    print("-" * 50)

    exitosos = 0
    for producto in productos:
        try:
            res = requests.post(
                f"{BASE_URL}/api/marketplace",
                json=producto,
                headers=HEADERS,
                timeout=10
            )
            if res.status_code in (200, 201):
                data = res.json()
                print(f"OK  {producto['nombre']} — ID: {data.get('id', 'N/A')}")
                exitosos += 1
            else:
                print(f"ERR {producto['nombre']} — Status {res.status_code}: {res.text}")
        except requests.exceptions.ConnectionError:
            print("ERROR: No se puede conectar al backend. Verifica que este corriendo en :8000")
            break
        except Exception as e:
            print(f"ERR {producto['nombre']} — {e}")

    print("-" * 50)
    print(f"Resultado: {exitosos}/{len(productos)} productos insertados")

if __name__ == "__main__":
    main()