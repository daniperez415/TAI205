from fastapi import FastAPI, status, HTTPException, Body
from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(title="Biblioteca digital", 
              version="1.0.0")

#BD Ficticia
libros = []
prestamos = []

#MODELOS
class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año_libro: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    correo: str = Field(..., pattern=r'^\S+@\S+\.\S+$')

#registrar un libro
@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El libro ya existe")
    libros.append(libro.dict())
    return {"mensaje": "Libro registrado", "libro": libro}

#listar todos los libros disponibles
@app.get("/libros", status_code=status.HTTP_200_OK)
def listar_libros():
    return libros

# buscar un libro por su nombre
@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Libro no encontrado")

# registrar el préstamo de un libro a un usuario
@app.post("/prestamos")
def registrar_prestamo(usuario: Usuario = Body(...), nombre_libro: str = Body(...) ):
    for libro in libros:
        if libro["nombre"].lower() == nombre_libro.lower():
            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="el libro ya esta prestado")
            libro["estado"] = "prestado"
            prestamos.append({"usuario": usuario.dict(), "libro": nombre_libro})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="el nombre el libro no es valido")

# marcar un libro como devuelto
@app.put("/prestamos/{nombre_libro}", status_code=status.HTTP_200_OK)
def devolver_libro(nombre_libro: str):
    for libro in libros:
        if libro["nombre"].lower() == nombre_libro.lower():
            if libro["estado"] == "prestado":
                libro["estado"] = "disponible"
                return {"mensaje": "Libro devuelto"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El registro de préstamo ya no existe"
                )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Libro no encontrado")

# Eliminar el registro de un préstamo@app.delete("/prestamos/{nombre_libro}", status_code=status.HTTP_200_OK)
def eliminar_prestamo(nombre_libro: str):
    for libro in libros:
        if libro["nombre"].lower() == nombre_libro.lower():
            if libro["estado"] == "prestado":
                libro["estado"] = "disponible"
                prestamos[:] = [p for p in prestamos if p["libro"].lower() != nombre_libro.lower()]
                return {"mensaje": "Préstamo eliminado"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El registro de préstamo ya no existe")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Libro no encontrado")
