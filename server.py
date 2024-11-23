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

    original_filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, original_filename)

    if os.path.exists(file_path):
        base, extension = os.path.splitext(original_filename)
        counter = 1
        new_filename = f"{base}_{counter}{extension}"
        new_file_path = os.path.join(UPLOAD_FOLDER, new_filename)

        while os.path.exists(new_file_path):
            counter += 1
            new_filename = f"{base}_{counter}{extension}"
            new_file_path = os.path.join(UPLOAD_FOLDER, new_filename)

        file_path = new_file_path

    file.save(file_path)
    return "File uploaded successfully", 200

@app.route('/files')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('files.html', files=files)

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return "File not found", 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))