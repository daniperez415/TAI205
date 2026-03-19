from fastapi import status, HTTPException, Depends, APIRouter
from typing import Optional
import asyncio
from app.data.database import usuarios

routerV= APIRouter (tags=['Inicio'])

#3.Endpoints

@routerV.get("/") #endpoint GET de inicio o arranque
async def holaMundo():
    return { "mensaje":"Hola Mundo FASTAPI" } #objeto JSON izquierdo es una llave y el lado derecho es el valor


@routerV.get("/v1/bienvenidos") 
async def bien():
    return { "mensaje":"Bienvenidos" } 
#al guardar el archivo debio de detectar la reecarga y se debe cambiar el endpoint

@routerV.get("/v1/promedio") 
async def promedio(): #permite el codigo asincrono
    await asyncio.sleep(3) #Tiempo de espera para una peticion a otra API, 
    #o una consulta a la base de datos
    return { "Calificacion":"7.5",
            "estatus":"200" } 

@routerV.get("/v1/parametro0/{id}") 
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return { "Resultado":"usuario encontrado", "Estatus":"200",  } 


@routerV.get("/v1/opcionalP/")
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==id:
                return { "Usuario encontrado": id, "Datos": usuario }
        return { "Error":"Usuario no encontrado"}
    else:
        return { "Aviso": "No se proporciono ID"}

