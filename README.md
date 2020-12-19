### This document contains details of the Torch Server deployed on EC2

# Step 1 - Initiate an EC2 instant. 
You have an instance already [running](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#InstanceDetails:instanceId=i-0fb18f1105e18d2e5). 
- The public IP of EC2 Instance: ec2-3-138-156-190.us-east-2.compute.amazonaws.com
- Instance type: t2.small (1 VCPU & 2GB RAM)

# Step 2 - Connect to your EC2 instance:
```ssh -i "torch-server.pem" ubuntu@ec2-3-138-156-190.us-east-2.compute.amazonaws.com```
you can find "torch-server.pem" ssh key from the EC2 link posted above

# Step 3A - Source Code details
- api_inputs/  -->  Directory where images are downloaded from S3
- model/   -->  Efficient net pytorch models are stored here. Any new model from API '/api/v1/update_model' are also stored here. load_model() always loads the latest model file.
- venv/   -->  Virutal Environment
- utils.py  -->  Utils for our server
- server.py  -->  Our Flask Application for deploying PyTorch model. All the work is done here
- requirements.txt  -->  Python requirements
- deploy.sh  -->   Setup environment on new EC2 image

# Step 3B - Setup App on EC2
1. Run ```scp -r -i "torch-server.pem" torch_server/* ubuntu@ec2-3-138-156-190.us-east-2.compute.amazonaws.com:/home/ubuntu/torch_server/``` to transfer files from local machine to AWS EC2 instance
2. cd ```/home/ubuntu/torch_server/```
3. (If new EC2 instance) -->>  Run ```sh deply.sh```
4. In order to access S3 buckets from Python App ```nano ~/.aws/credentials``` and write
[default]
aws_access_key_id = <YOUR_ACCESS_KEY>
aws_secret_access_key = <YOUR_SECRET_KEY>

5. ```python server.py```

Now your flask app is runnning and waiting for connections.

