from flask import Flask, send_from_directory

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

# Serve images dynamically
@app.route('/<filename>.JPG')
def serve_image(filename):
    return send_from_directory('.', f'{filename}.JPG')

# Serve images dynamically
@app.route('/<filename>.svg')
def serve_svg(filename):
    return send_from_directory('.', f'{filename}.svg')

# Serve images dynamically
@app.route('/<filename>.webp')
def serve_webp(filename):
    return send_from_directory('.', f'{filename}.webp')

# Serve images dynamically
@app.route('/<filename>.png')
def serve_png(filename):
    return send_from_directory('.', f'{filename}.png')

if __name__ == '__main__':
    app.run(debug=True, port=1100, host='0.0.0.0')
