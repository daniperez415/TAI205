
#1. Importaciones 
from fastapi import FastAPI, status, HTTPException
from typing import Optional
import asyncio
#agregamos BaseModel pydantic
from pydantic import BaseModel, Field

#2.Inicialización APP
app= FastAPI(title= 'Mi primer API',
             description= "Fernanda Daniela Perez",
             version= '1.0.0')

#BD Ficticia
usuarios=[
    {"id":"1", "nombre":"Fernanda", "edad":"20"},
    {"id":"2", "nombre":"Yesenia", "edad":"23"},
    {"id":"3", "nombre":"Julian", "edad":"20"}
]

#Modelo de validacion pydantic
class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str = Field(..., min_length=3,max_length=50,example="Juanita")
    edad:int = Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")


#3.Endpoints

@app.get("/", tags=['Inicio']) #endpoint GET de inicio o arranque
async def holaMundo():
    return { "mensaje":"Hola Mundo FASTAPI" } #objeto JSON izquierdo es una llave y el lado derecho es el valor

#se abre la terminal y primero se verifica donde estamos 
#cd miAPI
#COMANDO PARA EJECUTAR EL SERVIDOR
#uvicorn main:app --reload

@app.get("/v1/bienvenidos", tags=['Inicio']) 
async def bien():
    return { "mensaje":"Bienvenidos" } 
#al guardar el archivo debio de detectar la reecarga y se debe cambiar el endpoint

@app.get("/v1/promedio", tags=['Calificaciones']) 
async def promedio(): #permite el codigo asincrono
    await asyncio.sleep(3) #Tiempo de espera para una peticion a otra API, 
    #o una consulta a la base de datos
    return { "Calificacion":"7.5",
            "estatus":"200" } 

@app.get("/v1/parametro0/{id}", tags=['Parametros Obligatorio']) 
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return { "Resultado":"usuario encontrado", "Estatus":"200",  } 

@app.get("/v1/opcionalP/", tags=['Parametros Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return { "Usuario encontrado": id, "Datos": usuario }
        return { "Error":"Usuario no encontrado"}
    else:
        return { "Aviso": "No se proporciono ID"}


@app.get("/v1/usuarios", tags=['CRUD HTTP']) 
async def consulta():
    return { "status":"200", "total":len(usuarios), "data":usuarios } 



@app.post("/v1/usuarios/", tags=['CRUD_HTTP'], status_code=status.HTTP_201_CREATED)
#usamos el modelo
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado",
        "usuario":usuario
    }


@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario["id"]:
            raise HTTPException(status_code=400, detail="el usuario no se encontró")
    usuarios[index] = usuario
    return { "mensaje":"Usuario actualizado correctamente", "status": "200", "usuario": usuario}

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuario_eliminado = usuarios.pop(index) #elimina el usuario de la lista
    return { "mensaje":"Usuario eliminado correctamente", "status": "200", "usuario": usuario_eliminado}