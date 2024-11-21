from flask import Flask, request
import os
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    file.save(f"./uploaded_{file.filename}")  # Guarda el archivo en el servidor
    return "File uploaded successfully", 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto asignado por Railway
    app.run(host='0.0.0.0', port=port)
