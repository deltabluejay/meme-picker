from flask import Flask, jsonify, send_from_directory, request, render_template_string
import os
import random
import shutil

app = Flask(__name__)

MEMES_FOLDER = 'memes'
USED_MEMES_FOLDER = 'used_memes'

if not os.path.exists(USED_MEMES_FOLDER):
    os.makedirs(USED_MEMES_FOLDER)

current_meme = None

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Random Meme Picker</title>
</head>
<body>
    <h1>Random Meme Picker</h1>
    {% if current_meme.endswith(('mp4')) %}
        <video id="meme" controls style="max-width: 500px;">
            <source src="/{{ current_meme }}" type="video/mp4">
            Your browser does not support the video tag.
        </video><br>
    {% else %}
        <img id="meme" src="/{{ current_meme }}" style="max-width: 500px;"><br>
    {% endif %}
    <button onclick="acceptMeme()">Accept</button>
    <button onclick="newMeme()">New Meme</button>
    
    <script>
        function acceptMeme() {
            fetch('/accept', { method: 'POST' }).then(() => location.reload());
        }
        function newMeme() {
            location.reload();
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    global current_meme
    files = [f for f in os.listdir(MEMES_FOLDER) if f.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4', 'webp'))]
    if not files:
        return jsonify({'message': 'No media files found'})
    current_meme = random.choice(files)
    return render_template_string(TEMPLATE, current_meme=current_meme)

@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory(MEMES_FOLDER, filename)

@app.route('/accept', methods=['POST'])
def accept_meme():
    global current_meme
    if current_meme:
        src_path = os.path.join(MEMES_FOLDER, current_meme)
        dest_path = os.path.join(USED_MEMES_FOLDER, current_meme)
        shutil.move(src_path, dest_path)
        return jsonify({'message': f'Meme {current_meme} moved to used_memes'})
    return jsonify({'message': 'No meme to accept'})

@app.route('/new', methods=['POST'])
def new_meme():
    global current_meme
    files = [f for f in os.listdir(MEMES_FOLDER) if f.endswith(('png', 'jpg', 'jpeg', 'gif', 'mp4'))]
    if not files:
        return jsonify({'message': 'No media files found'})
    current_meme = random.choice(files)
    return jsonify({'meme': current_meme})

if __name__ == '__main__':
    app.run(debug=False)
