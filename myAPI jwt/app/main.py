
#1. Importaciones, crea el servidor api, codigos http definidos, errores controlados, dependencias
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

SECRET_KEY = "llave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#2.Inicialización API crea
app= FastAPI(title= 'Mi primer API',
             description= "Fernanda Daniela Perez",
             version= '1.0.0')

#BD Ficticia
usuarios=[
    {"id":1, "nombre":"Fernanda", "edad": 20},
    {"id":2, "nombre":"Yesenia", "edad": 23},
    {"id":3, "nombre":"Julian", "edad": 20}

]

#Modelo de validacion pydantic
class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str = Field(..., min_length=3,max_length=50,example="Juanita")
    edad:int = Field(..., ge=1,le=123,description="Edad valida entre 1 y 123")

#token
def crear_token(data: dict, expires_delta: timedelta=None):
    to_encode =data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="token invalido")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="token invalido")


#Seguridad HTTP BASIC
#seguridad= HTTPBasic()
#def verificar_peticion(credenciales: HTTPBasicCredentials=Depends(seguridad)):
    #el primero es el usuario que se ingresa y el segundo es el usuario que se espera con las credenciales aunque no es una buena practica
    #userAuth= secrets.compare_digest(credenciales.username, "fernanda")
    #passwordAuth= secrets.compare_digest(credenciales.password, "123456")
    #if not (userAuth and passwordAuth):
    #    raise HTTPException(
    #       status_code=status.HTTP_401_UNAUTHORIZED,
    #       detail="Credenciales no Autorizadas")
    #si no regrresa al usuario con sus credenciales correctas
    #return credenciales.username



#3.Endpoints

@app.get("/", tags=['Inicio']) #endpoint GET de inicio o arranque
async def holaMundo():
    return { "mensaje":"Hola Mundo FASTAPI" } #objeto JSON izquierdo es una llave y el lado derecho es el valor

#crea entorno y se abre la terminal y primero se verifica donde estamos
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


#post
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
        if form_data.username != "fernanda" or form_data.password != "123456":
            raise HTTPException(
                status_code=401,
                detail="Credenciales incorrectas"
            )
        access_token =crear_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}


@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario_endpoint(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    usuarios.append(usuario.dict())
    return {"mensaje": "Usuario agregado", "usuario": usuario}


@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario: dict, user:str= Depends(validar_token)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index] = usuario
            return { "mensaje":f"Usuario actualizado por {user}", "status": "200", "usuario": usuario}
        
    raise HTTPException(
        status_code=400, 
        detail="el usuario no se encontró")
  
    
#eliminar
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, user:str=Depends(validar_token)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index) #elimina el usuario de la lista
            return { 
                "mensaje": f"Usuario eliminado por {user}"}
    raise HTTPException(
        status_code=400, 
        detail="El usuario no se encontró")