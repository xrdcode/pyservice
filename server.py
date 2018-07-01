#!/usr/bin/env python 

from flask import Flask
import os
import logging
from flask import Flask, request, jsonify, render_template,redirect,make_response,url_for
from img_processing import process_image
from logging import Formatter, FileHandler


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['jpg','jpeg','png'])
VIEWS = 'views'

app = Flask(__name__,template_folder=VIEWS)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

_VERSION = 1

#util function

def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/extract',methods=['POST'])
def upload():
    file = request.files['file']
    if not allowed(file.filename):
        return jsonify({"error":"unsupported file to uploads"})
    
    try:
        text = process_image(img=file.read())
        return jsonify({"output":text})
    except:
        return jsonify({"error": "something when wrong"})

@app.route('/extract_imgurl',methods=['POST'])
def extract_text():
    try:
        url = request.json['image_url']
        print(url.split('.')[-1])
        if url.split('.')[-1] in ['jpg','png','tif']:
            rec_string = process_image(url=url)
            return jsonify({"output": rec_string })
        else:
            return jsonify({"error": "Not Support file types, please"})
    except:
        return jsonify({"error": "we only support [jpg, ,jpeg, png ,tif] or url like {'image_url': 'some_jpeg_url'}"})


@app.errorhandler(500)
def internal_error(error):
    print(str(error))  # ghetto logging

@app.errorhandler(404)
def not_found_error(error):
    print(str(error))

@app.errorhandler(405)
def not_allowed_error(error):
    print(str(error))

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )

if __name__ == '__main__':
    app.debug = True
    app.run()