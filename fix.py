content = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.usuarios import router as usuarios_router
from src.api.diagnostico import router as diagnostico_router
from src.api.auth import router as auth_router
from src.api.negocio import router as negocio_router
from src.api.protegido import router as protegido_router
from src.api.marketplace import router as marketplace_router

app = FastAPI(
    title="AgroIA Chiapas",
    description="Plataforma agricola inteligente para productores de Chiapas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router, prefix="/api")
app.include_router(diagnostico_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(negocio_router, prefix="/api")
app.include_router(protegido_router, prefix="/api")
app.include_router(marketplace_router, prefix="/api")
'''

open('src/main.py', 'w', encoding='utf-8').write(content)
print('Listo')