"""
Script para agregar productos de prueba al marketplace de AgroIA.
Ejecutar con el backend corriendo y el venv activado:

cd C:\\Users\\BECAS\\Desktop\\agroia-chiapas
venv\\Scripts\\activate
python agregar_productos.py
"""

import requests

# 1. Login para obtener token
login = requests.post(
    "http://127.0.0.1:8000/api/auth/login",
    json={"telefono": "9991234567", "password": "password123"}
)

if login.status_code != 200:
    print("Error en login:", login.text)
    exit()

token = login.json()["token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print("Login exitoso. Token obtenido.")

# 2. Productos a agregar
productos = [
    {
        "nombre": "Cafe Arabica Organico",
        "descripcion": "Cafe de altura cosecha 2026, certificado organico de los Altos de Chiapas",
        "precio": 180.0,
        "unidad": "kg",
        "municipio": "San Cristobal",
        "cultivo": "cafe",
        "disponible": 500.0,
    },
    {
        "nombre": "Cacao Fino de Aroma",
        "descripcion": "Cacao premium variedad criollo, cosecha artesanal de Tapachula",
        "precio": 220.0,
        "unidad": "kg",
        "municipio": "Tapachula",
        "cultivo": "cacao",
        "disponible": 300.0,
    },
    {
        "nombre": "Maiz Criollo Nativo",
        "descripcion": "Maiz nativo de los Altos, sin agroquimicos, ideal para tortillas",
        "precio": 8.0,
        "unidad": "kg",
        "municipio": "Comitan",
        "cultivo": "maiz",
        "disponible": 2000.0,
    },
    {
        "nombre": "Miel de Abeja Melipona",
        "descripcion": "Miel pura de abeja nativa melipona, sin procesar, region Palenque",
        "precio": 95.0,
        "unidad": "litro",
        "municipio": "Palenque",
        "cultivo": "miel",
        "disponible": 80.0,
    },
    {
        "nombre": "Frijol Negro Chiapaneco",
        "descripcion": "Frijol negro de temporal, cosecha 2025-2026, limpio y seleccionado",
        "precio": 25.0,
        "unidad": "kg",
        "municipio": "Comitan",
        "cultivo": "frijol",
        "disponible": 1500.0,
    },
]

# 3. Publicar cada producto
for p in productos:
    res = requests.post("http://127.0.0.1:8000/api/marketplace", json=p, headers=headers)
    if res.status_code in (200, 201):
        print(f"Publicado: {p['nombre']}")
    else:
        print(f"Error en {p['nombre']}: {res.text}")

print("\nListo. Abre http://localhost:3000/marketplace para ver los productos.")
