from fastai.vision.all import load_learner
import pathlib
import boto3
import os, glob

def clean_api_dir():
	files = glob.glob('api_inputs/*')
	for f in files:
	    os.remove(f)

def model_load(model_path):
    # pathlib.WindowsPath = pathlib.PosixPath
    #print ("fastai: version {}".format(fastai.__version__))
    print("Loading Model ...")
    model_path = pathlib.Path(model_path)
    learn_inf = load_learner(model_path)
    print("Model Loaded")
    return learn_inf

def get_model_S3():
    # Define the directory where the model and images will be downloaded 
    temp_dir = 'tmp'
    
    #Download Model from S3 and save in tmp/ 
    model_file_name = 'efficientnet_lite0__v4.2.pkl'
    model_download_path = os.path.join(temp_dir, model_file_name)
    print('Downloading model...')
    s3 = boto3.resource('s3')
    s3.Bucket('wyrs').download_file('prerak/efficientnet_lite0__v4.2.pkl', model_download_path)
    print('Model downloaded.')

def get_image_S3(s3, bucket, image_key, image_download_path):
	# image_key = 'IMG_3770_FRAME_54.png'

	# image_download_path = os.path.join(temp_dir, image_key)
	print('Downloading image...')
	s3.Bucket(bucket).download_file(image_key, image_download_path)
	print('Image downloaded.')

def get_latest_model():
	list_of_files = glob.glob('model/*') # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	print("Last Model File:", latest_file)
	return latest_file
