import requests
import json

data = {"bucket": "deploy-ml-api-inferenceapp-1ejhpq7o2563r", "file_key": "torch_EC2/IMG_3770_FRAME_56.png"}
response = requests.post('http://ec2-3-138-156-190.us-east-2.compute.amazonaws.com:5000/api/v1/pred', 
	json=data)

print("status_code:", response.status_code)
print(json.loads(response.content))