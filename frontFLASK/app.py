from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000/v1/usuarios"

#pagina principal
@app.route("/")
def index():
    response = requests.get(API_URL)
    data = response.json()
    usuarios = data.get("data", [])
    return render_template("index.html", usuarios=data["data"])

#crear usuarios
@app.route("/agregar", methods=["POST"])
def agregar_usuario():
    id = request.form["id"]
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    return redirect("/")

#elimina
def eliminar_usuario():
    id = request.form["id"]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5010)