import requests
import json

for i in range(343):
    file_name = "IMG_3736/IMG_3736_FRAME_{}.png".format(i+1)
    data = {"bucket": "w-yrs-input-images", "file_key": file_name}
    response = requests.post('http://localhost:5000/api/v1/pred',json=data)
    print("status_code:", response.status_code)
    print("Filename: {}. Respose:{}".format(file_name,json.loads(response.content)))
