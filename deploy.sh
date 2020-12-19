## Bash Script for Deployment on Fresh Ubuntu 18.04 instance


## NOTE: You have to be inside torch-server/ directory
## cd torch_server
sudo apt-get -y update
sudo apt-get install -y python3-pip
pip3 install virtualenv
python3 -m virtualenv venv
source ./venv/bin/activate

pip3 install -r requirements.txt

##  Setup AWS CLI with Credentials. Next 3 lines are what you paste into ~/.aws/credentials
mkdir ~/.aws && touch ~/.aws/credentials
#  ~/.aws/credentials CONTENT
# [default]
# aws_access_key_id = YOUR_ACCESS_KEY
# aws_secret_access_key = YOUR_SECRET_KEY
