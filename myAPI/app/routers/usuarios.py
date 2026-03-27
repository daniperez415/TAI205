from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

routerU=APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/") 
async def leer_usuario(db:Session= Depends(get_db)):

    queryUsuarios= db.query(usuarioDB).all()

    return { 
        "status":"200", 
        "total":len(queryUsuarios), 
        "usuarios":queryUsuarios 
    } 


@routerU.post("/", status_code=status.HTTP_201_CREATED)
#usamos el modelo
async def crear_usuario(usuarioP:crear_usuario, db:Session= Depends(get_db)):

    usuarioNuevo= usuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad)

    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)

    return{
        "mensaje":"usuario agregado",
        "usuario":usuarioP
    }


@routerU.put("/{id}")
async def actualizar_usuario(id: int, usuario: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario["id"]:
            return { "mensaje":"Usuario actualizado correctamente", "status": "200", "usuario": usuario}
        usuarios[index] = usuario

    raise HTTPException(
        status_code=400, 
        detail="el usuario no se encontró")
  
    
#eliminar
@routerU.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, userAuth:str=Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index) #elimina el usuario de la lista
            return { 
                "mensaje": f"Usuario eliminado por {userAuth}"}
    raise HTTPException(
        status_code=400, 
        detail="El id ya existe")
  