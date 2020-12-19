## Flask Server

from fastai.vision.all import get_image_files
import torch
import json

from flask import Flask, request
from flask_cors import CORS
import boto3, os
import pathlib

from utils import clean_api_dir, model_load, get_model_S3, get_image_S3, get_latest_model

app = Flask(__name__)
CORS(app)
pathlib.WindowsPath = pathlib.PosixPath
s3 = boto3.resource('s3')

model_path = "model/efficientnet_lite0__v4.2.pkl"
model = None
model_path = get_latest_model()
model = model_load(model_path)
# get_model_S3()

image_download_path = "api_inputs/api_image_tmp"

@app.route("/api/v1/pred", methods=["GET", "POST"])
def inference():
	if request.method == "GET":
		return "Only POST method accepted!"
	if request.method == "POST":
		global model
		# print(request.data)
		payload = request.get_json()
		print(payload)
		bucket = payload['bucket']
		file_key = payload['file_key']
		filename, file_extension = os.path.splitext(file_key)
		save_image_path = image_download_path + file_extension
		print("save_image_path:", save_image_path)
		if file_extension not in [".jpeg", ".jpg", ".png", ".tiff"]:
			return "Invalid Image extension. Allowed extensions: {}".format(", ".join([".jpeg", ".jpg", ".png", ".tiff"]))

		clean_api_dir()

		get_image_S3(s3, bucket, file_key, save_image_path)
		# save_image_path = "input/IMG_3770_FRAME_54.png"
		print("Starting Prediction!")
		pred = predict_image(model, save_image_path)

		return json.dumps(pred)
	else:
		return "Unkown invokation. Please use POST Request"


@app.route("/api/v1/update_model", methods=["POST"])
def update_model():
	if request.method == "POST":
		global model
		payload = request.get_json()
		print(payload)
		bucket = payload['bucket']
		model_key = payload['model_key']

		num_models = len(os.listdir('model'))
		fname = os.path.basename(model_key)
		fname_split = os.path.splitext(fname)
		model_download_path = os.path.join("model", "{}-{}{}".format(fname_split[0], num_models, fname_split[1]))
		print("Final Model Path:", model_download_path)
		try:
			get_image_S3(s3, bucket, model_key, model_download_path)
		except:
			return {"statusCode": 400, "msg": "ERROR Downloading odel from S3. Have you given the right path?"}
		try:
			model = model_load(model_download_path)
			return {"statusCode": 200, "msg":"Model Successfully loaded: {}".format(model_download_path)}
		except:
			return {"statusCode": 400, "msg": "ERROR loading new model"}


def predict_image(model, image_path):
	g = get_image_files("api_inputs")
	for img in g:
		pred = model.predict(img)
		print(pred)
		label_idx = int(pred[1].numpy())
		confidence = pred[2].numpy()[label_idx].item()
		lbl = pred[0]
		print("Image {}; Predicted Label {}".format(img, lbl))
		return {'image':str(img), 'label':lbl, "confidence": confidence}



if __name__ =="__main__":
	
	app.run(host="0.0.0.0", port=5000, threaded=False, debug=True)