# app.py
from flask import Flask, send_file, render_template
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr')
def serve_qr():
    return send_file('static/vcard_qr.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
