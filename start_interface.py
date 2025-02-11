from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/images/<path:filename>')
def serve_chatbot_image(filename):
    return send_from_directory('images', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.root_path, 'js'), filename)

@app.route('/')
def index():
    return render_template('index.html')  

if __name__ == '__main__':
    app.run(debug=True, port=5500)
