# make a simple flask upload server for testing purposes only

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import logging

UPLOAD_FOLDER = Path(
    '/work/download').resolve()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mp3', 'ogg', 'm4a', 'avi', 'mov', 'zip', 'rar', '7z', 'tar', 'gz', 'iso', 'apk', 'exe', 'msi', 'deb', 'pkg', 'dmg', 'bin', 'bat', 'sh', 'py', 'c', 'cpp',
                         'java', 'js', 'html', 'htm', 'css', 'scss', 'json', 'xml', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'csv', 'db', 'dbf', 'log', 'mdb', 'sav', 'sql', 'tar', 'xml', 'apk', 'bat', 'bin', 'com', 'exe', 'jar', 'ai'])
ROOT = Path("/usr/local/apache2/wsgi/upload/static").resolve()
FAVICON = ROOT / "favicon"



error = "<html><head><title>{status}</title></head><body><center><h1>{status}</h1></center><hr><center>{server}</center></body></html>"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# render html file for uploading files


@app.route('/')
def index():
    return (ROOT / 'index.html').resolve().read_bytes() 


@app.route('/', methods=['GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded successfully'


@app.route('/list')
def list():
    return (ROOT / 'list.html').resolve().read_bytes()

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download a file."""
    logging.info('Downloading file= [%s]', filename)
    logging.info(app.root_path)
    full_path = os.path.join(app.root_path, UPLOAD_FOLDER)
    logging.info(full_path)
    return send_from_directory(full_path, filename, as_attachment=True)


@app.route('/list')
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('list.html', files=files)

@app.route('/assets/<path:filename>')
def send_assets(filename):
    
    file=ROOT / 'assets' /filename
    if file.exists():
        return file.read_bytes()
    else:
        return error.format(status="404", server=request.url), 404



@app.route('/', methods=['POST', 'PUT'])
def upload():
    f = request.files['file']
    save_path = UPLOAD_FOLDER / f.filename
    f.save(save_path)
    return 'File uploaded successfully'


@app.route('/favicon.ico')
def favicon():
    return (FAVICON / 'favicon.ico').resolve().read_bytes()

@app.route('/apple-touch-icon.png')
def apple_touch_icon():
    return (FAVICON / 'apple-touch-icon.png').resolve().read_bytes()

@app.route('/favicon-32x32.png')
def favicon_32x32():
    return (FAVICON / 'favicon-32x32.png').resolve().read_bytes()

@app.route('/favicon-16x16.png')
def favicon_16x16():
    return (FAVICON / 'favicon-16x16.png').resolve().read_bytes()

@app.route('/site.webmanifest')
def site_webmanifest():
    return (FAVICON / 'site.webmanifest').resolve().read_bytes()

@app.route('/android-chrome-192x192.png')
def android_chrome_192x192():
    return (FAVICON / 'android-chrome-192x192.png').resolve().read_bytes()

@app.route('/android-chrome-512x512.png')
def android_chrome_512x512():
    return (FAVICON / 'android-chrome-512x512.png').resolve().read_bytes()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
    
