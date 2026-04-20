from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import date, datetime
import uuid

app = Flask(__name__)
auth = HTTPBasicAuth()

USERS = {"hotel": "r2026"}

@auth.verify_password
def verify_password(username, password):
    return USERS.get(username) == password

reservas = {}

def validar_reserva(data):
    errors = []

    huesped = data.get("huesped", "")
    if len(huesped) < 5:
        errors.append("El nombre del huésped debe tener mínimo 5 caracteres.")

    try:
        fecha_entrada = date.fromisoformat(data.get("fecha_entrada", ""))
    except ValueError:
        errors.append("Fecha de entrada inválida. Formato: YYYY-MM-DD.")
        fecha_entrada = None

    try:
        fecha_salida = date.fromisoformat(data.get("fecha_salida", ""))
    except ValueError:
        errors.append("Fecha de salida inválida. Formato: YYYY-MM-DD.")
        fecha_salida = None

    hoy = date.today()

    if fecha_entrada and fecha_entrada < hoy:
        errors.append("La fecha de entrada no puede ser menor a la fecha actual.")

    if fecha_entrada and fecha_salida:
        if fecha_salida <= fecha_entrada:
            errors.append("La fecha de salida debe ser mayor que la fecha de entrada.")
        else:
            dias = (fecha_salida - fecha_entrada).days
            if dias > 7:
                errors.append("La estancia no puede ser mayor a 7 días.")

    tipo = data.get("tipo_habitacion", "")
    if tipo not in ["sencilla", "doble", "suite"]:
        errors.append("El tipo de habitación debe ser: sencilla, doble o suite.")

    return errors


# Crear reserva (PROTEGIDO)
@app.route("/reservas", methods=["POST"])
@auth.login_required
def crear_reserva():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Body JSON requerido."}), 400

    errors = validar_reserva(data)
    if errors:
        return jsonify({"errores": errors}), 422

    reserva_id = str(uuid.uuid4())[:8].upper()
    reserva = {
        "id": reserva_id,
        "huesped": data["huesped"],
        "fecha_entrada": data["fecha_entrada"],
        "fecha_salida": data["fecha_salida"],
        "tipo_habitacion": data["tipo_habitacion"],
        "estado": "pendiente",
        "creada_en": datetime.now().isoformat()
    }
    reservas[reserva_id] = reserva
    return jsonify({"mensaje": "Reserva creada exitosamente.", "reserva": reserva}), 201


# Listar reservas
@app.route("/reservas", methods=["GET"])
def listar_reservas():
    return jsonify({"total": len(reservas), "reservas": list(reservas.values())}), 200


# Consultar por ID
@app.route("/reservas/<id>", methods=["GET"])
def consultar_reserva(id):
    reserva = reservas.get(id.upper())
    if not reserva:
        return jsonify({"error": f"Reserva '{id}' no encontrada."}), 404
    return jsonify(reserva), 200


# Confirmar reserva
@app.route("/reservas/<id>/confirmar", methods=["PATCH"])
def confirmar_reserva(id):
    reserva = reservas.get(id.upper())
    if not reserva:
        return jsonify({"error": f"Reserva '{id}' no encontrada."}), 404
    if reserva["estado"] == "cancelada":
        return jsonify({"error": "No se puede confirmar una reserva cancelada."}), 400
    reserva["estado"] = "confirmada"
    return jsonify({"mensaje": "Reserva confirmada.", "reserva": reserva}), 200


# Cancelar reserva (PROTEGIDO)
@app.route("/reservas/<id>", methods=["DELETE"])
@auth.login_required
def cancelar_reserva(id):
    reserva = reservas.get(id.upper())
    if not reserva:
        return jsonify({"error": f"Reserva '{id}' no encontrada."}), 404
    reserva["estado"] = "cancelada"
    return jsonify({"mensaje": "Reserva cancelada.", "reserva": reserva}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
