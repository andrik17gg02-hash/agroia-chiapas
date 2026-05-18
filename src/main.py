from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.usuarios import router as usuarios_router
from src.api.diagnostico import router as diagnostico_router
from src.api.auth import router as auth_router
from src.api.negocio import router as negocio_router
from src.api.protegido import router as protegido_router
from src.api.marketplace import router as marketplace_router
from src.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgroIA Chiapas",
    description="Plataforma agricola inteligente para productores de Chiapas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://agroia-chiapas.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
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
