import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, send_file
from werkzeug.utils import secure_filename
import os , io , sys
from PIL import Image
from daltonize import processImage

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/processImage', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
     
		img = Image.open(io.BytesIO(file.read()))
		newImg = processImage(img, int(request.form['type']))
		rawBytes = io.BytesIO()
		newImg.save(rawBytes, "JPEG")
		rawBytes.seek(0)
		return send_file(rawBytes,attachment_filename='teste.jpeg',mimetype='image/jpeg')
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.run()