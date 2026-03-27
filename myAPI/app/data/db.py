from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1- Definir la URL de conexion con el contenedor
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2- Crear motor de conexion
engine= create_engine(DATABASE_URL)

#3- Definimos el manejador de sesiones
SessionLocal=sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine

)

#4- Instaciamos la base declarativa del modelo
Base =declarative_base()

#5- Funcion para manejo de sesiones por peticion
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()