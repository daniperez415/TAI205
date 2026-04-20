from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

print(datetime.now().date().day)

app = FastAPI()

reservas = []
tipo_habitacion_lista = ["sencilla", "suite", "doble"]

class Reserva(BaseModel):
    id: int
    nombre_huesped: str = Field(..., min_length=5)
    fecha_entrada: datetime
    fecha_salida: datetime
    tipo_habitacion: str
    confirmado: bool = False
    estancia: int = Field(None, description="Duración de la estancia")

    @field_validator('tipo_habitacion')
    @classmethod
    def validar_tipo_habitacion(cls, v):
        if v not in tipo_habitacion_lista:
            raise ValueError(f'Tipo de habitación debe ser uno de: {tipo_habitacion_lista}')
        return v

seguridad = HTTPBasic()

def verificar_usuario(credentials: HTTPBasicCredentials = Depends(seguridad)):
    usuario_valido = secrets.compare_digest(credentials.username, "hotel")
    contrasena_valida = secrets.compare_digest(credentials.password, "r2026")
    if not (usuario_valido and contrasena_valida):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    return credentials.username

# endpoints

# CREAR RESERVA
@app.post("/reservas", status_code=status.HTTP_201_CREATED)
def crear_reserva(reserva: Reserva, user: str = Depends(verificar_usuario)): # <-- Agregado el Depends

    if reserva.fecha_entrada.date() < datetime.now().date():
        raise HTTPException(status_code=400, detail="La fecha de entrada no puede ser menor a la actual.")

    if reserva.fecha_salida <= reserva.fecha_entrada:
        raise HTTPException(status_code=400, detail="La fecha de salida debe ser mayor a la entrada.")

    estancia = (reserva.fecha_salida - reserva.fecha_entrada).days

    # Validacion
    if estancia > 7:
        raise HTTPException(status_code=400, detail="La estancia no puede ser mayor a 7 días.")

    reserva.estancia = estancia
    reservas.append(reserva)
    return reserva

# listar
@app.get("/reservas")
def listar_reservas():
    return reservas

# consultar id
@app.get("/reservas/{reserva_id}")
def consultar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva.id == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

# conf reserva
@app.post("/reservas/{reserva_id}/confirmar")
def confirmar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva.id == reserva_id:
            reserva.confirmado = True
            return {"message": "Reserva confirmada"}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

# delete
@app.delete("/reservas/{reserva_id}")
def eliminar_reserva(reserva_id: int, credentials: str = Depends(verificar_usuario)):
    for i, reserva in enumerate(reservas):
        if reserva.id == reserva_id:
            del reservas[i]
            return {"message": "Reserva eliminada"}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")