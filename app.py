from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'


def compress_image(input_path, output_path, quality=60):
    try:
        original_size = os.path.getsize(input_path) / 1024.0  # Taille en kilo-octets (KB)

        img = Image.open(input_path)
        img.save(output_path, "JPEG", quality=quality)

        compressed_size = os.path.getsize(output_path) / 1024.0  # Taille en kilo-octets (KB)
        compression_ratio = (original_size - compressed_size) / original_size * 100

        return compression_ratio

    except Exception as e:
        print(f"Erreur lors de la compression de l'image : {e}")
        return None
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Enregistrer l'image originale
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(original_path)

        # Chemin pour l'image compressée
        compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + file.filename)

        # Compression de l'image et récupération du taux de compression
        compression_ratio = compress_image(original_path, compressed_path)

        return render_template('image.html', original_image=file.filename,
                               compressed_image='compressed_' + file.filename,
                               compression_ratio=compression_ratio)
if __name__ == '__main__':
    app.run(debug=True)
