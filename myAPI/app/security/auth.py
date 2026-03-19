from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
#contraseñas seguras
import secrets


#Seguridad HTTP BASIC
seguridad= HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials=Depends(seguridad)):
    #el primero es el usuario que se ingresa y el segundo es el usuario que se espera con las credenciales aunque no es una buena practica
    userAuth= secrets.compare_digest(credenciales.username, "fernanda")
    passwordAuth= secrets.compare_digest(credenciales.password, "123456")
    if not (userAuth and passwordAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas"
        )
    #si no regrresa al usuario con sus credenciales correctas
    return credenciales.username
