from flask import Flask, request, send_from_directory, jsonify, Response, stream_with_context
from flask_cors import CORS
from werkzeug.utils import secure_filename
import face_blur
import os

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}})

UPLOAD_FOLDER = 'input_videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/anonymize', methods=['POST'])
def anonymize_video():
    if 'inputVideo' not in request.files:
        return jsonify({"error": "No input video provided"}), 400
    input_video = request.files['inputVideo']
    output_filename = request.form.get('outputFilename', 'output_video.mp4')

    if not output_filename.endswith('.mp4'):
        output_filename += '.mp4'

    input_video_filename = secure_filename(input_video.filename)
    input_video.save(os.path.join(app.config['UPLOAD_FOLDER'], input_video_filename))

    face_blur.process_video(os.path.join(app.config['UPLOAD_FOLDER'], input_video_filename), f'output_videos/{output_filename}')
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], input_video_filename))

    return jsonify({"message": "Video processed successfully"}), 200

def generate_video_stream(path):
    with open(path, "rb") as video:
        chunk_size = 4096
        while True:
            chunk = video.read(chunk_size)
            if len(chunk) == 0:
                break
            yield chunk

@app.route('/output_videos/<path:filename>', methods=['GET'])
def output_videos(filename):
    video_path = f'output_videos/{filename}'
    return Response(stream_with_context(generate_video_stream(video_path)), content_type='video/mp4')

if __name__ == "__main__":
    app.run(debug=True)
