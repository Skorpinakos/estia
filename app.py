from flask import Flask, send_from_directory

app = Flask(__name__)

# Serve the main page
@app.route('/')
def index():
    return send_from_directory('.', 'front-end/main.html')

# Serve CSS files
@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'front-end/styles.css')

# Serve JavaScript files
@app.route('/script.js')
def script():
    return send_from_directory('.', 'front-end/script.js')

# Serve images dynamically
@app.route('/<filename>.JPG')
def serve_image(filename):
    return send_from_directory('.', f'front-end/{filename}.JPG')

# Serve images dynamically
@app.route('/<filename>.svg')
def serve_svg(filename):
    return send_from_directory('.', f'front-end/{filename}.svg')

# Serve images dynamically
@app.route('/<filename>.png')
def serve_png(filename):
    return send_from_directory('.', f'front-end/{filename}.png')

if __name__ == '__main__':
    app.run(debug=True, port=1100, host='0.0.0.0')
