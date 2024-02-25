from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'


def compress_image(input_path, output_path, quality=60):
    try:
        original_size = os.path.getsize(input_path) / 1024.0  # Size in kilobytes (KB)

        img = Image.open(input_path)
        img.save(output_path, "JPEG", quality=quality)

        compressed_size = os.path.getsize(output_path) / 1024.0  # Size in kilobytes (KB)
        compression_ratio = (original_size - compressed_size) / original_size * 100

        return compression_ratio

    except Exception as e:
        print(f"Error compressing image: {e}")
        return None


def compress_audio(input_path, output_path, bitrate="64k"):
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="mp3", bitrate=bitrate)
        return True

    except Exception as e:
        print(f"Error compressing audio: {e}")
        return False


def compress_video(input_path, output_path, bitrate="1000k"):
    try:
        video = VideoFileClip(input_path)
        video.write_videofile(output_path, codec="libx264", bitrate=bitrate)
        return True

    except Exception as e:
        print(f"Error compressing video: {e}")
        return False


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
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(original_path)

        compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed_' + file.filename)

        if file.filename.endswith(('.jpg', '.jpeg', '.png')):
            compression_ratio = compress_image(original_path, compressed_path)
        elif file.filename.endswith(('.mp3', '.wav')):
            success = compress_audio(original_path, compressed_path)
        elif file.filename.endswith(('.mp4', '.webm', '.ogg')):
            success = compress_video(original_path, compressed_path)

        return render_template('index.html', original_file=file.filename,
                               compressed_file='compressed_' + file.filename,
                               compression_ratio=compression_ratio if 'compression_ratio' in locals() else None,
                               success=success if 'success' in locals() else None)


if __name__ == '__main__':
    app.run(debug=True)
