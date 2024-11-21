from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello from Flask!'



UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la carpeta si no existe

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file.save(os.path.join(UPLOAD_FOLDER, f"uploaded_{file.filename}"))
    return "File uploaded successfully", 200

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
