from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.models.usuario import Usuario

SECRET_KEY = "agroia-chiapas-secret-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano, password_hash)

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def crear_token(data: dict) -> str:
    datos = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expira})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def registrar_usuario(db: Session, nombre: str, telefono: str, municipio: str, password: str, email: str = None):
    password_hash = hashear_password(password)
    usuario = Usuario(
        nombre=nombre,
        telefono=telefono,
        municipio=municipio,
        email=email,
        password_hash=password_hash
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def login_usuario(db: Session, telefono: str, password: str):
    usuario = db.query(Usuario).filter(Usuario.telefono == telefono).first()
    if not usuario:
        return None
    if not verificar_password(password, usuario.password_hash):
        return None
    token = crear_token({"sub": str(usuario.id), "telefono": usuario.telefono})
    return {"token": token, "usuario": usuario}
