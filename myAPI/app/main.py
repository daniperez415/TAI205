#1. Importaciones, crea el servidor api, codigos http definidos, errores controlados, dependencias
from fastapi import FastAPI
from app.routers import usuarios, varios
#parametros opcionales, codigo asincrono, seguridad HTTP BASIC autenticacion

#2.Inicialización API crea
app= FastAPI(
    title= 'Mi primer API',
    description= "Fernanda Daniela Perez",
    version= '1.0.0'
)

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
