import os
import logging
from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
import config

app = Flask(__name__)
app.config.from_object(config)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_path = os.path.join(app.root_path, 'logs/application.log')
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

from flask import jsonify

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        file_url = url_for('download_file', filename=filename)
        response = jsonify({'filename': filename, 'file_url': file_url})
        logger.info(f'File uploaded: {filename}')
        return response
    else:
        return render_template('upload.html')

@app.route('/downloads/<path:filename>')
def download_file(filename):
    logger.info(f'File downloaded: {filename}')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/static/css/styles.css')
def serve_css():
    return app.send_static_file('css/styles.css')