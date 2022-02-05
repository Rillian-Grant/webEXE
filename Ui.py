from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import uuid, os, shutil

from Builder import QUEUE_DIR

UPLOAD_FOLDER = 'queue'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!')
            return redirect("/")
        file = request.files['file']
        if file.filename == '':
            flash('No file selected!')
            return redirect("/")
        if file and allowed_file(file.filename):
            file_id = uuid.uuid4().hex
            file.save(os.path.join(UPLOAD_FOLDER, file_id + ".notouch"))
            shutil.move(os.path.join(UPLOAD_FOLDER, file_id + ".notouch"), os.path.join(UPLOAD_FOLDER, file_id))
            return redirect("/" + file_id)

@app.route("/<id>")
def job(id):
    if not is_hex(id): return redirect(url_for('index'))

    if os.path.exists(os.path.join(UPLOAD_FOLDER, id)):
        return render_template('processing.html')
    if os.path.exists(os.path.join(UPLOAD_FOLDER, id + ".done")):
        return render_template('download.html', id=id)
    else:
        return render_template('error.html')

@app.route("/<id>/download")
def download(id):
    return send_from_directory(
        QUEUE_DIR,
        id + ".done",
        as_attachment=True,
        download_name="WebEXE.exe"
    )

if __name__ == '__main__':
    app.run(port=8000)
