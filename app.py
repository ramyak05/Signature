from distutils.command.upload import upload
import os
from flask import Flask, flash, request, redirect, url_for, render_template 
from werkzeug.utils import secure_filename
from model_utils import is_forged

UPLOAD_FOLDER = './upload'
TEST_FOLDER = './test'
ALLOWED_EXTENSIONS =['png','jpg']
app = Flask(__name__) 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash("upload successful")
            return redirect(request.url) # go home
    return render_template("upload_image.html")

@app.route('/', methods=['GET','POST'])
def test():
    res = os.listdir('./upload')
    if request.method == 'GET':
        print("GET")
        print(res)
        return render_template('display.html',results=res)
    if request.method == 'POST':
        print("POST")
        select = request.form.get('anchor')
        print(str(select))
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(TEST_FOLDER, filename))
            flash("upload successful")
            #flash(is_forged(filename, select))
            return redirect(request.url) # go home
    return render_template("upload_image.html")


    