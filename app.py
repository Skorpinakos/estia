from flask import Flask, send_from_directory

import os

app = Flask(__name__)

# Serve the main page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
# Serve html page as file for caching
@app.route('/index.html')
def index_html():
    return send_from_directory('.', 'index.html')

# Serve CSS files
@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

# Serve favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico')

# Serve JavaScript files
@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

# Serve js data file
@app.route('/data.js')
def data():
    return send_from_directory('.', 'data.js')

# Serve service-worker js file
@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js')


# Serve manifest
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

#Serve media
@app.route('/media/<filename>')
def serve_media(filename):
    media_folder = os.path.join(os.getcwd(), 'media')
    return send_from_directory(media_folder, filename)

#Serve icons
@app.route('/media/icons/<filename>')
def serve_icons(filename):
    media_folder = os.path.join(os.getcwd(), 'media/icons')
    return send_from_directory(media_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=1100, host='0.0.0.0')
