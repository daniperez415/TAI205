import secrets

from fastapi import FastAPI, status, HTTPException, Depends
from typing import Literal, Optional
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

app= FastAPI(title= 'Reservas de hospedaje',
             description= "Fernanda Daniela Perez")


#MODELOS 
class huesped (BaseModel):
    huesped : str = Field(..., min_length=5 , max_length=50)
    fecha_entrada: str =Field (..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    fecha_salida: str =Field (..., pattern=r'^\d{4}-\d{2}-\d{2}$') 
    tipo_habitacion: Literal["disponible", "prestado"] = "disponible"
    estancia: str = Field(..., min_length=1, max_length=7)

#BD Ficticia
reservas = [{"id":1, "nombre":"Fernanda", "edad":20},
    {"id":2, "nombre":"Yesenia", "edad":23},
    {"id":3, "nombre":"Julian", "edad":20}
]

seguridad= HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials=Depends(seguridad)):
    #el primero es el huesped se ingresa y el segundo  las credenciales aunque no es una buena practica
    userAuth= secrets.compare_digest(credenciales.username, "hotel")
    passwordAuth= secrets.compare_digest(credenciales.password, "r2026")
    if not (userAuth and passwordAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    #regrsa el huesped con sus credenciales
    return credenciales.username


#crear reserva
@app.get("/crear_reserva", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def crear_reserva(id: int, userAuth:str=Depends(verificar_peticion)):
    for index, reserva in enumerate(reservas):
        if reserva["id"] == id:
            raise HTTPException(status_code=400, detail="la reserva no se encontró")
        return { "mensaje": f"Reserva creada por {userAuth}"}
    raise HTTPException(
        status_code=400, 
        detail="el huesped no se encontró")

#listar reservas que la fecha de entrada no sea menor a la actual, y la fecha de salida mayor fecha de entrada
@app.post("/reservas", status_code=status.HTTP_201_CREATED)
def registrar_reserva(reserva: Reserva):
    for r in reservas:
        if r["nombre"].lower() == reserva.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="La reserva ya existe")
    reservas.append(reserva.dict())
    return {"mensaje": "Reserva registrada", "reserva": reserva}

@app.get("/v1/listar_reservas", tags=['Reservas'])
async def listar_reservas():
    await asyncio.sleep(2)
    if fecha_entrada < fecha_actual:return { "mensaje":"la fecha de entrada no puede ser menor a la actual"}
    if fecha_salida <= fecha_entrada: return { "mensaje":"la fecha de salida debe ser mayor a la fecha de entrada"}
    else:       
        return { "mensaje":"Reservas listadas correctamente"}

#consultar por id
@app.get("/v1/reservas/{id}", tags=['CRUD HTTP'])
async def consultar_reserva(id: int):
    for r in reservas:
        if r["id"] == id:
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

#confirmar reserva
@app.put("/v1/confirmar_reserva/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def confirmar_reserva(id: int):
    for index, r in enumerate(reservas):
        if r["id"] == id:    
            reservas[index]["estado"] = "confirmada"
    return {"mensaje": f"Reserva confirmada"}


#Cancelar reservas
@app.delete("/v1/cancelar_reserva/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def cancelar_reserva(id: int, userAuth:str=Depends(verificar_peticion)):
    for index, r in enumerate(reservas):
        if r["id"] == id:
            reservas.pop(index)
            return {
                "mensaje": f"Reserva cancelada por {userAuth}"}
    raise HTTPException(
        status_code=400, 
        detail="El id no existe")



 