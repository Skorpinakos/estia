from flask import Flask, send_from_directory

import os

app = Flask(__name__)

# Serve the main page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve CSS files
@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

# Serve JavaScript files
@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

@app.route('/media/<filename>')
def serve_media(filename):
    media_folder = os.path.join(os.getcwd(), 'media')
    return send_from_directory(media_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=1100, host='0.0.0.0')
