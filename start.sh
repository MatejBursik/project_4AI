#!/bin/bash

# Define variables
PAYLOAD=""

# Update package list
echo "Updating package list..."
sudo apt update

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y pip swig python3-dev python3-setuptools

# Install Python requirements
echo "Installing Python requirements..."
sudo pip install -r requirements_hard.txt

# Install wiringpi
echo "Installing WiringOP-Python..."
git clone --recursive https://github.com/orangepi-xunlong/wiringOP-Python.git
cd wiringOP-Python
python3 generate-bindings.py > bindings.i
sudo python3 setup.py install
cd ..

# Create the .env file
echo "Creating .env file..."
echo -e "access_token=a\npayload=$PAYLOAD\nloc_id=l" > .env
sudo python3 cronjob_access_token.py
sleep 10
sudo python3 set_loc_id.py
sleep 10

# Install Docker
echo "Installing Docker..."
curl -fsSL get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Pull Docker image
# or Build a Docker image
echo "Pulling or Building Docker image..."
#docker pull jorikgoris/project40-ai:testing-53cb65fc
docker build -t project40-ai:1.0 .

# Run Docker container
echo "Running Docker container..."
#docker run -it --rm --name project40-ai jorikgoris/project40-ai:testing-53cb65fc /bin/bash
docker run -it --rm --name project40-ai project40-ai:1.0 /bin/bash

# Run relay script
echo "Running relay.py..."
sudo python3 relay.py
