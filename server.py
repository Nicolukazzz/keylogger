from flask import Flask, request, send_from_directory, render_template
import os

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
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Extraer el nombre del PC del nombre del archivo
    hostname = file.filename.split('_')[0]
    
    # Crear una carpeta para el PC si no existe
    hostname_folder = os.path.join(UPLOAD_FOLDER, hostname)
    os.makedirs(hostname_folder, exist_ok=True)

    # Guardar el archivo en la carpeta correspondiente (se sobrescribe si ya existe)
    file_path = os.path.join(hostname_folder, file.filename)
    file.save(file_path)

    return "File uploaded successfully", 200

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

@app.route('/files/<pc>/<filename>', methods=['GET'])
def get_file(pc, filename):
    try:
        # Descargar el archivo desde la carpeta del PC correspondiente
        return send_from_directory(os.path.join(UPLOAD_FOLDER, pc), filename)
    except FileNotFoundError:
        return "File not found", 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))