#1. Importaciones 
from fastapi import FastAPI

#2.Inicialización API
app= FastAPI()

#3.Endpoints

@app.get("/") #endpoint GET de inicio o arranque
async def holaMundo():
    return { "mensaje":"Hola Mundo FASTAPI" } #objeto JSON izquierdo es una llave y el lado derecho es el valor

#se abre la terminal y primero se verifica donde estamos 
#cd miAPI
#COMANDO PARA EJECUTAR EL SERVIDOR
#uvicorn main:app --reload

@app.get("/bienvenidos") #endpoint GET de inicio o arranque
async def bien():
    return { "mensaje":"Bienvenidos" } 

#al guardar el archivo debio de detectar la reecarga y se debe cambiar el endpoint

