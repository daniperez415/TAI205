from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU=APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/") 
async def consulta():
    return { 
        "status":"200", 
        "total":len(usuarios), 
        "data":usuarios 
    } 


routerU.post("/", status_code=status.HTTP_201_CREATED)
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


routerU.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuario: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario["id"]:
            return { "mensaje":"Usuario actualizado correctamente", "status": "200", "usuario": usuario}
        usuarios[index] = usuario

    raise HTTPException(
        status_code=400, 
        detail="el usuario no se encontró")
  
    
#eliminar
routerU.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, userAuth:str=Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index) #elimina el usuario de la lista
            return { 
                "mensaje": f"Usuario eliminado por {userAuth}"}
    raise HTTPException(
        status_code=400, 
        detail="El id ya existe")
  