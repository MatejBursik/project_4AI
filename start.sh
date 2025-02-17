#!/bin/bash

# Define variables
PAYLOAD="..."
# Before running the script, fill in the variable payload in this format:
# "{\"client_id\":\" ... \",
# \"client_secret\":\" ... \",
# \"audience\":\" ... ",
# \"grant_type\":\"client_credentials\"}"

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

# Create and populating the .env file
echo "Creating .env file..."
echo -e "access_token=a\npayload=$PAYLOAD\nloc_id=l" > .env
sudo python3 cronjob_access_token.py
sleep 5
sudo python3 set_loc_id.py
sleep 5

# Install Docker
echo "Installing Docker..."
curl -fsSL get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
# Use the `exit` command when the test container cli pops up

# Build Docker image
# or Pull a Docker image
echo "Pulling or Building Docker image..."
docker build -t project40-ai:1.0 .
#docker pull name/project40-ai:testing-1

# Run button script
echo "Running hardware button script..."
sudo python3 button.py
