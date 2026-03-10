from fastapi import FastAPI, status, HTTPException, Depends
from typing import Literal, Optional
import asyncio
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

app= FastAPI(title= 'Reservas de hospedaje',
             description= "Fernanda Daniela Perez",
             version= '1.0.0')
#BD Ficticia
huespedes = []


#MODELOS listar reservas que la fecha de entrada no sea menor a la actual, y la fecha de salida mayor fecha de entrada
class huesped (BaseModel):
    nombre: str = Field(..., min_length=5 , max_length=50)
    fecha_entrada: str =Field
    fecha_salida: str =Field
    tipo_habitacion: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    correo: str = Field(..., pattern=r'^\S+@\S+\.\S+$')

#BD Ficticia
usuarios=[{"id":1, "nombre":"Fernanda", "edad":20},
    {"id":2, "nombre":"Yesenia", "edad":23},
    {"id":3, "nombre":"Julian", "edad":20}
]

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El libro ya existe")
    libros.append(libro.dict())
    return {"mensaje": "Libro registrado", "libro": libro}

seguridad= HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials=Depends(seguridad)):
    #el primero es el usuario que se ingresa y el segundo es el usuario que se espera con las credenciales aunque no es una buena practica
    userAuth= secrets.compare_digest(credenciales.username, "hotel")
    passwordAuth= secrets.compare_digest(credenciales.password, "r2026")
    if not (userAuth and passwordAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    #regrsa el usuario con sus credenciales
    return credenciales.username


@app.get("/reservas", status_code=status.HTTP_200_OK)
def listar_reservas( fecha_entrada: str, fecha_salida: str):
    return reservas



@app.get("/v1/listar_reservas", tags=['Reservas'])
async def listar_reservas():
    await asyncio.sleep(2)
    if fecha_entrada < fecha_actual:
        return { "mensaje":"la fecha de entrada no puede ser menor a la actual"}
    if fecha_salida <= fecha_entrada:
        return { "mensaje":"la fecha de salida debe ser mayor a la fecha de entrada"}
    else:       
        return { "mensaje":"Reservas listadas correctamente"}
    

#tipo de habitacion: sencilla, doble, o suite que puede elegir el huesped
@app.get("/v1/tipos_habitacion", tags=['Habitaciones']) 
async def tipo_habitacion (str
    for huesped in usuarios:
        if huesped["id"] == id:
            return huesped
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


#consultar por id
@app.get("/v1/huespedes/{id}", tags=['CRUD HTTP'])
async def consultar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return usr
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


#cancelar reservas
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, userAuth:str=Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index) #elimina el usuario de la lista
            return { 
                "mensaje": f"Usuario eliminado por {userAuth}"}
    raise HTTPException(
        status_code=400, 
        detail="El id ya existe")